import pytest
import inspect
import responses
from unittest import mock
import whatsmyip.providers as providers
from dns.rdtypes.IN.A import A
from dns.rdtypes.ANY.TXT import TXT


@pytest.fixture()
def dns_ns_query_response():
    answer = []
    answer.append(
        A(1, 1, '216.239.32.10')
    )
    return answer


@pytest.fixture()
def dns_ip_query_response():
    answer = []
    answer.append(
        TXT(1, 16, [b'240.0.0.0'])
    )
    return answer


def test_base_ip_provider():
    with pytest.raises(NotImplementedError):
        provider = providers.IpProvider
        provider.fetch()


@mock.patch('dns.resolver.Resolver.query')
@pytest.mark.parametrize(
    'provider',
    [
        (providers.GoogleDnsProvider),
        (providers.CloudflareDnsProvider)
    ]
)
def test_dns_providers(
    mock_query, provider, dns_ns_query_response, dns_ip_query_response
):
    mock_query.side_effect = [dns_ns_query_response,
                              dns_ip_query_response]
    ip = provider.fetch()
    assert ip == '240.0.0.0'


@responses.activate
def test_cloudflare_provider():
    responses.add(responses.GET, 'https://cloudflare.com/cdn-cgi/trace',
                  body="""
fl=100000
h=www.cloudflare.com
ip=240.0.0.0
visit_scheme=https
uag=python-requests/2.20.1
colo=AMS
spdy=off
http=http/1.1
loc=NL
tls=TLSv1.2
sni=plaintext

""",
                  status=200)
    provider = providers.CloudflareHttpProvider
    provider.fetch()


@responses.activate
def test_httpbin_provider():
    responses.add(responses.GET, 'https://httpbin.org/ip',
                  json={'origin': '240.0.0.0'}, status=200)
    provider = providers.HttpbinProvider
    provider.fetch()


def test_all_providers_in_ip_providers_dict():
    ps = {m[1].name: m[1]
          for m in inspect.getmembers(providers, inspect.isclass)
          if isinstance(m[1], providers.IpProvider)}
    assert ps.keys() == providers.ip_providers.keys()
    for name, klass in ps.items():
        type(providers.ip_providers[name]) is type(klass)
