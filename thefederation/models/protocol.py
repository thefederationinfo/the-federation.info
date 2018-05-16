from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Protocol',)


class Protocol(ModelBase):
    description = models.TextField(blank=True)
    display_name = models.CharField(max_length=80, blank=True)
    name = models.CharField(max_length=80, unique=True)
    website = models.URLField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)
