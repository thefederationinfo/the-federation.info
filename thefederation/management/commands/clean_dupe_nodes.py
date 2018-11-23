import logging

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from thefederation.models import Node

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clean duplicate nodes."

    def handle(self, *args, **options):
        for node in Node.objects.only('id', 'host').order_by('id'):
            original = node.host

            try:
                with transaction.atomic():
                    # Save, cleaning happens there so invalid hostnames will be caught
                    node.save()
            except IntegrityError:
                # Boom, it's a dupe, delete it
                logger.info("Deleted duplicate node id %s with hostname %s", node.id, original)
                node.delete()
