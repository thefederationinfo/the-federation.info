"""Crawler concern: fetch nodeinfo from remote nodes and store results.

Maps to the cRawler service (Worker + QueueManager store side) in the
next-generation architecture at https://codeberg.org/thefederationinfo/next
"""

import logging

import geoip2.database
from django.conf import settings
from django.db import transaction
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

METHODS = ["nodeinfo", "nodeinfo2", "matrix"]


def fetch_using_method(host, method):
    if method is None:
        return
    logger.debug(f"Fetching {host} using method {method}")
    func = getattr(fetchers, f"fetch_{method}_document", None)
    if func is None:
        # Platform.get_method can name methods (e.g. "mastodon") that a
        # given federation library version may not ship a fetcher for.
        # Treat that like a failed method instead of crashing the job.
        logger.warning("No fetcher for method %s (host %s)", method, host)
        return None
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
    Try each fetch method in order, first hit wins.

    Always works the same for every node; per-platform preferred methods
    were dropped for simplicity, matching the next-generation crawler.

    :param host: str
    :return: dict
    """
    for method in METHODS:
        result = fetch_using_method(host, method)
        if result:
            return result


def fill_country_information():
    logger.info("Updating country and IP information for all nodes.")
    ipdb = geoip2.database.Reader(settings.MAXMIND_DB_PATH)
    updates = 0
    # Node.save() reads name, version and platform.name; with only() those
    # were deferred, costing three extra SELECTs per saved node. Fetch the
    # full row plus platform in the single initial query instead.
    for node in Node.objects.select_related("platform").active().iterator():
        try:
            save = False
            ip = fetch_host_ip(node.host)
            if node.ip != ip:
                node.ip = ip
                save = True
            if ip:
                response = ipdb.country(ip)
                new_country = (response.country.iso_code or "") if response.country else ""
                # Compare before assigning: the old code marked nodes whose
                # country stayed unresolved ('' -> '') as changed, rewriting
                # every such node on every run.
                if response.country and (node.country.code or "") != new_country:
                    node.country = new_country
                    save = True
            if save:
                node.save()
                updates += 1
        except Exception as ex:
            logger.warning(f"Error trying to fill country info: {ex}")
    logger.info(f"Update of country and IP information done, updated {updates} nodes.")


@job("medium", result_ttl=0)
def poll_node(host):
    logger.info(f"Start processing {host}")
    result = fetch_node(host)
    if not result:
        logger.info(f"No result for {host}.")
        return False

    if host != result.get("host"):
        # A parser attributing the result to a different host (redirects,
        # aliases) must not crash the job, and storing it under the wrong
        # host would create duplicate nodes.
        logger.warning("Fetch for %s returned data for %s, discarding.", host, result.get("host"))
        return False
    # A poll causes several small writes (node, m2m links, stat). Without an
    # explicit transaction each one autocommits separately, forcing Postgres
    # to fsync its WAL per statement. One atomic block per poll collapses
    # that to a single commit, which matters a lot with many concurrent
    # rqworkers hammering the same disk.
    with transaction.atomic():
        return _store_poll_result(host, result)


def _store_poll_result(host, result):
    activity = result.get("activity", {})
    users = activity.get("users", {})

    # check bounds for Django's PositiveIntegerField before touching the
    # database, so a node with broken stats costs zero writes per poll
    # instead of a node update that gets thrown away anyway
    metrics = [
        ("total", users),
        ("half_year", users),
        ("monthly", users),
        ("weekly", users),
        ("local_posts", activity),
        ("local_comments", activity),
    ]
    for metric, source in metrics:
        value = source.get(metric)
        if value and (value > 2147483647 or value < 0):
            logger.info(f"Updated {host} failed out of range value for {metric}")
            return False

    platform, _created = Platform.objects.get_or_create(name=result["platform"])
    node, _created = Node.objects.update_or_create(
        host=host,
        defaults={
            "features": result.get("features", {}),
            "last_success": now(),
            "name": result.get("name") or host,
            "open_signups": result.get("open_signups", False),
            "organization_account": result.get("organization", {}).get("account", ""),
            "organization_contact": result.get("organization", {}).get("contact", ""),
            "organization_name": result.get("organization", {}).get("name", ""),
            "relay": result.get("relay") or Relay.NONE,
            "server_meta": result.get("server_meta", {}),
            "version": result.get("version", ""),
            "platform": platform,
        },
    )

    protocols = set()
    for protocol in result.get("protocols", []):
        if not protocol:
            # An empty entry in a remote document must not abort the poll,
            # and asserts vanish under python -O anyway.
            continue
        if protocol == "friendica":
            protocol = "dfrn"
        elif protocol == "gnusocial":
            protocol = "ostatus"
        proto, _created = Protocol.objects.get_or_create(name=protocol)
        protocols.add(proto)
    node.protocols.set(protocols)
    services = set()
    for service in result.get("services", []):
        if not service:
            continue
        serv, _created = Service.objects.get_or_create(name=service)
        services.add(serv)
    node.services.set(services)

    stat_values = {
        "users_total": users.get("total"),
        "users_half_year": users.get("half_year"),
        "users_monthly": users.get("monthly"),
        "users_weekly": users.get("weekly"),
        "local_posts": activity.get("local_posts"),
        "local_comments": activity.get("local_comments"),
    }
    stat, created = Stat.objects.get_or_create(
        node=node,
        date=now().date(),
        defaults=stat_values,
    )
    if not created and any(getattr(stat, key) != value for key, value in stat_values.items()):
        # update_or_create would UPDATE unconditionally, turning every
        # repeat poll of the day into a disk write even when nothing
        # changed. Only write when a value actually differs.
        for key, value in stat_values.items():
            setattr(stat, key, value)
        stat.save(update_fields=list(stat_values))

    logger.info(f"Updated {host} successfully.")
    return True


def poll_nodes(skip=0):
    logger.info(f"Queueing polling all nodes (skipping {skip}).")
    # values_list + iterator: only host strings, no Node instances. The
    # slice becomes a SQL OFFSET instead of counting rows down by hand.
    hosts = Node.objects.pollable().values_list("host", flat=True)
    queued = 0
    for host in hosts[skip:].iterator():
        poll_node.delay(host)
        queued += 1
    logger.info(f"Queued {queued} nodes for polling.")
