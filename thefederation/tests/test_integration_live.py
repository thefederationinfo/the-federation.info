"""
Integration tests against live fediverse instances.

These verify the whole poll pipeline (nodeinfo discovery, fetching,
parsing, storing) still works against the real world, not just against
fixtures. They are excluded from the default pytest run (see setup.cfg)
and executed explicitly with:

    pytest -m live

The host list intentionally covers different platforms and nodeinfo
flavours, including PeerTube whose nodeinfo links need the
nodeinfo_compat workaround.
"""

import pytest

from thefederation.models import Node
from thefederation.tasks import poll_node

LIVE_HOSTS = [
    "chaos.social",  # Mastodon, nodeinfo 2.0
    "mobilizon.us",  # Mobilizon, nodeinfo 2.1
    "rocket.chat",  # Matrix, federation delegated via .well-known
    "media.zat.im",  # PeerTube, exercises nodeinfo_compat
]


@pytest.mark.live
@pytest.mark.django_db
@pytest.mark.parametrize("host", LIVE_HOSTS)
def test_poll_live_node(host):
    # RQ queues run with ASYNC=False under test settings, so .delay in
    # production maps to this direct call executing inline.
    assert poll_node(host) is True, f"polling {host} failed"

    node = Node.objects.get(host=host)
    assert node.platform.name, "platform was not detected"
    assert node.last_success is not None
    assert node.stats.filter(date__isnull=False).count() == 1, "no stat row was written"
