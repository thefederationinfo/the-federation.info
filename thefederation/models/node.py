from django.contrib.postgres.fields import JSONField
from django.db import models
from django_countries.fields import CountryField
from enumfields import EnumField

from thefederation.enums import Relay
from thefederation.models.base import ModelBase

__all__ = ('Node',)


class Node(ModelBase):
    admin_email = models.EmailField(blank=True)
    blocked = models.BooleanField(default=False)
    country = CountryField(blank=True)
    failures = models.PositiveIntegerField(default=0)
    features = JSONField(default={})
    hide_from_list = models.BooleanField(default=False)
    host = models.CharField(max_length=128, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    name = models.CharField(max_length=300)
    open_signups = models.BooleanField()
    protocols = models.ManyToManyField('thefederation.Protocol', related_name='nodes')
    relay = EnumField(Relay, default=Relay.NONE)
    server_meta = JSONField(default={})
    services = models.ManyToManyField('thefederation.Service', related_name='nodes')
    platform = models.ForeignKey('thefederation.Platform', on_delete=models.PROTECT, related_name='nodes')
    version = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name} ({self.host})"
