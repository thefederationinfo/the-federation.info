from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Platform',)


class Platform(ModelBase):
    latest_version = models.CharField(max_length=128, blank=True)
    icon = models.CharField(max_length=80, default='unknown')
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.name}"
