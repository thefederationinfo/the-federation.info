import logging

from django_rq import job
from federation.hostmeta import fetchers

from thefederation.enums import Relay
from thefederation.models import Node, Platform, Protocol, Service

logger = logging.getLogger(__name__)

METHODS = ['nodeinfo2', 'nodeinfo', 'statisticsjson']


def fetch_using_method(host, method):
    logger.debug(f'Fetching {host} using method {method}')
    func = getattr(fetchers, f"fetch_{method}_document")
    return func(host)


def fetch_server(host):
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
def poll_server(host):
    result = fetch_server(host)
    if not result:
        logger.info(f'No result for {host}, incrementing failure count.')
        Node.log_failure(host)
        return

    assert host == result.get('host')
    platform, _created = Platform.objects.get_or_create(name=result['platform'])
    node, _created = Node.objects.update_or_create(
        host=host,
        defaults={
            'failures': 0,
            'features': result.get('features', {}),
            'ip': result.get('ip'),
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
        proto, _created = Protocol.objects.get_or_create(name=protocol)
        protocols.add(proto)
    node.protocols.set(protocols)
    services = set()
    for service in result.get('services', []):
        assert service != ""
        serv, _created = Service.objects.get_or_create(name=service)
        services.add(serv)
    node.services.set(services)
    logger.info(f'Updated {host} successfully.')


@job('medium')
def poll_servers():
    logger.info(f'Queueing polling all servers.')
    for node in Node.objects.only('host').filter(failures__lte=30):
        poll_server.delay(node.host)
