from whatsmyip.providers import IpProvider


def get_ip(provider: IpProvider) -> str:
    ip = provider.fetch()
    return ip
