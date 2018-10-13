import json

from test_plus import TestCase

from thefederation.tests.factories import NodeFactory


class LegacyPodsJsonViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.node = NodeFactory()
        cls.active_node = NodeFactory(active=True)

    def test_renders(self):
        self.get('/pods.json')
        self.response_200()
        self.assertEqual(
            json.loads(self.last_response.content),
            {'pods': [{'host': self.active_node.host}]},
        )
