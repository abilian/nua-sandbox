import pytest
from cleez.testing import CliRunner

from nua_agent.cli import get_cli


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def cli():
    return get_cli()


def test_version(cli, runner):
    result = runner.invoke(cli, "--version")
    assert result.exit_code == 0
    assert "nua-dev" in result.stdout
    assert cli.version in result.stdout
