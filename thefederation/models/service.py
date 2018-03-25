from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Service',)


class Service(ModelBase):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.name}"
