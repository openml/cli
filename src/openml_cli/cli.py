"""Main CLI entry point for OpenML."""

import click

from openml_cli import __version__
from openml_cli.commands.flows import flows


@click.group()
@click.version_option(version=__version__, prog_name="openml")
def main():
    """OpenML command-line interface.

    A CLI tool for interacting with the OpenML platform.
    """
    pass


main.add_command(flows)


@main.command()
def version():
    """Display the version of the OpenML CLI."""
    click.echo(f"openml-cli version {__version__}")


if __name__ == "__main__":
    main()
