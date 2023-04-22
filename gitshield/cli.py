import re

import click
from utils import check_for_git, install_git_hook, uninstall_git_hook


@click.group()
def cli():
    pass


@cli.command()
def install():
    """Install the git hook"""
    click.secho("Installing the git hook...", fg="green")
    check_for_git()
    install_git_hook()


@cli.command()
def uninstall():
    """Uninstall the git hook"""
    click.secho("Uninstall the git hook...", fg="green")
    check_for_git()
    uninstall_git_hook()


@cli.command()
@click.option(
    "--changed_file_path",
    type=click.Path(exists=True),
    multiple=True,
    required=True,
    help="Path to the changed file",
)
def pre_commit(changed_file_path):
    """Run on the pre-commit hook"""
    for file in changed_file_path:
        click.secho(f"Checking {file} for secrets...", fg="green")
        with open(file, "r") as f:
            fileString = f.read()
            regex = r"\b\w{2}-\w{2}\b"
            if len(re.findall(regex, fileString)):
                click.secho(
                    f"There are secrets present in {file} secrets - \
                      {re.findall(regex, fileString)}",
                    fg="red",
                )
                import sys

                sys.exit(1)


if __name__ == "__main__":
    cli()