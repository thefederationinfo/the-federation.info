import re


def clean_hostname(hostname: str) -> str:
    """
    Some basic cleaning of a hostname.
    """
    hostname = hostname.strip().lower()
    # Strip protocol
    hostname = re.sub(r'https?://', '', hostname)
    return hostname


def is_valid_hostname(hostname: str) -> bool:
    """
    Validate is a hostname

    Thanks to https://stackoverflow.com/a/2532344/1489738
    """
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def single_true(iterable):
    """
    Check that iterable has only one truethy value.

    Thanks to: https://stackoverflow.com/a/16801605/1489738
    """
    i = iter(iterable)
    return any(i) and not any(i)
