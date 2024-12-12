"""hg-setup package"""

import click


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
def generate_shell_completion(name):
    """Generate shell completion code

    Can be used as

      echo 'eval "$(hg-setup generate-shell-completion bash)"' >> ~/.bashrc

    """

    print(f"Not implemented, {name = }")
