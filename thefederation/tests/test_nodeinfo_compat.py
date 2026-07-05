import json
from unittest.mock import patch

from test_plus import TestCase

from thefederation.nodeinfo_compat import fetch_matrix_document

VERSION_DOC = json.dumps({"server": {"name": "Rocket.Chat", "version": "8.7"}})


def _fetch_document(host=None, path=None, url=None):
    """Fake network: rocket.chat delegates federation to open.rocket.chat."""
    if host == "rocket.chat" and path == "/.well-known/matrix/server":
        return json.dumps({"m.server": "open.rocket.chat:443"}), 200, None
    if host == "open.rocket.chat:443" and path == "/_matrix/federation/v1/version":
        return VERSION_DOC, 200, None
    if host == "matrix.org" and path == "/_matrix/federation/v1/version":
        return VERSION_DOC, 200, None
    return None, 404, Exception("not found")


@patch("thefederation.nodeinfo_compat.fetch_document", side_effect=_fetch_document)
@patch("federation.hostmeta.parsers.send_document", return_value=(403, None))
class FetchMatrixDocumentTestCase(TestCase):
    def test_follows_well_known_delegation(self, _send, _fetch):
        result = fetch_matrix_document("rocket.chat")
        # attributed to the original host, not the delegated one
        assert result["host"] == "rocket.chat"
        assert result["platform"] == "matrix|rocket.chat"
        assert result["version"] == "8.7"
        assert result["protocols"] == ["matrix"]

    def test_direct_host_without_delegation(self, _send, _fetch):
        result = fetch_matrix_document("matrix.org")
        assert result["host"] == "matrix.org"
        assert result["version"] == "8.7"

    def test_unreachable_host_returns_none(self, _send, _fetch):
        assert fetch_matrix_document("nothing.invalid") is None
