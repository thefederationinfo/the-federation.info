import datetime
import logging

import geoip2.database
from django.conf import settings
from django.core.management import call_command
from django.db import transaction
from django.db.models import Sum
from django.utils.timezone import now
from django_rq import job
from federation.hostmeta import fetchers
from federation.utils.network import fetch_host_ip

from thefederation import nodeinfo_compat
from thefederation.enums import Relay
from thefederation.models import Node, Platform, Protocol, Service, Stat

# Work around a federation-library crash on PeerTube's nodeinfo links.
nodeinfo_compat.apply()

logger = logging.getLogger(__name__)

METHODS = ['nodeinfo2', 'nodeinfo', 'matrix']


@transaction.atomic
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
            node__blocked=False,
            node__hide_from_list=False,
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
            node__hide_from_list=False,
            node__blocked=False,
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
    try:
        return func(host)
    except Exception as ex:
        # A single method failing must not abort the whole fetch. Network
        # errors, malformed remote documents, or the federation library's
        # own validation (e.g. the NodeInfo2 "baseUrl is outside called
        # host" check) should be treated like an empty result so fetch_node
        # falls through to the next method. Many live nodes serve a broken
        # NodeInfo2 document but a perfectly valid NodeInfo one.
        logger.info("Method %s failed for %s: %s", method, host, ex)
        return None


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
        if node.preferred_method and node.preferred_method in methods:
            methods.remove(node.preferred_method)

    # Use remaining methods
    for method in methods:
        result = fetch_using_method(host, method)
        if result:
            return result


def fill_country_information():
    logger.info('Updating country and IP information for all nodes.')
    ipdb = geoip2.database.Reader(settings.MAXMIND_DB_PATH)
    updates = 0
    # Node.save() reads name, version and platform.name; with only() those
    # were deferred, costing three extra SELECTs per saved node. Fetch the
    # full row plus platform in the single initial query instead.
    for node in Node.objects.select_related('platform').active().iterator():
        try:
            save = False
            ip = fetch_host_ip(node.host)
            if node.ip != ip:
                node.ip = ip
                save = True
            if ip:
                response = ipdb.country(ip)
                if response.country and (not node.country or node.country.code != response.country.iso_code):
                    node.country = response.country.iso_code or ''
                    save = True
            if save:
                node.save()
                updates += 1
        except Exception as ex:
            logger.warning(f"Error trying to fill country info: {ex}")
    logger.info(f'Update of country and IP information done, updated {updates} nodes.')


@job('medium')
def poll_node(host):
    logger.info(f'Start processing {host}')
    result = fetch_node(host)
    if not result:
        logger.info(f'No result for {host}.')
        return False

    assert host == result.get('host')
    # A poll causes several small writes (node, m2m links, stat). Without an
    # explicit transaction each one autocommits separately, forcing Postgres
    # to fsync its WAL per statement. One atomic block per poll collapses
    # that to a single commit, which matters a lot with many concurrent
    # rqworkers hammering the same disk.
    with transaction.atomic():
        return _store_poll_result(host, result)


def _store_poll_result(host, result):
    activity = result.get('activity', {})
    users = activity.get('users', {})

    # check bounds for Django's PositiveIntegerField before touching the
    # database, so a node with broken stats costs zero writes per poll
    # instead of a node update that gets thrown away anyway
    metrics = [
        ('total', users),
        ('half_year', users),
        ('monthly', users),
        ('weekly', users),
        ('local_posts', activity),
        ('local_comments', activity),
    ]
    for metric, source in metrics:
        value = source.get(metric)
        if value and (value > 2147483647 or value < 0):
            logger.info(f'Updated {host} failed out of range value for {metric}')
            return False

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

    stat_values = {
        'users_total': users.get('total'),
        'users_half_year': users.get('half_year'),
        'users_monthly': users.get('monthly'),
        'users_weekly': users.get('weekly'),
        'local_posts': activity.get('local_posts'),
        'local_comments': activity.get('local_comments'),
    }
    stat, created = Stat.objects.get_or_create(
        node=node, date=now().date(), defaults=stat_values,
    )
    if not created and any(getattr(stat, key) != value for key, value in stat_values.items()):
        # update_or_create would UPDATE unconditionally, turning every
        # repeat poll of the day into a disk write even when nothing
        # changed. Only write when a value actually differs.
        for key, value in stat_values.items():
            setattr(stat, key, value)
        stat.save(update_fields=list(stat_values))

    logger.info(f'Updated {host} successfully.')
    return True


def poll_nodes(skip = 0):
    logger.info(f'Queueing polling all nodes (skipping {skip}).')
    # values_list + iterator: only host strings, no Node instances, and
    # len() would have materialized the whole queryset in memory
    hosts = Node.objects.active().values_list('host', flat=True)
    total = count = hosts.count()
    for host in hosts.iterator():
        if total - count < skip:
            count -= 1
            continue
        poll_node.delay(host)
        count -= 1
        logger.debug(f'{count} nodes left')
    logger.info(f'Queued {total - skip if total > skip else 0} nodes for polling.')
