from click.testing import CliRunner

from hg_setup import main


def test_with_options():
    """test hg-setup init with --name and --email options"""
    command = ["init", "--name", "toto", "--email", "toto.lastname@me"]
    runner = CliRunner()
    result = runner.invoke(main, command)

    assert result.exit_code == 0
