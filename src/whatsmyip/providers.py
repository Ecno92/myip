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
        r = dns.resolver.query('ns1.google.com')
        ns_ip = r[0].address

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [ns_ip]

        qr = resolver.query('o-o.myaddr.l.google.com', 'TXT')

        ip = qr.response.answer[0][0].to_text()
        ip = ip.replace('"', '')
        return ip


class CloudflareDnsProvider(metaclass=IpProvider):
    name = 'cloudflare-dns'

    @staticmethod
    def fetch():
        r = dns.resolver.query('ns1.cloudflare.com')
        ns_ip = r[0].address

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [ns_ip]

        qr = resolver.query('whoami.cloudflare.com', 'TXT')

        ip = qr.response.answer[0][0].to_text()
        ip = ip.replace('"', '')
        return ip


class CloudflareHttpProvider(metaclass=IpProvider):
    name = 'cloudflare'

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
