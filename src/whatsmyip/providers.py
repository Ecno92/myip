from typing import Dict

import dns.resolver  # type: ignore
import requests


class IpProvider(type):
    name: str

    @staticmethod
    def fetch() -> str:
        raise NotImplementedError


class GoogleDnsProvider(metaclass=IpProvider):
    name = 'google-dns'

    @staticmethod
    def fetch():
        resolver = dns.resolver.Resolver(configure=True)

        resp = resolver.query('ns1.google.com')

        ns_ip = resp[0].to_text()
        resolver.nameservers = [ns_ip]

        resp_two = resolver.query('o-o.myaddr.l.google.com', 'TXT')
        ip = resp_two[0].to_text()
        ip = ip.replace('"', '')
        return ip


class CloudflareDnsProvider(metaclass=IpProvider):
    name = 'cloudflare-dns'

    @staticmethod
    def fetch():
        resolver = dns.resolver.Resolver(configure=True)

        r = resolver.query('ns1.cloudflare.com')

        ns_ip = r[0].address
        resolver.nameservers = [ns_ip]

        resp_two = resolver.query('whoami.cloudflare.com', 'TXT')
        ip = resp_two[0].to_text()
        ip = ip.replace('"', '')
        return ip


class CloudflareHttpProvider(metaclass=IpProvider):
    name = 'cloudflare-http'

    @staticmethod
    def fetch():
        r = requests.get(url='https://cloudflare.com/cdn-cgi/trace')
        for line in r.text.split("\n"):
            k, v = line.split('=')
            if k == 'ip':
                return v


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
