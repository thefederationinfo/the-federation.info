from django_rq import job
from federation.hostmeta import fetchers

from thefederation.enums import Relay
from thefederation.models import Node

METHODS = ['nodeinfo2', 'nodeinfo', 'statisticsjson']


def fetch_using_method(host, method):
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
        methods = METHODS[:].remove(node.preferred_method)

    # Use remaining methods
    for method in methods:
        result = fetch_using_method(host, method)
        if result:
            return result


@job('medium')
def poll_server(host):
    result = fetch_server(host)
    if not result:
        Node.log_failure(host)
        return

    assert host == result.get('host')
    # TODO Platform
    Node.objects.update_or_create(
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
            'relay': result.get('relay', Relay.NONE),
            'server_meta': result.get('server_meta', {}),
            'version': result.get('version', ''),
        }
    )
    # TODO Protocols
    # TODO Services


@job('medium')
def poll_servers():
    for node in Node.objects.only('host').filter(failures__lte=30):
        poll_server.delay(node.host)
