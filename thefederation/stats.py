import random

from django.template.loader import render_to_string

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
        stats = Stat.objects.for_days(days=30, platform=platform.name)
        if not stats or not stats[0].users_half_year:
            continue
        platform_stat = {
            'name': platform.display_name.replace('.', '．'),
            'percentage': (stats[0].users_half_year / global_stats[0].users_half_year) * 100,
            'value': stats[0].users_half_year,
            'old_value': stats[0].users_half_year - stats[len(stats)-1].users_half_year,
        }
        platform_users.append(platform_stat)

    platform_nodes = []
    for platform in Platform.objects.all():
        stats = Stat.objects.node_counts(item_type='platform', value=platform.name).order_by('-date')[:30]
        if not stats:
            continue
        platform_stat = {
            'name': platform.display_name.replace('.', '．'),
            'percentage': (stats[0]['count'] / node_counts[0]['count']) * 100,
            'value': stats[0]['count'],
            'old_value': stats[0]['count'] - stats[len(stats)-1]['count'],
        }
        platform_nodes.append(platform_stat)

    context = {
        'nodes': node_counts[0],
        'prevnodes': node_counts[len(node_counts)-1],
        'stat': global_stats[0],
        'prevstat': global_stats[len(global_stats)-1],
        'platform_users': platform_users,
        'platform_nodes': platform_nodes,
    }

    posts = {
        1: "global_counts",
        2: "platform_nodes",
        3: "platform_users",
    }
    post = random.randint(1, 3)

    return render_to_string(f'thefederation/social/{posts[post]}.md', context)
