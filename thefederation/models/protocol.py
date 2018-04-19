from django.db import models

from thefederation.models.base import ModelBase

__all__ = ('Protocol',)


class Protocol(ModelBase):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """
        Fix some values given by some metadata documents.
        """
        if self.name == 'friendica':
            self.name = 'dfrn'
        elif self.name == 'gnusocial':
            self.name = 'ostatus'
        super().save(*args, **kwargs)
