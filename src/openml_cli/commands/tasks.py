"""Tasks command group for browsing OpenML tasks."""

import sys

import click


@click.group()
def tasks():
    """Browse OpenML tasks.

    Tasks define a specific problem to solve, combining a dataset
    with an evaluation procedure and target feature.
    """
    pass


@tasks.command("list")
@click.option("--offset", type=int, default=None, help="Number of tasks to skip.")
@click.option("--size", type=int, default=None, help="Maximum number of tasks to return.")
@click.option("--tag", type=str, default=None, help="Filter tasks by tag.")
@click.option("--task-type", type=int, default=None, help="Filter by task type ID.")
@click.option("--status", type=str, default=None, help="Filter by status.")
@click.option("--data-name", type=str, default=None, help="Filter by dataset name.")
@click.option("--data-id", type=int, default=None, help="Filter by dataset ID.")
@click.option(
    "--output", type=click.Choice(["table", "plain"]), default="plain",
    help="Output format.",
)
def tasks_list(offset, size, tag, task_type, status, data_name, data_id, output):
    """List tasks available on OpenML."""
    import openml

    kwargs = dict(
        offset=offset, size=size, tag=tag, status=status,
        data_name=data_name, data_id=data_id,
    )
    if task_type is not None:
        kwargs["task_type"] = openml.tasks.TaskType(task_type)

    try:
        df = openml.tasks.list_tasks(**kwargs)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if df.empty:
        click.echo("No tasks found.")
        return

    if output == "table":
        click.echo(f"\nFound {len(df)} task(s):\n")
        click.echo(df.to_string(index=False))
    else:
        click.echo(f"\nFound {len(df)} task(s):\n")
        for _, row in df.iterrows():
            tid = row.get("tid", "?")
            name = row.get("name", "unknown")
            ttype = row.get("task_type", "")
            click.echo(f"  {tid:>6}  {name:<40}  {ttype}")


@tasks.command("info")
@click.argument("task_id", type=int)
def tasks_info(task_id):
    """Show detailed information about a specific task."""
    import openml

    try:
        task = openml.tasks.get_task(task_id, download_data=False)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Task ID    : {task.task_id}")
    click.echo(f"Task type  : {task.task_type}")
    click.echo(f"Dataset ID : {task.dataset_id}")

    target = getattr(task, "target_name", None)
    if target:
        click.echo(f"Target     : {target}")

    estimation = getattr(task, "estimation_procedure_type", None)
    if estimation:
        click.echo(f"Estimation : {estimation}")

    measure = getattr(task, "evaluation_measure", None)
    if measure:
        click.echo(f"Evaluation : {measure}")
