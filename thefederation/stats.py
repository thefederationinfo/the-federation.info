import datetime

from django.template.loader import render_to_string
from django.utils.timezone import now

from thefederation.models import Stat, Platform


def daily_stats():
    """
    Compile a daily stats post.

    :return: str
    """
    node_counts = Stat.objects.node_counts().order_by('-date')[:30]
    global_stats = Stat.objects.for_days(days=30)

    platform_users = []
    for platform in Platform.objects.all():
        stats = Stat.objects.for_days(days=30, later_than=now() - datetime.timedelta(days=30), platform=platform.name)
        if not stats or not stats[0].users_monthly:
            continue
        platform_stat = {
            'name': platform.display_name,
            'percentage': (stats[0].users_monthly / global_stats[0].users_monthly) * 100,
        }
        if len(stats) > 1 and stats[len(stats)-1].users_monthly:
            platform_stat['change'] = (
                platform_stat['percentage'] -
                (stats[len(stats)-1].users_monthly / global_stats[len(stats)-1].users_monthly) * 100
            )
        else:
            platform_stat['change'] = 0
        platform_users.append(platform_stat)

    platform_nodes = []
    for platform in Platform.objects.all():
        stats = Stat.objects.node_counts(
            later_than=now() - datetime.timedelta(days=30), item_type='platform', value=platform.name,
        )[:30]
        if not stats:
            continue
        platform_stat = {
            'name': platform.display_name,
            'percentage': (stats[0]['count'] / node_counts[0]['count']) * 100,
        }
        if len(stats) > 1:
            platform_stat['change'] = (
                platform_stat['percentage'] -
                (stats[len(stats)-1]['count'] / node_counts[len(stats)-1]['count']) * 100
            )
        else:
            platform_stat['change'] = 0
        platform_nodes.append(platform_stat)

    context = {
        'nodes': node_counts[0],
        'prevnodes': node_counts[len(node_counts)-1],
        'stat': global_stats[0],
        'prevstat': global_stats[len(global_stats)-1],
        'platform_users': platform_users,
        'platform_nodes': platform_nodes,
    }

    return render_to_string('thefederation/social/daily_stats.md', context)
