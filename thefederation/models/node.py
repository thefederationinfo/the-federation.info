import datetime
import re

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.functions import Lower
from django.utils.functional import cached_property
from django.utils.timezone import now
from django_countries.fields import CountryField
from enumfields import EnumField

from thefederation.enums import Relay
from thefederation.models.base import ModelBase
from thefederation.utils import clean_hostname

__all__ = ('Node',)

models.CharField.register_lookup(Lower)
class NodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            blocked=False,
            last_success__gte=now() - datetime.timedelta(days=30),
        )


class Node(ModelBase):
    blocked = models.BooleanField(default=False)
    country = CountryField(blank=True)
    features = JSONField(default={}, blank=True)
    hide_from_list = models.BooleanField(default=False)
    host = models.CharField(max_length=128, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    last_success = models.DateTimeField(null=True, db_index=True)
    name = models.CharField(max_length=300)
    open_signups = models.BooleanField()
    organization_account = models.CharField(max_length=256, blank=True, default="")
    organization_contact = models.CharField(max_length=256, blank=True, default="")
    organization_name = models.CharField(max_length=128, blank=True, default="")
    protocols = models.ManyToManyField('thefederation.Protocol', related_name='nodes', blank=True)
    relay = EnumField(Relay, default=Relay.NONE)
    server_meta = JSONField(default={}, blank=True)
    services = models.ManyToManyField('thefederation.Service', related_name='nodes', blank=True)
    platform = models.ForeignKey('thefederation.Platform', on_delete=models.PROTECT, related_name='nodes')
    version = models.CharField(max_length=128, blank=True)

    objects = NodeQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} ({self.host})"

    def save(self, *args, **kwargs):
        self.host = clean_hostname(self.host)
        clean_name = re.match(r'[a-zA-Z]*', self.name)
        if clean_name:
            if self.platform.name == clean_name[0].lower():
                self.name = self.host
        self.version = self.platform.clean_version(self.version)
        super().save(*args, **kwargs)

    @property
    def clean_version(self):
        """
        Get the version number cleaned as a number.
        """
        if not self.version:
            return
        # Strip all non-numbers
        cleaned_str = "".join([c for c in self.version if c.isnumeric() or c == "."]).strip('.')
        # Split into tuple
        return tuple([int(i) for i in cleaned_str.split(".")])

    @cached_property
    def preferred_method(self):
        """
        Calls a function to get the preferred method.

        Function is passed in the version.
        :return:
        """
        return self.platform.get_method(self.clean_version)
