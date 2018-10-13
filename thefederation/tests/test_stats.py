import datetime
from unittest.mock import patch

from django.utils.timezone import now
from freezegun import freeze_time
from test_plus import TestCase

from thefederation.models import Stat
from thefederation.stats import daily_stats, daily_stats_data
from thefederation.tasks import aggregate_daily_stats
from thefederation.tests.factories import NodeFactory, StatFactory


class DailyStatsDataSingleNodeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.node = NodeFactory()
        with freeze_time('2018-03-10'):
            cls.stat1 = StatFactory(node=cls.node, date=now().date())
            aggregate_daily_stats()
        with freeze_time('2018-03-11'):
            cls.stat2 = StatFactory(node=cls.node, date=now().date())
            aggregate_daily_stats()
        with freeze_time('2018-03-12'):
            cls.stat3 = StatFactory(node=cls.node, date=now().date())
            aggregate_daily_stats()

    @patch('thefederation.stats.daily_stats_data', return_value={
        'platform_users': [{
            'name': "foobar",
            'percentage': 100.0,
            'value': 20,
            'change': 10,
        }],
        'platform_nodes': [{
            'name': "barfoo",
            'percentage': 100.0,
            'value': 1,
            'change': 0,
        }],
    })
    def test_renders(self, mock_daily_stats_data):
        daily_stats()

    def test_results(self):
        with freeze_time('2018-03-12'):
            stats = daily_stats_data()
        self.assertEqual(stats['nodes'], {'count': 1, 'date': datetime.date(2018, 3, 12)})
        self.assertEqual(stats['prevnodes'], {'count': 1, 'date': datetime.date(2018, 3, 10)})
        self.assertEqual(stats['stat'], Stat.objects.for_global().filter(date=datetime.date(2018, 3, 12)).first())
        self.assertEqual(stats['prevstat'], Stat.objects.for_global().filter(date=datetime.date(2018, 3, 10)).first())
        self.assertEqual(
            stats['platform_users'][0],
            {
                'name': self.node.platform.display_name or '',
                'percentage': 100.0,
                'value': self.stat3.users_half_year,
                'change': self.stat3.users_half_year - self.stat1.users_half_year,
            },
        )
        self.assertEqual(
            stats['platform_nodes'][0],
            {
                'name': self.node.platform.display_name or '',
                'percentage': 100.0,
                'value': 1,
                'change': 0,
            },
        )

    def test_results__inactive_does_stay_excluded(self):
        with freeze_time('2018-01-10'):
            node = NodeFactory()
            StatFactory(node=node, date=now().date())
            aggregate_daily_stats()

        with freeze_time('2018-01-11'):
            StatFactory(node=node, date=now().date())
            aggregate_daily_stats()

        with freeze_time('2018-01-12'):
            StatFactory(node=node, date=now().date())
            aggregate_daily_stats()

        with freeze_time('2018-03-12'):
            stats = daily_stats_data()
        self.assertEqual(stats['nodes'], {'count': 1, 'date': datetime.date(2018, 3, 12)})
        self.assertEqual(stats['prevnodes'], {'count': 1, 'date': datetime.date(2018, 3, 10)})
        self.assertEqual(stats['stat'], Stat.objects.for_global().filter(date=datetime.date(2018, 3, 12)).first())
        self.assertEqual(stats['prevstat'], Stat.objects.for_global().filter(date=datetime.date(2018, 3, 10)).first())
        self.assertEqual(
            stats['platform_users'][0],
            {
                'name': self.node.platform.display_name or '',
                'percentage': 100.0,
                'value': self.stat3.users_half_year,
                'change': self.stat3.users_half_year - self.stat1.users_half_year,
            },
        )
        self.assertEqual(
            stats['platform_nodes'][0],
            {
                'name': self.node.platform.display_name or '',
                'percentage': 100.0,
                'value': 1,
                'change': 0,
            },
        )
