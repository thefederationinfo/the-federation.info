from test_plus import TestCase

from thefederation.tests.factories import NodeFactory


class NodeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.node = NodeFactory(version="0.9.0")
        cls.x_version_node = NodeFactory(version="2.x")

    def test_version_tuple__returns_version(self):
        self.assertEqual(self.node.version_tuple, (0, 9, 0))

    def test_version_tuple__survices_x_version(self):
        self.assertEqual(self.x_version_node.version_tuple, (2,))
