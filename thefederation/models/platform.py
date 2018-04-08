from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Platform',)


class Platform(ModelBase):
    latest_version = models.CharField(max_length=128, blank=True)
    icon = models.CharField(max_length=80, default='unknown')
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.name}"

    def get_method(self, version):
        """
        Calls a function to get the preferred method.

        Tries to compare with a version.

        :param version: tuple of version, numeric only
        :return:
        """
        return {
            'diaspora': 'nodeinfo' if version >= (0, 5, 3, 0) else "statisticsjson",
            'friendica': 'nodeinfo' if version >= (3, 4, 2) else "statisticsjson",
            'ganggo': 'nodeinfo',
            'hubzilla': 'nodeinfo' if version >= (1, 6) else "statisticsjson",
            'socialhome': 'nodeinfo2' if version > (0, 8) else "nodeinfo",
        }.get(self.name)
