import datetime
import random
from typing import Dict, List

from django.utils.timezone import now

from thefederation.models import Stat, Platform


def daily_stats_data() -> Dict:
    """
    Compile daily stats data.
    """
    from_date = now().date() - datetime.timedelta(days=30)
    node_counts = Stat.objects.node_counts(from_date=from_date).order_by('-date')
    global_stats = Stat.objects.for_days(from_date=from_date)
    platform_users = []
    for platform in Platform.objects.all():
        stats = Stat.objects.for_days(platform=platform.name, from_date=from_date)
        if not stats or not stats[0].users_half_year:
            continue
        platform_stat = {
            'name': platform.display_name.replace('.', '．'),
            'percentage': (stats[0].users_half_year / global_stats[0].users_half_year) * 100,
            'value': stats[0].users_half_year,
            'change': stats[0].users_half_year - get_last_stat(stats, 'users_half_year'),
        }
        platform_users.append(platform_stat)
    platform_nodes = []
    for platform in Platform.objects.all():
        stats = Stat.objects.node_counts(
            item_type='platform', value=platform.name, from_date=from_date,
        ).order_by('-date')
        if not stats:
            continue
        platform_stat = {
            'name': platform.display_name.replace('.', '．'),
            'percentage': (stats[0]['count'] / node_counts[0]['count']) * 100,
            'value': stats[0]['count'],
            'change': stats[0]['count'] - get_last_stat(stats, 'count'),
        }
        platform_nodes.append(platform_stat)
    context = {
        'nodes': node_counts[0] if node_counts else None,
        'prevnodes': node_counts[len(node_counts) - 1] if node_counts else None,
        'stat': global_stats[0] if global_stats else None,
        'prevstat': global_stats[len(global_stats) - 1] if global_stats else None,
        'platform_users': platform_users,
        'platform_nodes': platform_nodes,
    }
    return context


def get_last_stat(stats: List[Dict[str, int]], stat: str) -> int:
    count = len(stats) - 1
    while count >= 0:
        try:
            if hasattr(stats[count], stat):
                value = getattr(stats[count], stat)
            elif isinstance(stats[count], dict):
                value = stats[count].get(stat)
            else:
                count -= 1
                continue
            if value is not None:
                return value
            count -= 1
        except AttributeError:
            return 0
