import datetime

from django.utils.timezone import now
from test_plus import TestCase

from thefederation.models import Node
from thefederation.tests.factories import NodeFactory


class NodeQuerySetTestCase(TestCase):
    def test_active__excludes_never_crawled(self):
        NodeFactory(last_success=None)
        self.assertEqual(Node.objects.active().count(), 0)

    def test_pollable__includes_never_crawled(self):
        node = NodeFactory(last_success=None)
        self.assertEqual(list(Node.objects.pollable()), [node])

    def test_pollable__includes_active(self):
        node = NodeFactory(active=True)
        self.assertEqual(list(Node.objects.pollable()), [node])

    def test_pollable__excludes_stale(self):
        NodeFactory(last_success=now() - datetime.timedelta(days=31))
        self.assertEqual(Node.objects.pollable().count(), 0)

    def test_pollable__excludes_blocked(self):
        NodeFactory(last_success=None, blocked=True)
        NodeFactory(active=True, blocked=True)
        self.assertEqual(Node.objects.pollable().count(), 0)
