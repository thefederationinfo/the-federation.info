from unittest.mock import patch

from django.utils.timezone import now
from test_plus import TestCase

from thefederation.models import Stat
from thefederation.tasks import poll_node, fetch_using_method
from thefederation.tests.fixtures import FETCH_NODE_RESPONSE, FETCH_NODE_RESPONSE__NO_STATS


class FetchUsingMethodTestCase(TestCase):
    def test_returns_none_on_none_method(self):
        self.assertIsNone(fetch_using_method("foo.bar", None))


class PollNodeTestCase(TestCase):
    @patch('thefederation.tasks.fetch_node', return_value=FETCH_NODE_RESPONSE)
    def test_stat__creates_on_successful_poll(self, mock_fetch):
        poll_node('example.com')
        stat = Stat.objects.get(node__host='example.com')
        self.assertEqual(stat.date, now().date())
        self.assertIsNone(stat.platform)
        self.assertIsNone(stat.protocol)
        self.assertEqual(stat.users_total, 4)
        self.assertEqual(stat.users_half_year, 3)
        self.assertEqual(stat.users_monthly, 2)
        self.assertEqual(stat.users_weekly, 1)
        self.assertEqual(stat.local_posts, 5)
        self.assertEqual(stat.local_comments, 6)

    @patch('thefederation.tasks.fetch_node', return_value=FETCH_NODE_RESPONSE__NO_STATS)
    def test_stat__creates_on_successful_poll__no_stats_exposed(self, mock_fetch):
        poll_node('example.com')
        stat = Stat.objects.get(node__host='example.com')
        self.assertEqual(stat.date, now().date())
        self.assertIsNone(stat.platform)
        self.assertIsNone(stat.protocol)
        self.assertIsNone(stat.users_total)
        self.assertIsNone(stat.users_half_year)
        self.assertIsNone(stat.users_monthly)
        self.assertIsNone(stat.users_weekly)
        self.assertIsNone(stat.local_posts)
        self.assertIsNone(stat.local_comments)

    @patch('thefederation.tasks.fetch_node', return_value=FETCH_NODE_RESPONSE)
    def test_stat__updates_on_successful_poll(self, mock_fetch):
        poll_node('example.com')
        assert Stat.objects.filter(node__host='example.com').exists()
        response = FETCH_NODE_RESPONSE
        response['activity']['users']['total'] = 10
        mock_fetch.return_value = response
        poll_node('example.com')
        stat = Stat.objects.get(node__host='example.com')
        self.assertEqual(stat.date, now().date())
        self.assertEqual(stat.users_total, 10)
