"""hg-setup package"""

import os
import sys

from importlib.resources import files
from pathlib import Path

import rich_click as click


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def main():
    """Setup Mercurial and modify its configuration files"""


@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("-n", "--name", help="user name", default=None)
@click.option("-e", "--email", help="email address", default=None)
def init(name, email):
    """Initialize Mercurial configuration file"""
    print(f"Not implemented, {name = }, {email = }")


@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("-l", "--local", is_flag=True, help="edit repository config")
def config(local):
    """UI to edit Mercurial configuration files"""

    print("Not implemented")
    print(f"{local = }")


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
@click.option("--share-dir", help="share dir", default=None)
def init_shell_completion(name, share_dir):
    """init shell completion for a specific shell

    Examples:

      hg-setup init-shell-completion bash
      hg-setup init-shell-completion zsh

    """
    supported_shells = ["bash", "zsh"]

    if name not in supported_shells:
        str_shells = ". ".join(supported_shells)
        click.echo(f"'{name}' not in supported shells ({str_shells}).")
        sys.exit(1)

    text = files("hg_setup.data").joinpath(f"{name}_completion").read_text()

    if share_dir is None:
        try:
            share_dir = Path(os.environ["XDG_DATA_HOME"])
        except KeyError:
            share_dir = Path.home() / ".local/share"

    match name:
        case "bash":
            path_dest = share_dir / "bash-completion/completions/hg"
        case "zsh":
            path_dest = share_dir / "zsh/site-functions/_hg"
        case _:
            assert False

    if path_dest.exists():
        print(f"{path_dest} already exists")
        return

    path_dest.parent.mkdir(parents=True, exist_ok=True)
    path_dest.write_text(text)
    print(f"{path_dest} written")
