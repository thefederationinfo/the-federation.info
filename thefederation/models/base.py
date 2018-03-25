from django.db import models


class ModelBase(models.Model):
    uuid = models.UUIDField(unique=True, auto_created=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
