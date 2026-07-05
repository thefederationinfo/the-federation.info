"""Registration concern: gatekeeper for adding new nodes.

Maps to the Registrar service in the next-generation architecture at
https://codeberg.org/thefederationinfo/next which works like:

1. reject callers whose IP is over the rate limit
2. reject hosts that were already requested recently
3. hand the host to the crawler

The actual nodeinfo verification happens in the crawler job, the
registrar only validates cheaply and queues.
"""

import logging

from django.core.cache import cache

from thefederation.crawler import poll_node
from thefederation.utils import clean_hostname, is_valid_hostname

logger = logging.getLogger(__name__)

# Mirrors the next-generation Registrar: httprate.LimitByIP(10, 1*time.Minute)
IP_LIMIT = 10
IP_WINDOW = 60
# One register request per host per hour is plenty, the scheduler polls
# known nodes every few hours anyway.
HOST_WINDOW = 60 * 60

OK = "ok"
INVALID = "invalid"
RATE_LIMITED = "rate_limited"


def _over_limit(key, limit, window):
    """Sliding-window-ish counter on the default cache.

    cache.add is atomic on the redis backend used in production; the
    locmem backend used in development is per-process, which is fine
    there.
    """
    if cache.add(key, 1, timeout=window):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        # Key expired between add and incr, this request starts a window.
        return False
    return count > limit


def register_node(host, client_ip=None):
    """Validate a registration request and queue a poll for it.

    Returns one of OK, INVALID or RATE_LIMITED together with the cleaned
    hostname.
    """
    host = clean_hostname(host)
    if not is_valid_hostname(host):
        return INVALID, host

    if client_ip and _over_limit(f"registrar:ip:{client_ip}", IP_LIMIT, IP_WINDOW):
        logger.info("Rate limited registration from %s for %s", client_ip, host)
        return RATE_LIMITED, host

    if _over_limit(f"registrar:host:{host}", 1, HOST_WINDOW):
        logger.info("Host %s was already registered recently", host)
        return RATE_LIMITED, host

    poll_node.delay(host)
    return OK, host
