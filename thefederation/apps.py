import datetime

import django_rq
from django.apps import AppConfig


class TheFederationConfig(AppConfig):
    name = "thefederation"
    verbose_name = "The Federation"

    def ready(self):
        from thefederation.tasks import aggregate_daily_stats
        from thefederation.tasks import poll_nodes

        scheduler = django_rq.get_scheduler('high')
        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.schedule(
            scheduled_time=datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            func=aggregate_daily_stats,
            interval=1500,
        )

        scheduler = django_rq.get_scheduler('medium')
        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.schedule(
            scheduled_time=datetime.datetime.utcnow(),
            func=poll_nodes,
            interval=3600,
        )
