from click.testing import CliRunner

from hg_setup import main


def test_version():
    """test --version"""
    command = ["--version"]

    runner = CliRunner()
    result = runner.invoke(main, command)

    assert result.exit_code == 0
