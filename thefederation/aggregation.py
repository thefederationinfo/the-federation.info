"""Stats aggregation and housekeeping concern.

Maps to scheduled database-side jobs (not the crawler, not registration)
in the next-generation architecture at
https://codeberg.org/thefederationinfo/next
"""

import datetime
import logging

from django.core.management import call_command
from django.db import transaction
from django.db.models import Sum
from django.utils.timezone import now

from thefederation.models import Platform, Protocol, Stat

logger = logging.getLogger(__name__)


@transaction.atomic
def aggregate_daily_stats(date=None):
    if not date:
        date = now().date()

    # Do all platforms, protocols and then global
    totals = {
        "users_total": 0,
        "users_half_year": 0,
        "users_monthly": 0,
        "users_weekly": 0,
        "local_posts": 0,
        "local_comments": 0,
    }

    for platform in Platform.objects.all():
        stats = (
            Stat.objects.exclude(node__last_success__lt=now() - datetime.timedelta(days=30))
            .filter(
                node__platform=platform,
                date=date,
                node__blocked=False,
                node__hide_from_list=False,
            )
            .aggregate(
                users_total=Sum("users_total"),
                users_half_year=Sum("users_half_year"),
                users_monthly=Sum("users_monthly"),
                users_weekly=Sum("users_weekly"),
                local_posts=Sum("local_posts"),
                local_comments=Sum("local_comments"),
            )
        )

        Stat.objects.update_or_create(
            date=date,
            protocol=None,
            platform=platform,
            node=None,
            defaults=stats,
        )

        # Increment globals
        for key in totals:
            totals[key] += stats[key] if stats[key] else 0

    for protocol in Protocol.objects.all():
        stats = (
            Stat.objects.exclude(node__last_success__lt=now() - datetime.timedelta(days=30))
            .filter(
                node__protocols=protocol,
                date=date,
                node__hide_from_list=False,
                node__blocked=False,
            )
            .aggregate(
                users_total=Sum("users_total"),
                users_half_year=Sum("users_half_year"),
                users_monthly=Sum("users_monthly"),
                users_weekly=Sum("users_weekly"),
                local_posts=Sum("local_posts"),
                local_comments=Sum("local_comments"),
            )
        )

        Stat.objects.update_or_create(
            date=date,
            protocol=protocol,
            platform=None,
            node=None,
            defaults=stats,
        )

    # Add global stat
    Stat.objects.update_or_create(date=date, protocol=None, platform=None, node=None, defaults=totals)


def clean_duplicate_nodes():
    """
    Call the clean dupe nodes command.
    """
    call_command("clean_dupe_nodes")
    # Also re-aggregate stats from a few days
    for single_date in (now().date() - datetime.timedelta(n) for n in range(2)):
        aggregate_daily_stats(single_date)
