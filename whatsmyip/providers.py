import dns.resolver
import requests


class GoogleDnsProvider:
    name = 'google-dns'

    def fetch():
        r = dns.resolver.query('ns1.google.com')
        ns_ip = r[0].address

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [ns_ip]

        qr = resolver.query('o-o.myaddr.l.google.com', 'TXT')

        ip = qr.response.answer[0][0].to_text()
        ip = ip.replace('"', '')
        return ip


class HttpbinProvider:
    name = 'httpbin'

    def fetch():
        r = requests.get(url='https://httpbin.org/ip',
                         headers=dict(Accept='application/json'))
        ip = r.json()['origin']
        return ip


ip_providers = {GoogleDnsProvider.name: GoogleDnsProvider,
                HttpbinProvider.name: HttpbinProvider}
