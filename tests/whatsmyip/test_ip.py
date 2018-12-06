from whatsmyip.providers import IpProvider
from whatsmyip.ip import get_ip
from unittest import mock


@mock.patch('whatsmyip.providers.IpProvider.fetch', return_value='240.0.0.0')
def test_get_ip(mocked_fetch):
    provider = IpProvider
    get_ip(provider)
    assert provider.fetch.called is True
