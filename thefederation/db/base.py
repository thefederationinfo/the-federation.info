import datetime

from django.conf import settings
from django.db.backends.postgresql import base
from django.utils.timezone import utc

__all__ = ("DatabaseWrapper",)


def utc_tzinfo_factory(offset):
    """Copy of django.db.backends.postgresql.utils.utc_tzinfo_factory
    that works with psycopg2 >= 2.9.

    psycopg2 2.9 changed the offset passed to tzinfo_factory from an int
    (minutes) to a datetime.timedelta. Django 2.2 compares against the
    int 0, and timedelta(0) != 0, so every timestamptz fetch raises
    "database connection isn't set to UTC" even though the connection
    *is* set to UTC. Changing connection properties cannot fix this, the
    comparison itself is the bug. Django only fixed it in 3.1.13/3.2.4.
    """
    if offset not in (0, datetime.timedelta(0)):
        raise AssertionError("database connection isn't set to UTC")
    return utc


class DatabaseWrapper(base.DatabaseWrapper):
    def create_cursor(self, name=None):
        cursor = super().create_cursor(name=name)
        cursor.tzinfo_factory = utc_tzinfo_factory if settings.USE_TZ else None
        return cursor
