import datetime
import sys

import django_rq
from django.apps import AppConfig


class TheFederationConfig(AppConfig):
    name = "thefederation"
    verbose_name = "The Federation"

    def ready(self):
        # Only register tasks if RQ Scheduler process
        if "rqscheduler" not in sys.argv:
            return

        from thefederation.social import make_daily_post
        from thefederation.tasks import aggregate_daily_stats
        from thefederation.tasks import clean_duplicate_nodes
        from thefederation.tasks import poll_nodes

        scheduler = django_rq.get_scheduler()
        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.schedule(
            scheduled_time=datetime.datetime.utcnow(),
            func=aggregate_daily_stats,
            interval=5500,
            queue_name='high',
        )
        scheduler.cron(
            '0 10 * * *',
            func=make_daily_post,
            queue_name='high',
        )
        scheduler.cron(
            '18 4 * * *',
            func=clean_duplicate_nodes,
            queue_name='medium',
            timeout=3600,
        )
        scheduler.schedule(
            scheduled_time=datetime.datetime.utcnow(),
            func=poll_nodes,
            interval=10800,
            queue_name='medium',
        )
