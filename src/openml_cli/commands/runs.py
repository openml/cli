"""Runs command group for browsing OpenML runs."""

import sys

import click


@click.group()
def runs():
    """Browse OpenML runs.

    Runs represent the execution of a flow (model) on a task,
    producing evaluation results and predictions.
    """
    pass


@runs.command("list")
@click.option("--offset", type=int, default=None, help="Number of runs to skip.")
@click.option("--size", type=int, default=None, help="Maximum number of runs to return.")
@click.option("--id", "run_ids", type=str, default=None, help="Comma-separated run IDs.")
@click.option("--task", "task_ids", type=str, default=None, help="Comma-separated task IDs.")
@click.option("--flow", "flow_ids", type=str, default=None, help="Comma-separated flow IDs.")
@click.option("--uploader", "uploader_ids", type=str, default=None, help="Comma-separated uploader IDs.")
@click.option("--tag", type=str, default=None, help="Filter runs by tag.")
@click.option("--study", type=int, default=None, help="Filter by study ID.")
@click.option(
    "--output", type=click.Choice(["table", "plain"]), default="plain",
    help="Output format.",
)
def runs_list(offset, size, run_ids, task_ids, flow_ids, uploader_ids, tag, study, output):
    """List runs available on OpenML."""
    import openml

    def parse_ids(raw):
        if raw is None:
            return None
        return [int(x.strip()) for x in raw.split(",")]

    try:
        df = openml.runs.list_runs(
            offset=offset, size=size,
            id=parse_ids(run_ids),
            task=parse_ids(task_ids),
            flow=parse_ids(flow_ids),
            uploader=parse_ids(uploader_ids),
            tag=tag, study=study,
        )
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if df.empty:
        click.echo("No runs found.")
        return

    if output == "table":
        click.echo(f"\nFound {len(df)} run(s):\n")
        click.echo(df.to_string(index=False))
    else:
        click.echo(f"\nFound {len(df)} run(s):\n")
        for _, row in df.iterrows():
            rid = row.get("run_id", "?")
            tid = row.get("task_id", "?")
            fid = row.get("flow_id", "?")
            click.echo(
                f"  run {rid:>6}  task {tid:>6}  flow {fid:>6}"
            )


@runs.command("info")
@click.argument("run_id", type=int)
def runs_info(run_id):
    """Show detailed information about a specific run."""
    import openml

    try:
        run = openml.runs.get_run(run_id)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Run ID     : {run.run_id}")
    click.echo(f"Task ID    : {run.task_id}")
    click.echo(f"Flow ID    : {run.flow_id}")
    click.echo(f"Flow name  : {run.flow_name}")
    click.echo(f"Setup ID   : {run.setup_id}")
    click.echo(f"Uploader   : {run.uploader}")

    if hasattr(run, "evaluations") and run.evaluations:
        click.echo(f"\nEvaluations ({len(run.evaluations)}):")
        for metric, value in sorted(run.evaluations.items()):
            click.echo(f"  {metric}: {value}")

    if hasattr(run, "tags") and run.tags:
        click.echo(f"\nTags: {', '.join(run.tags)}")
