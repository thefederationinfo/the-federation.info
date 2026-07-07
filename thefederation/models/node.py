import datetime
import re

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now
from django_countries.fields import CountryField
from enumfields import EnumField

from thefederation.enums import Relay
from thefederation.models.base import ModelBase
from thefederation.utils import clean_hostname

__all__ = ("Node",)


class NodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            blocked=False,
            last_success__gte=now() - datetime.timedelta(days=30),
        )

    def pollable(self):
        # active() plus nodes that never had a successful crawl
        # (last_success IS NULL). Such rows only come from legacy data:
        # registration gates on a successful crawl and never writes a
        # node row itself, so they would otherwise stay unpolled forever.
        return self.filter(blocked=False).filter(
            models.Q(last_success__isnull=True)
            | models.Q(last_success__gte=now() - datetime.timedelta(days=30)),
        )


class Node(ModelBase):
    blocked = models.BooleanField(default=False)
    country = CountryField(blank=True)
    features = JSONField(default=dict, blank=True)
    hide_from_list = models.BooleanField(default=False)
    host = models.CharField(max_length=128, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    last_success = models.DateTimeField(null=True, db_index=True)
    name = models.CharField(max_length=300)
    open_signups = models.BooleanField()
    organization_account = models.CharField(max_length=256, blank=True, default="")
    organization_contact = models.CharField(max_length=256, blank=True, default="")
    organization_name = models.CharField(max_length=128, blank=True, default="")
    protocols = models.ManyToManyField("thefederation.Protocol", related_name="nodes", blank=True)
    relay = EnumField(Relay, default=Relay.NONE)
    server_meta = JSONField(default=dict, blank=True)
    services = models.ManyToManyField("thefederation.Service", related_name="nodes", blank=True)
    platform = models.ForeignKey("thefederation.Platform", on_delete=models.PROTECT, related_name="nodes")
    version = models.CharField(max_length=128, blank=True)

    objects = NodeQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} ({self.host})"

    def save(self, *args, **kwargs):
        self.host = clean_hostname(self.host)
        # Nodes that report just the platform name as their name (like
        # "Mastodon") carry no information, use the host instead.
        name_letters = re.match(r"[a-zA-Z]*", self.name)[0]
        if name_letters.lower() == self.platform.name:
            self.name = self.host
        self.version = self.platform.clean_version(self.version)
        # Node data comes from untrusted remote documents, which can carry
        # values longer than our column limits (e.g. a name over 300 chars).
        # Truncate to max_length so a misbehaving node can't abort the save
        # with a DataError ("value too long for type character varying").
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField) and field.max_length:
                value = getattr(self, field.attname, None)
                if isinstance(value, str) and len(value) > field.max_length:
                    setattr(self, field.attname, value[: field.max_length])
        super().save(*args, **kwargs)
