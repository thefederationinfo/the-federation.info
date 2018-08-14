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
        stat = Stat.objects.for_days(days=1, platform=platform.name).first()
        if not stat or not stat.users_half_year:
            continue
        platform_stat = {
            'name': platform.display_name,
            'percentage': (stat.users_half_year / global_stats[0].users_half_year) * 100,
        }
        platform_users.append(platform_stat)

    platform_nodes = []
    for platform in Platform.objects.all():
        stat = Stat.objects.node_counts(item_type='platform', value=platform.name).order_by('-date').first()
        if not stat:
            continue
        platform_stat = {
            'name': platform.display_name,
            'percentage': (stat['count'] / node_counts[0]['count']) * 100,
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
