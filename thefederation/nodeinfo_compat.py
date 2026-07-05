"""Compatibility shim for the ``federation`` library's nodeinfo fetcher.

federation.hostmeta.fetchers.fetch_nodeinfo_document iterates over every link
in /.well-known/nodeinfo and does ``float(link['rel'].split('/')[-1])`` to find
the schema version. PeerTube (and some other software) advertise an extra
ActivityPub link such as ``https://www.w3.org/ns/activitystreams#Application``
in the same document, whose rel is not a versioned nodeinfo schema URL. The
unguarded float() then raises::

    ValueError: could not convert string to float: 'activitystreams#Application'

which aborts the whole fetch, so those nodes can never be polled.

This shim reinstalls the same logic but skips rels that do not parse as a
version number. It should be removed once the upstream fix is released.
"""

import json

from federation.hostmeta import fetchers
from federation.hostmeta.fetchers import (
    HIGHEST_SUPPORTED_NODEINFO_VERSION,
    fetch_document,
    parse_nodeinfo_document,
)


def fetch_nodeinfo_document(host):
    doc, status_code, error = fetch_document(host=host, path="/.well-known/nodeinfo")
    if not doc:
        return
    try:
        doc = json.loads(doc)
    except json.JSONDecodeError:
        return

    url, highest_version = "", 0.0

    if doc.get("0"):
        # Buggy NodeInfo from certain old Hubzilla versions
        url = doc.get("0", {}).get("href")
    elif isinstance(doc.get("links"), dict):
        # Another buggy NodeInfo from certain old Hubzilla versions
        url = doc.get("links").get("href")
    else:
        for link in doc.get("links") or []:
            rel = link.get("rel") or ""
            try:
                version = float(rel.split("/")[-1])
            except (TypeError, ValueError):
                # Not a versioned nodeinfo schema rel (e.g. PeerTube's
                # activitystreams#Application link); skip instead of crashing.
                continue
            if highest_version < version <= HIGHEST_SUPPORTED_NODEINFO_VERSION:
                url, highest_version = link.get("href"), version

    if not url:
        return

    doc, status_code, error = fetch_document(url=url)
    if not doc:
        return
    try:
        doc = json.loads(doc)
    except json.JSONDecodeError:
        return
    return parse_nodeinfo_document(doc, host)


def apply():
    """Monkeypatch the federation library's nodeinfo fetcher in place."""
    fetchers.fetch_nodeinfo_document = fetch_nodeinfo_document
