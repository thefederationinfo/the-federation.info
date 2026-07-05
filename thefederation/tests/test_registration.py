from unittest.mock import patch

from django.core.cache import cache
from test_plus import TestCase

from thefederation import registration
from thefederation.utils import clean_hostname


@patch("thefederation.registration.poll_node")
class RegisterNodeTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def test_valid_host_is_queued(self, mock_poll):
        result, host = registration.register_node("Example.COM")
        assert result == registration.OK
        assert host == "example.com"
        mock_poll.delay.assert_called_once_with("example.com")

    def test_invalid_host_is_rejected(self, mock_poll):
        result, _host = registration.register_node("not a hostname")
        assert result == registration.INVALID
        mock_poll.delay.assert_not_called()

    def test_same_host_is_rate_limited(self, mock_poll):
        result, _host = registration.register_node("example.com")
        assert result == registration.OK
        result, _host = registration.register_node("example.com")
        assert result == registration.RATE_LIMITED
        assert mock_poll.delay.call_count == 1

    def test_ip_is_rate_limited(self, mock_poll):
        for i in range(registration.IP_LIMIT):
            result, _host = registration.register_node(f"node{i}.example.com", client_ip="10.0.0.1")
            assert result == registration.OK
        result, _host = registration.register_node("one-too-many.example.com", client_ip="10.0.0.1")
        assert result == registration.RATE_LIMITED
        # another caller is unaffected
        result, _host = registration.register_node("other-caller.example.com", client_ip="10.0.0.2")
        assert result == registration.OK


class CleanHostnamePunycodeTestCase(TestCase):
    def test_unicode_hostname_is_punycoded(self):
        assert clean_hostname("bücher.example") == "xn--bcher-kva.example"

    def test_ascii_hostname_is_untouched(self):
        assert clean_hostname("https://Example.com ") == "example.com"
