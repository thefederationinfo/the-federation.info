import random

import datetime
import logging

from django.core.management import call_command
from django.db.models import Sum
from django.utils.timezone import now
from django_rq import job
from federation.hostmeta import fetchers
from federation.utils.network import fetch_host_ip_and_country

from thefederation.enums import Relay
from thefederation.models import Node, Platform, Protocol, Service, Stat

logger = logging.getLogger(__name__)

METHODS = ['nodeinfo2', 'nodeinfo', 'mastodon', 'statisticsjson']


def aggregate_daily_stats(date=None):
    if not date:
        date = now().date()
    # Do all platforms, protocols and then global
    totals = {
        'users_total': 0,
        'users_half_year': 0,
        'users_monthly': 0,
        'users_weekly': 0,
        'local_posts': 0,
        'local_comments': 0,
    }
    for platform in Platform.objects.all():
        stats = Stat.objects.exclude(
            node__last_success__lt=now() - datetime.timedelta(days=30)
        ).filter(
            node__platform=platform,
            date=date,
        ).aggregate(
            users_total=Sum('users_total'),
            users_half_year=Sum('users_half_year'),
            users_monthly=Sum('users_monthly'),
            users_weekly=Sum('users_weekly'),
            local_posts=Sum('local_posts'),
            local_comments=Sum('local_comments'),
        )
        Stat.objects.update_or_create(
            date=date, protocol=None, platform=platform, node=None, defaults=stats,
        )
        # Increment globals
        for key in totals:
            totals[key] += stats[key] if stats[key] else 0
    for protocol in Protocol.objects.all():
        stats = Stat.objects.exclude(
            node__last_success__lt=now() - datetime.timedelta(days=30)
        ).filter(
            node__protocols=protocol,
            date=date,
        ).aggregate(
            users_total=Sum('users_total'),
            users_half_year=Sum('users_half_year'),
            users_monthly=Sum('users_monthly'),
            users_weekly=Sum('users_weekly'),
            local_posts=Sum('local_posts'),
            local_comments=Sum('local_comments'),
        )
        Stat.objects.update_or_create(
            date=date, protocol=protocol, platform=None, node=None, defaults=stats,
        )
    # Add global stat
    Stat.objects.update_or_create(date=date, protocol=None, platform=None, node=None, defaults=totals)


def clean_duplicate_nodes():
    """
    Call the clean dupe nodes command.
    """
    call_command('clean_dupe_nodes')
    # Also re-aggregate stats from a few days
    for single_date in (now().date() - datetime.timedelta(n) for n in range(2)):
        aggregate_daily_stats(single_date)


def fetch_using_method(host, method):
    if method is None:
        return
    logger.debug(f'Fetching {host} using method {method}')
    func = getattr(fetchers, f"fetch_{method}_document")
    return func(host)


def fetch_node(host):
    """
    Fetch different documents in order

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
        if node.preferred_method:
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

    if not node.ip or not node.country:
        node.ip, node.country = fetch_host_ip_and_country(node.host)
        node.save(update_fields=['ip', 'country'])
    else:
        # Refresh periodically
        if random.randint(1, 100) < 50:
            ip, country = fetch_host_ip_and_country(node.host)
            if ip and country and (ip != node.ip or country != node.country.code):
                node.ip = ip
                node.country = country
                node.save(update_fields=['ip', 'country'])

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
    Stat.objects.update_or_create(
        node=node,
        date=now().date(),
        defaults={
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
