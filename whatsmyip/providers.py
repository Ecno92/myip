import dns.resolver
import requests


class IpProvider:
    pass


class GoogleDnsProvider(IpProvider):
    name = 'google-dns'

    @staticmethod
    def fetch() -> str:
        r = dns.resolver.query('ns1.google.com')
        ns_ip = r[0].address

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [ns_ip]

        qr = resolver.query('o-o.myaddr.l.google.com', 'TXT')

        ip = qr.response.answer[0][0].to_text()
        ip = ip.replace('"', '')
        return ip


class HttpbinProvider(IpProvider):
    name = 'httpbin'

    @staticmethod
    def fetch() -> str:
        r = requests.get(url='https://httpbin.org/ip',
                         headers=dict(Accept='application/json'))
        ip = r.json()['origin']
        return ip


ip_providers = {GoogleDnsProvider.name: GoogleDnsProvider,
                HttpbinProvider.name: HttpbinProvider}
