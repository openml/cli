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


@datasets.command("info")
@click.argument("dataset_id", type=int)
def datasets_info(dataset_id):
    """Show detailed information about a specific dataset."""
    import openml

    try:
        dataset = openml.datasets.get_dataset(dataset_id, download_data=False)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    fields = [
        ("Dataset ID", dataset.dataset_id),
        ("Name", dataset.name),
        ("Version", dataset.version),
        ("Format", dataset.format),
        ("Creator", dataset.creator),
        ("Licence", getattr(dataset, "licence", None)),
        ("Collected", dataset.collection_date),
    ]
    for label, value in fields:
        if value:
            click.echo(f"{label:<12}: {value}")

    if dataset.description:
        click.echo(f"\nDescription:\n  {dataset.description}")

    if dataset.qualities:
        click.echo(f"\nQualities ({len(dataset.qualities)}):")
        for key, val in sorted(dataset.qualities.items()):
            click.echo(f"  {key}: {val}")


@datasets.command("search")
@click.argument("query")
@click.option("--size", type=int, default=1000, help="Max datasets to search through.")
@click.option("--tag", type=str, default=None, help="Pre-filter by tag.")
def datasets_search(query, size, tag):
    """Search for datasets by name (case-insensitive)."""
    import openml

    try:
        df = openml.datasets.list_datasets(offset=0, size=size, tag=tag)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if df.empty:
        click.echo("No datasets found on the server.")
        return

    query_lower = query.lower()
    name_col = df["name"].astype(str).str.lower()
    matches = df[name_col.str.contains(query_lower, na=False)]

    if matches.empty:
        click.echo(f"No datasets matching '{query}'.")
        return

    click.echo(f"\nFound {len(matches)} dataset(s) matching '{query}':\n")
    for _, row in matches.iterrows():
        did = row.get("did", row.get("id", "?"))
        dname = row.get("name", "unknown")
        dstatus = row.get("status", "")
        click.echo(f"  {did:>6}  {dname:<40}  {dstatus}")
