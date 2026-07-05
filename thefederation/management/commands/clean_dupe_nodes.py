import logging

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from thefederation.models import Node, Stat
from thefederation.utils import clean_hostname

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clean duplicate nodes."

    def handle(self, *args, **options):
        # Full rows on purpose: save() touches name, version, platform and
        # every CharField, and the relay enum field breaks under only()
        # (KeyError on deferred access).
        for node in Node.objects.select_related("platform").order_by("id").iterator():
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
                # It's a dupe. Move its stat history onto the surviving node
                # (only for dates the survivor has no row for) instead of
                # cascading it away with the delete.
                survivor = Node.objects.get(host=clean_hostname(original))
                moved = (
                    Stat.objects.filter(node=node)
                    .exclude(date__in=Stat.objects.filter(node=survivor).values("date"))
                    .update(node=survivor)
                )
                logger.info(
                    "Deleted duplicate node id %s with hostname %s, moved %s stats to node id %s",
                    node.id,
                    original,
                    moved,
                    survivor.id,
                )
                node.delete()
