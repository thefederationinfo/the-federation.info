"""Backwards-compatibility shim.

Job payloads already sitting in redis reference functions by their dotted
path under thefederation.tasks, and so do old rq-scheduler entries. Keep
the names importable here; new code should import from thefederation.crawler
and thefederation.aggregation directly.
"""

from thefederation.aggregation import aggregate_daily_stats, clean_duplicate_nodes  # noqa: F401
from thefederation.crawler import (  # noqa: F401
    fetch_node,
    fetch_using_method,
    fill_country_information,
    poll_node,
    poll_nodes,
)
