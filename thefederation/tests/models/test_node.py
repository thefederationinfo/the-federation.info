from test_plus import TestCase

from thefederation.tests.factories import NodeFactory


class NodeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.node = NodeFactory(version='0.9.0')
        cls.x_version_node = NodeFactory(version='2.x')

    def test_clean_version__returns_version(self):
        self.assertEqual(self.node.clean_version, (0, 9, 0))

    def test_clean_version__survices_x_version(self):
        self.assertEqual(self.x_version_node.clean_version, (2,))
