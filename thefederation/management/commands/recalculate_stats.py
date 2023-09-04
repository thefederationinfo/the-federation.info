import logging
import datetime

from django.core.management.base import BaseCommand

from thefederation.tasks import aggregate_daily_stats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Recalculate aggregated daily stats from the given date onward"

    def add_arguments(self, parser):
        parser.add_argument(
            "start",
            help="date to start recalculating stats from in the isoformat",
            type=lambda s: datetime.date.fromisoformat(s),
        )
        parser.add_argument(
            "--until",
            help="date to stop in the isoformat. default: datetime.now()",
            type=lambda s: datetime.date.fromisoformat(s),
        )

    def handle(self, *args, **options):
        stop_date = options["until"] or datetime.datetime.now().date()
        current_date = options["start"]

        logger.info(f"recalculating stats from {current_date.isoformat()} to {stop_date.isoformat()}, days: {(stop_date - current_date).days}")

        while current_date <= stop_date:
            logger.info(f"recalculating stats for {current_date.isoformat()}, remaining days: {(stop_date - current_date).days}")

            aggregate_daily_stats(current_date)

            current_date += datetime.timedelta(days=1)
