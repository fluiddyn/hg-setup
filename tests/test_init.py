import os

from click.testing import CliRunner

from hg_setup import main


def test_auto_with_options(tmp_path):
    """test hg-setup init --auto with --name and --email options"""

    tmp_dir = tmp_path / "home_test"
    tmp_dir.mkdir()

    env = os.environ.copy()
    env["HOME"] = str(tmp_dir)

    command = ["init", "--name", "toto", "--email", "toto.lastname@me", "--auto"]
    print("\nhg-setup " + " ".join(command))
    runner = CliRunner()
    result = runner.invoke(main, command, env=env)
    assert result.exit_code == 0
    assert result.output.startswith("configuration written in")

    result = runner.invoke(main, command, env=env)
    assert result.exit_code == 0
    assert result.output.endswith("already exists. Nothing to do.\n")
