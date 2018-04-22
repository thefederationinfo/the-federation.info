import datetime
import logging

from django.db.models import Sum
from django.utils.timezone import now
from django_rq import job
from federation.hostmeta import fetchers

from thefederation.enums import Relay
from thefederation.models import Node, Platform, Protocol, Service, Stat

logger = logging.getLogger(__name__)

METHODS = ['nodeinfo2', 'nodeinfo', 'statisticsjson']


def aggregate_daily_stats():
    # Do all platforms and then global
    totals = {
        'users_total': 0,
        'users_half_year': 0,
        'users_monthly': 0,
        'users_weekly': 0,
        'local_posts': 0,
        'local_comments': 0,
    }
    today = now().date()
    for platform in Platform.objects.all():
        stats = Stat.objects.exclude(
            node__last_success__lt=now() - datetime.timedelta(days=30)
        ).filter(
            node__platform=platform,
            date=today,
        ).aggregate(
            users_total=Sum('users_total'),
            users_half_year=Sum('users_half_year'),
            users_monthly=Sum('users_monthly'),
            users_weekly=Sum('users_weekly'),
            local_posts=Sum('local_posts'),
            local_comments=Sum('local_comments'),
        )
        Stat.objects.update_or_create(
            date=today, platform=platform, node=None, defaults=stats,
        )
        # Increment globals
        for key in totals:
            totals[key] += stats[key] if stats[key] else 0
    # Add global stat
    Stat.objects.update_or_create(date=today, platform=None, node=None, defaults=totals)


def fetch_using_method(host, method):
    logger.debug(f'Fetching {host} using method {method}')
    func = getattr(fetchers, f"fetch_{method}_document")
    return func(host)


def fetch_node(host):
    """
    Fetch differet documents in order

    If host exists, use preferred document, falling back to all.

    :param host: str
    :return: dict
    """
    # Use preferred method if known
    try:
        node = Node.objects.only('platform', 'version').get(host=host)
    except Node.DoesNotExist:
        methods = METHODS[:]
    else:
        result = fetch_using_method(host, node.preferred_method)
        if result:
            return result
        methods = METHODS[:]
        methods.remove(node.preferred_method)

    # Use remaining methods
    for method in methods:
        result = fetch_using_method(host, method)
        if result:
            return result


@job('medium')
def poll_node(host):
    result = fetch_node(host)
    if not result:
        logger.info(f'No result for {host}.')
        return False

    assert host == result.get('host')
    platform, _created = Platform.objects.get_or_create(name=result['platform'])
    node, _created = Node.objects.update_or_create(
        host=host,
        defaults={
            'features': result.get('features', {}),
            'ip': result.get('ip'),
            'last_success': now(),
            'name': result.get('name') or host,
            'open_signups': result.get('open_signups', False),
            'organization_account': result.get('organization', {}).get('account', ''),
            'organization_contact': result.get('organization', {}).get('contact', ''),
            'organization_name': result.get('organization', {}).get('name', ''),
            'relay': result.get('relay') or Relay.NONE,
            'server_meta': result.get('server_meta', {}),
            'version': result.get('version', ''),
            'platform': platform,
        }
    )

    protocols = set()
    for protocol in result.get('protocols', []):
        assert protocol != ""
        if protocol == 'friendica':
            protocol = 'dfrn'
        elif protocol == 'gnusocial':
            protocol = 'ostatus'
        proto, _created = Protocol.objects.get_or_create(name=protocol)
        protocols.add(proto)
    node.protocols.set(protocols)
    services = set()
    for service in result.get('services', []):
        assert service != ""
        serv, _created = Service.objects.get_or_create(name=service)
        services.add(serv)
    node.services.set(services)

    activity = result.get('activity', {})
    users = activity.get('users', {})
    if any([users.get('total'), users.get('half_year'), users.get('monthly'), users.get('weekly'),
            activity.get('local_posts'), activity.get('local_comments')]):
        Stat.objects.update_or_create(
            node=node,
            date=now().date(),
            defaults={
                # TODO should we guess some missing stats, like guess weekly from monthly
                # or monthly from weekly?
                'users_total': users.get('total'),
                'users_half_year': users.get('half_year'),
                'users_monthly': users.get('monthly'),
                'users_weekly': users.get('weekly'),
                'local_posts': activity.get('local_posts'),
                'local_comments': activity.get('local_comments'),
            },
        )

    logger.info(f'Updated {host} successfully.')
    return True


def poll_nodes():
    logger.info(f'Queueing polling all nodes.')
    nodes_qs = Node.objects.only('host').active()
    for node in nodes_qs:
        poll_node.delay(node.host)
