from unittest.mock import MagicMock
from whatsmyip.providers import IpProvider
from whatsmyip.ip import get_ip


def test_get_ip():
    provider = IpProvider
    provider.fetch = MagicMock(return_value='240.0.0.0')
    get_ip(provider)
    assert provider.fetch.called
