"""Flows command group for browsing and searching OpenML flows."""

import sys

import click


@click.group()
def flows():
    """Browse and search OpenML flows (models/pipelines).

    Flows represent machine learning models and pipelines registered
    on the OpenML platform.
    """
    pass


@flows.command("list")
@click.option("--offset", type=int, default=None, help="Number of flows to skip.")
@click.option("--size", type=int, default=None, help="Maximum number of flows to return.")
@click.option("--tag", type=str, default=None, help="Filter flows by tag.")
@click.option("--uploader", type=str, default=None, help="Filter flows by uploader ID.")
@click.option(
    "--output", type=click.Choice(["table", "plain"]), default="plain",
    help="Output format.",
)
def flows_list(offset, size, tag, uploader, output):
    """List flows available on OpenML."""
    import openml

    try:
        df = openml.flows.list_flows(
            offset=offset, size=size, tag=tag, uploader=uploader,
        )
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if df.empty:
        click.echo("No flows found.")
        return

    if output == "table":
        click.echo(f"\nFound {len(df)} flow(s):\n")
        click.echo(df.to_string(index=False))
    else:
        click.echo(f"\nFound {len(df)} flow(s):\n")
        for _, row in df.iterrows():
            click.echo(
                f"  {row['id']:>6}  {row['name']:<40}  v{row['version']}"
            )


@flows.command("info")
@click.argument("flow_id", type=int)
def flows_info(flow_id):
    """Show detailed information about a specific flow."""
    import openml

    try:
        flow = openml.flows.get_flow(flow_id)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Flow ID     : {flow.flow_id}")
    click.echo(f"Name        : {flow.name}")
    click.echo(f"Version     : {flow.version}")
    click.echo(f"Description : {flow.description or 'N/A'}")
    click.echo(f"Uploader    : {flow.uploader}")
    click.echo(f"Upload date : {flow.upload_date or 'N/A'}")

    if flow.parameters:
        click.echo(f"\nParameters ({len(flow.parameters)}):")
        for name, value in flow.parameters.items():
            click.echo(f"  {name}: {value}")

    if flow.tags:
        click.echo(f"\nTags: {', '.join(flow.tags)}")

