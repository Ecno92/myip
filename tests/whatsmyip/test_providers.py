import pytest
import inspect
import responses
import whatsmyip.providers as providers


@pytest.mark.skip(reason="TODO: Found no cheap testing strategy yet.")
def test_google_dns_provider():
    pass


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
