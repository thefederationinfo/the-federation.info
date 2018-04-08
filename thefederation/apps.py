import datetime

import django_rq
from django.apps import AppConfig
from django.utils.timezone import now


class TheFederationConfig(AppConfig):
    name = "thefederation"
    verbose_name = "The Federation"

    def ready(self):
        from thefederation.tasks import aggregate_daily_stats
        from thefederation.tasks import poll_nodes

        scheduler = django_rq.get_scheduler('high')
        scheduler.schedule(
            scheduled_time=now() + datetime.timedelta(minutes=15),
            func=aggregate_daily_stats,
            interval=1500,
        )
        scheduler = django_rq.get_scheduler('medium')
        scheduler.schedule(
            scheduled_time=now(),
            func=poll_nodes,
            interval=3600,
        )
