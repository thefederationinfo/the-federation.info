from graphene.test import Client
from test_plus import TestCase

from config.schema import schema
from thefederation.tests.factories import NodeFactory


class SchemaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.node = NodeFactory(active=True)
        cls.inactive_node = NodeFactory()

    def setUp(self):
        self.glient = Client(schema)
