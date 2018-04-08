from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from django_countries.fields import CountryField
from enumfields import EnumField

from thefederation.enums import Relay
from thefederation.models.base import ModelBase

__all__ = ('Node',)


class Node(ModelBase):
    blocked = models.BooleanField(default=False)
    country = CountryField(blank=True)
    failures = models.PositiveIntegerField(default=0)
    features = JSONField(default={})
    hide_from_list = models.BooleanField(default=False)
    host = models.CharField(max_length=128, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    name = models.CharField(max_length=300)
    open_signups = models.BooleanField()
    organization_account = models.CharField(max_length=256, blank=True)
    organization_contact = models.CharField(max_length=256, blank=True)
    organization_name = models.CharField(max_length=128, blank=True)
    protocols = models.ManyToManyField('thefederation.Protocol', related_name='nodes')
    relay = EnumField(Relay, default=Relay.NONE)
    server_meta = JSONField(default={})
    services = models.ManyToManyField('thefederation.Service', related_name='nodes')
    platform = models.ForeignKey('thefederation.Platform', on_delete=models.PROTECT, related_name='nodes')
    version = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name} ({self.host})"

    @property
    def clean_version(self):
        """
        Get the version number cleaned as a number.
        """
        if not self.version:
            return
        # Strip all non-numbers
        cleaned_str = "".join([c for c in self.version if c.isnumeric() or c == "."])
        # Split into tuple
        return tuple([int(i) for i in cleaned_str.split(".")])

    @staticmethod
    def log_failure(host):
        """
        Increment failure counter of node.
        """
        # TODO implement
        pass

    @cached_property
    def preferred_method(self):
        """
        Calls a function to get the preferred method.

        Function is passed in the version.
        :return:
        """
        return self.platform.get_method(self.clean_version)
