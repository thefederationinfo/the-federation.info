from django.core.management.base import BaseCommand

from thefederation.legacy import sync_legacy_data


class Command(BaseCommand):
    help = "Sync legacy DB."

    def handle(self, *args, **options):
        sync_legacy_data()
