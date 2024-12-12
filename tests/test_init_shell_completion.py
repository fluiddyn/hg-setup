from click.testing import CliRunner

from hg_setup import main

import pytest


@pytest.mark.parametrize("name_shell", ["bash", "zsh"])
def test_simple_bash(tmp_path, name_shell):
    """test hg-setup init-shell-completion"""
    tmp_dir = tmp_path / "local_share"
    tmp_dir.mkdir()

    if name_shell == "bash":
        path_file = tmp_dir / "bash-completion/completions/hg"
    elif name_shell == "zsh":
        path_file = tmp_dir / "zsh/site-functions/_hg"
    else:
        assert False

    command = ["init-shell-completion", name_shell]
    runner = CliRunner()
    env = {"XDG_DATA_HOME": str(tmp_dir)}
    result = runner.invoke(main, command, env=env)
    assert result.output.strip() == f"{path_file} written"

    result = runner.invoke(main, command, env=env)
    assert result.output.strip() == f"{path_file} already exists"

    assert result.exit_code == 0
