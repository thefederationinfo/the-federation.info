import logging

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from thefederation.models import Node
from thefederation.utils import clean_hostname

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clean duplicate nodes."

    def handle(self, *args, **options):
        for node in Node.objects.only("id", "host").order_by("id").iterator():
            # clean_hostname is idempotent, so a node whose host is already in
            # canonical form cannot become a duplicate when re-saved. Skipping
            # these avoids re-saving (and committing) the entire Node table on
            # every run, which had grown past the rq 3600s job timeout.
            if clean_hostname(node.host) == node.host:
                continue

            original = node.host

            try:
                with transaction.atomic():
                    # Save, cleaning happens there so invalid hostnames will be caught
                    node.save()
            except IntegrityError:
                # Boom, it's a dupe, delete it
                logger.info("Deleted duplicate node id %s with hostname %s", node.id, original)
                node.delete()
