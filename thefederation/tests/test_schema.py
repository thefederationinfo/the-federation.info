from thefederation.tests.factories import NodeFactory, StatFactory
from thefederation.tests.utils import SchemaTestCase


class QueryResolveNodesTestCase(SchemaTestCase):
    def test_contains_only_active(self):
        response = self.glient.execute("query { nodes { id }}")
        nodes = [node for node in response['data']['nodes']]
        if self.inactive_node in nodes:
            self.fail('Should not contain inactive node')
        self.assertEqual(response['data']['nodes'][0]['id'], str(self.node.id))

    def test_resolves(self):
        response = self.glient.execute("query { nodes { id }}")
        self.assertTrue('nodes' in response['data'])


class QueryResolvePlatformsTestCase(SchemaTestCase):
    def test_contains_only_active(self):
        response = self.glient.execute("query { platforms { id }}")
        platforms = [platform for platform in response['data']['platforms']]
        if self.inactive_node.platform_id in platforms:
            self.fail('Should not contain inactive platform')
        self.assertEqual(response['data']['platforms'][0]['id'], str(self.node.platform_id))

    def test_resolves(self):
        response = self.glient.execute("query { platforms { id }}")
        self.assertTrue('platforms' in response['data'])


class QueryResolveProtocolsTestCase(SchemaTestCase):
    def test_contains_only_active(self):
        response = self.glient.execute("query { protocols { id }}")
        protocols = [protocol for protocol in response['data']['protocols']]
        if self.inactive_node.protocols.first().id in protocols:
            self.fail('Should not contain inactive protocol')
        self.assertEqual(response['data']['protocols'][0]['id'], str(self.node.protocols.first().id))

    def test_resolves(self):
        response = self.glient.execute("query { protocols { id }}")
        self.assertTrue('protocols' in response['data'])


class QueryResolveStatsUsersActiveRatioTestCase(SchemaTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.second_node = NodeFactory(active=True)
        StatFactory(node=cls.node, users_monthly=1, users_total=2)
        StatFactory(node=cls.second_node, users_monthly=1, users_total=4)

    def test_contains_result(self):
        response = self.glient.execute(
            "query { statsUsersActiveRatio { count }}"
        )
        self.assertAlmostEqual(response['data']['statsUsersActiveRatio'][0]['count'], 0.33333333)


class QueryResolveStatsUsersPerNodeTestCase(SchemaTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.second_node = NodeFactory(active=True)
        StatFactory(node=cls.node, users_total=1)
        StatFactory(node=cls.second_node, users_total=3)

    def test_contains_result(self):
        response = self.glient.execute(
            "query { statsUsersPerNode { count }}"
        )
        self.assertEqual(response['data']['statsUsersPerNode'][0]['count'], 2)
