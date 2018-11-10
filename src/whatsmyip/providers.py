from typing import Dict

import dns.resolver  # type: ignore
import requests


class IpProvider(type):
    name: str

    @staticmethod
    def fetch() -> str:
        raise NotImplementedError


def fetch_ip_for_dns_provider(ns_address, query_address):
    resolver = dns.resolver.Resolver(configure=True)

    resp = resolver.query(ns_address)

    ns_ip = resp[0].to_text()
    resolver.nameservers = [ns_ip]

    resp_two = resolver.query(query_address, 'TXT')
    ip = resp_two[0].to_text()
    ip = ip.replace('"', '')
    return ip


class GoogleDnsProvider(metaclass=IpProvider):
    name = 'google-dns'

    @staticmethod
    def fetch():
        ip = fetch_ip_for_dns_provider(
            'ns1.google.com', 'o-o.myaddr.l.google.com')
        return ip


class CloudflareDnsProvider(metaclass=IpProvider):
    name = 'cloudflare-dns'

    @staticmethod
    def fetch():
        ip = fetch_ip_for_dns_provider(
            'ns1.cloudflare.com', 'whoami.cloudflare.com')
        return ip


class CloudflareHttpProvider(metaclass=IpProvider):
    name = 'cloudflare-http'

    @staticmethod
    def fetch():
        r = requests.get(url='https://cloudflare.com/cdn-cgi/trace')
        items = dict(
            item.split('=') for item in filter(None, r.text.split('\n'))
        )
        ip = items['ip']
        return ip


class HttpbinProvider(metaclass=IpProvider):
    name = 'httpbin'

    @staticmethod
    def fetch():
        r = requests.get(url='https://httpbin.org/ip',
                         headers=dict(Accept='application/json'))
        ip = r.json()['origin']
        return ip


ip_providers: Dict[str, IpProvider] = {
    GoogleDnsProvider.name: GoogleDnsProvider,
    HttpbinProvider.name: HttpbinProvider,
    CloudflareDnsProvider.name: CloudflareDnsProvider,
    CloudflareHttpProvider.name: CloudflareHttpProvider}
