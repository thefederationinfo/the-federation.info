import time

import shcli
from django.conf import settings

from thefederation.stats import daily_stats


def make_daily_post():
    content = daily_stats()
    shcli.create(
        settings.THEFEDERATION_SOCIALHOME_HOST,
        settings.THEFEDERATION_SOCIALHOME_KEY,
        content,
        settings.THEFEDERATION_SOCIALHOME_VISIBILITY,
    )

    # Sleep for 60 seconds. This might stop duplicate posts due to possibly
    # https://github.com/rq/rq-scheduler/issues/173
    time.sleep(60)
