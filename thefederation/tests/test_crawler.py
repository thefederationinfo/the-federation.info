from unittest.mock import MagicMock, patch

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils.timezone import now
from test_plus import TestCase

from thefederation.models import Node, Stat
from thefederation.crawler import fetch_using_method, fill_country_information, poll_node
from thefederation.tests.fixtures import FETCH_NODE_RESPONSE, FETCH_NODE_RESPONSE__NO_STATS
from thefederation.tests.factories import NodeFactory


class FetchUsingMethodTestCase(TestCase):
    def test_returns_none_on_none_method(self):
        self.assertIsNone(fetch_using_method("foo.bar", None))


class PollNodeTestCase(TestCase):
    @patch("thefederation.crawler.fetch_node", return_value=FETCH_NODE_RESPONSE)
    def test_stat__creates_on_successful_poll(self, mock_fetch):
        poll_node("example.com")
        stat = Stat.objects.get(node__host="example.com")
        self.assertEqual(stat.date, now().date())
        self.assertIsNone(stat.platform)
        self.assertIsNone(stat.protocol)
        self.assertEqual(stat.users_total, 4)
        self.assertEqual(stat.users_half_year, 3)
        self.assertEqual(stat.users_monthly, 2)
        self.assertEqual(stat.users_weekly, 1)
        self.assertEqual(stat.local_posts, 5)
        self.assertEqual(stat.local_comments, 6)

    @patch("thefederation.crawler.fetch_node", return_value=FETCH_NODE_RESPONSE__NO_STATS)
    def test_stat__creates_on_successful_poll__no_stats_exposed(self, mock_fetch):
        poll_node("example.com")
        stat = Stat.objects.get(node__host="example.com")
        self.assertEqual(stat.date, now().date())
        self.assertIsNone(stat.platform)
        self.assertIsNone(stat.protocol)
        self.assertIsNone(stat.users_total)
        self.assertIsNone(stat.users_half_year)
        self.assertIsNone(stat.users_monthly)
        self.assertIsNone(stat.users_weekly)
        self.assertIsNone(stat.local_posts)
        self.assertIsNone(stat.local_comments)

    @patch("thefederation.crawler.fetch_node")
    def test_stat__rejects_out_of_range_local_posts(self, mock_fetch):
        import copy

        response = copy.deepcopy(FETCH_NODE_RESPONSE)
        response["activity"]["local_posts"] = 2147483648
        mock_fetch.return_value = response
        self.assertFalse(poll_node("example.com"))
        self.assertFalse(Stat.objects.filter(node__host="example.com").exists())

    @patch("thefederation.crawler.fetch_node", return_value=FETCH_NODE_RESPONSE)
    def test_stat__no_write_on_unchanged_repeat_poll(self, mock_fetch):
        poll_node("example.com")
        with CaptureQueriesContext(connection) as ctx:
            poll_node("example.com")
        stat_writes = [
            query["sql"]
            for query in ctx.captured_queries
            if query["sql"].startswith(("UPDATE", "INSERT")) and "thefederation_stat" in query["sql"]
        ]
        self.assertEqual(stat_writes, [])

    @patch("thefederation.crawler.fetch_node", return_value=FETCH_NODE_RESPONSE)
    def test_stat__updates_on_successful_poll(self, mock_fetch):
        poll_node("example.com")
        assert Stat.objects.filter(node__host="example.com").exists()
        response = FETCH_NODE_RESPONSE
        response["activity"]["users"]["total"] = 10
        mock_fetch.return_value = response
        poll_node("example.com")
        stat = Stat.objects.get(node__host="example.com")
        self.assertEqual(stat.date, now().date())
        self.assertEqual(stat.users_total, 10)


class FetchUsingMethodMissingFetcherTestCase(TestCase):
    def test_unknown_method_returns_none(self):
        self.assertIsNone(fetch_using_method("foo.bar", "doesnotexist"))


class PollNodeRobustnessTestCase(TestCase):
    @patch("thefederation.crawler.fetch_node")
    def test_host_mismatch_is_discarded(self, mock_fetch):
        import copy

        result = copy.deepcopy(FETCH_NODE_RESPONSE)
        result["host"] = "other.example.com"
        mock_fetch.return_value = result
        self.assertFalse(poll_node("example.com"))
        self.assertFalse(Node.objects.filter(host__contains="example.com").exists())

    @patch("thefederation.crawler.fetch_node")
    def test_empty_protocol_and_service_entries_are_skipped(self, mock_fetch):
        import copy

        result = copy.deepcopy(FETCH_NODE_RESPONSE)
        result["protocols"] = ["", "activitypub"]
        result["services"] = ["", "gnusocial"]
        mock_fetch.return_value = result
        self.assertTrue(poll_node("example.com"))
        node = Node.objects.get(host="example.com")
        self.assertEqual([p.name for p in node.protocols.all()], ["activitypub"])
        self.assertEqual([s.name for s in node.services.all()], ["gnusocial"])


class FillCountryInformationTestCase(TestCase):
    def _run(self, node, ip, iso_code):
        country_record = MagicMock()
        country_record.iso_code = iso_code
        response = MagicMock()
        response.country = country_record
        reader = MagicMock()
        reader.country.return_value = response
        with (
            patch("thefederation.crawler.geoip2.database.Reader", return_value=reader),
            patch("thefederation.crawler.fetch_host_ip", return_value=ip),
        ):
            fill_country_information()

    def test_sets_resolved_country(self):
        node = NodeFactory(active=True, ip="10.0.0.1")
        self._run(node, "10.0.0.1", "DE")
        node.refresh_from_db()
        assert node.country.code == "DE"

    def test_unresolved_country_does_not_rewrite_node(self):
        node = NodeFactory(active=True, ip="10.0.0.1")
        updated_before = Node.objects.get(pk=node.pk).updated
        self._run(node, "10.0.0.1", None)
        assert Node.objects.get(pk=node.pk).updated == updated_before
