import os
import pytest
from unittest import mock
from click.testing import CliRunner
from whatsmyip.cli.main import main
from whatsmyip.providers import GoogleDnsProvider, ip_providers


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    with open(
            os.path.join(os.path.dirname(__file__),
                         'data',
                         'stdout_help.txt'),
            mode='r') as f:
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert result.output == f.read()


@pytest.mark.parametrize(
    'provider_name,provider_class',
    [(p_name, p_class) for p_name, p_class in ip_providers.items()]
    + [('', GoogleDnsProvider)])
def test_running_with_all_providers(runner, provider_name, provider_class):
    with mock.patch('whatsmyip.cli.main.get_ip') as get_ip_mock:
        get_ip_mock.return_value = '240.0.0.0'

        args = ['--provider', provider_name] if provider_name else []
        result = runner.invoke(main, args)

        assert result.exit_code == 0
        assert result.output == '240.0.0.0' + '\n'
        assert str(provider_class) == str(get_ip_mock.call_args[0][0])
