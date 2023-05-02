from unittest import skip

import pytest
from cleez.testing import CliRunner

from nua_dev.cli import get_cli


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def cli():
    return get_cli()


@skip("FIXME")
def test_version(cli, runner):
    cli.run()

    result = runner.invoke(cli, "--version")
    assert result.exit_code == 0
    assert "Nua CLI version:" in result.stdout


@skip("FIXME")
def test_bad_arg(cli, runner):
    result = runner.invoke(cli, "bad_arg")
    assert result.exit_code != 0


@skip("FIXME")
def test_verbose(cli, runner):
    result = runner.invoke(cli, "--verbose")
    assert result.exit_code != 0

    result = runner.invoke(cli, "-v")
    assert result.exit_code != 0
