"""Datasets command group for browsing and searching OpenML datasets."""

import sys

import click


@click.group()
def datasets():
    """Browse and search OpenML datasets.

    Datasets are the core data resources on the OpenML platform,
    each identified by a unique ID, with metadata, qualities,
    and versioning.
    """
    pass


@datasets.command("list")
@click.option("--offset", type=int, default=None, help="Number of datasets to skip.")
@click.option("--size", type=int, default=None, help="Maximum number of datasets to return.")
@click.option("--tag", type=str, default=None, help="Filter datasets by tag.")
@click.option("--status", type=str, default=None, help="Filter by status (e.g. active).")
@click.option("--name", type=str, default=None, help="Filter by (partial) name.")
@click.option(
    "--output", type=click.Choice(["table", "plain"]), default="plain",
    help="Output format.",
)
def datasets_list(offset, size, tag, status, name, output):
    """List datasets available on OpenML."""
    import openml

    try:
        df = openml.datasets.list_datasets(
            offset=offset, size=size, tag=tag, status=status, data_name=name,
        )
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if df.empty:
        click.echo("No datasets found.")
        return

    if output == "table":
        click.echo(f"\nFound {len(df)} dataset(s):\n")
        click.echo(df.to_string(index=False))
    else:
        click.echo(f"\nFound {len(df)} dataset(s):\n")
        for _, row in df.iterrows():
            did = row.get("did", row.get("id", "?"))
            dname = row.get("name", "unknown")
            dstatus = row.get("status", "")
            click.echo(f"  {did:>6}  {dname:<40}  {dstatus}")

