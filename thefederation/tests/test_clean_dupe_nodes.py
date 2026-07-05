import datetime

from django.core.management import call_command
from django.utils.timezone import now
from test_plus import TestCase

from thefederation.models import Node, Stat
from thefederation.tests.factories import NodeFactory


class CleanDupeNodesTestCase(TestCase):
    def test_duplicate_is_removed_and_stats_merged(self):
        survivor = NodeFactory(host="example.com")
        dupe = NodeFactory(host="dupe.example.com")
        # Dirty the host the way legacy rows predating the cleaning did,
        # bypassing save() which would clean it.
        Node.objects.filter(pk=dupe.pk).update(host="https://example.com")

        today = now().date()
        yesterday = today - datetime.timedelta(days=1)
        Stat.objects.create(node=survivor, date=today, users_total=1)
        Stat.objects.create(node_id=dupe.pk, date=today, users_total=100)
        Stat.objects.create(node_id=dupe.pk, date=yesterday, users_total=50)

        call_command("clean_dupe_nodes")

        assert not Node.objects.filter(pk=dupe.pk).exists()
        # survivor keeps its own value for the colliding date
        assert Stat.objects.get(node=survivor, date=today).users_total == 1
        # and inherits the date it had no row for
        assert Stat.objects.get(node=survivor, date=yesterday).users_total == 50
