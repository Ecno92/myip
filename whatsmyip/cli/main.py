import dns.resolver


def main():
    answer = dns.resolver.query('ns1.google.com')
    ns_ip = answer[0].address

    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [ns_ip]

    q_result = resolver.query('o-o.myaddr.l.google.com', 'TXT')
    my_ip = q_result.response.answer[0][0].to_text()
    my_ip = my_ip.replace('"', '')
    print(my_ip)