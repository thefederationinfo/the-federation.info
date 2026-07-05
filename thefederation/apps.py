import sys

import django_rq
from django.apps import AppConfig
from django.utils.timezone import now


class TheFederationConfig(AppConfig):
    name = "thefederation"
    verbose_name = "The Federation"

    def ready(self):
        # Only register tasks if RQ Scheduler process
        if "rqscheduler" not in sys.argv:
            return

        from thefederation.aggregation import aggregate_daily_stats
        from thefederation.aggregation import clean_duplicate_nodes
        from thefederation.crawler import fill_country_information
        from thefederation.crawler import poll_nodes

        scheduler = django_rq.get_scheduler()
        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.schedule(
            scheduled_time=now(),
            func=aggregate_daily_stats,
            interval=5500,
            queue_name="high",
        )
        scheduler.cron(
            "18 4 * * *",
            func=clean_duplicate_nodes,
            queue_name="medium",
            timeout=3600,
        )
        scheduler.cron(
            "23 6 * * *",
            func=fill_country_information,
            queue_name="low",
            timeout=3600,
        )
        scheduler.schedule(
            scheduled_time=now(),
            func=poll_nodes,
            interval=10800,
            queue_name="medium",
        )
