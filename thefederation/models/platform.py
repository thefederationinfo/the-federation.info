from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Platform',)


class Platform(ModelBase):
    VERSION_CLEAN_NONE = 'none'
    VERSION_CLEAN_REMOVE_AFTER_DASH = 'remove_after_dash'
    VERSION_CLEAN_STYLES = (
        (VERSION_CLEAN_NONE, VERSION_CLEAN_NONE),
        (VERSION_CLEAN_REMOVE_AFTER_DASH, VERSION_CLEAN_REMOVE_AFTER_DASH),
    )

    code = models.URLField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    display_name = models.CharField(max_length=128, blank=True)
    latest_version = models.CharField(max_length=128, blank=True)
    license = models.CharField(max_length=128, blank=True)
    icon = models.CharField(max_length=80, default='unknown')
    install_guide = models.URLField(max_length=256, blank=True)
    name = models.CharField(max_length=80, unique=True)
    tagline = models.CharField(max_length=300, blank=True)
    version_clean_style = models.CharField(choices=VERSION_CLEAN_STYLES, default=VERSION_CLEAN_NONE, max_length=30)
    website = models.URLField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)

    def clean_version(self, version):
        if self.version_clean_style == Platform.VERSION_CLEAN_NONE:
            return version
        elif self.version_clean_style == Platform.VERSION_CLEAN_REMOVE_AFTER_DASH:
            return version.split('-')[0]
        return version

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
            'mastodon': 'mastodon',
            'socialhome': 'nodeinfo2' if version > (0, 8) else "nodeinfo",
        }.get(self.name)
