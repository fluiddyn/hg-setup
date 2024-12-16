import os

from click.testing import CliRunner

from hg_setup import main
from hg_setup import completion
from hg_setup.hgrcs import name_default


def test_auto_with_options(tmp_path):
    """test hg-setup init --auto with --name and --email options"""

    completion.CONSIDER_SYSTEM_PATHS = False

    tmp_dir = tmp_path / "home_test"
    tmp_dir.mkdir()

    env = os.environ.copy()
    name_home_envvar = "HOME" if os.name != "nt" else "UserProfile"
    env[name_home_envvar] = str(tmp_dir)

    runner = CliRunner()

    command = ["init", "--name", "toto", "--email", "toto.lastname@me", "--auto"]
    print("\nhg-setup " + " ".join(command))
    result = runner.invoke(main, command, env=env)
    assert result.exit_code == 0
    assert "configuration written in" in result.output, list(tmp_dir.glob("*"))

    result = runner.invoke(main, command, env=env)
    assert result.exit_code == 0
    assert result.output.endswith("already exists. Nothing to do.\n")

    command = ["init", "-n", "toto", "-e", "toto.lastname@me", "--auto", "--force"]
    result = runner.invoke(main, command, env=env)
    assert result.exit_code == 0
    assert "configuration written in" in result.output

    assert len(list(tmp_dir.glob(name_default + "*"))) == 2
