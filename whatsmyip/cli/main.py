import click
from whatsmyip.ip import get_ip
from whatsmyip.providers import GoogleDnsProvider, ip_providers


@click.command(help='Query for the external IP address')
@click.option('--provider', type=click.Choice(ip_providers.keys()),
              default=GoogleDnsProvider.name,
              help='name of the provider')
def main(provider: str) -> None:
    provider = ip_providers.get(provider)
    ip = get_ip(provider)
    click.echo(ip)
