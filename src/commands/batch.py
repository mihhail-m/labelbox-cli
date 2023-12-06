import sys

import click
from labelbox import Client


@click.group()
def batch():
    """
    Command for interacting with batches in the projects.
    """
    pass


@batch.command("get")
@click.argument("project_id", nargs=1)
@click.argument("batch_id", nargs=1)
@click.pass_obj
def get_batch(client: Client, project_id: str, batch_id: str):
    """
    Retrieves batch by Project and Batch ID.
    """
    batch = client.get_batch(project_id, batch_id)
    click.echo(batch)
    sys.exit(0)


@batch.command("create")
@click.option(
    "--project-id",
    "--pi",
    required=True,
    help="Project ID for which to create a batch.",
)
@click.option("--name", "--n", required=True, help="Unique batch name.")
@click.option(
    "--rows",
    "--r",
    help='List of comma separated (,) data row ids. Ex: "dataRowId1,dataRowId2".',
)
@click.option("--priority", "--p", default=5, type=int, help="Batch priority.")
@click.option(
    "--file-path",
    "--fp",
    type=click.Path(exists=True),
    help="Text file that contains global keys separated by newlines.",
)
@click.pass_obj
def create_batch(
    client: Client,
    project_id: str,
    name: str,
    rows: str,
    priority: int,
    file_path: click.Path,
):
    """
    Creates a batch for the Benchmark project using global keys.
    """
    project = client.get_project(project_id)
    data_row_ids = []

    if rows and rows.strip():
        data_row_ids = [row.strip() for row in rows.split(",")]

    if file_path:
        with open(str(file_path), "r") as f:
            data_row_ids = [line.strip() for line in f.readlines()]

    batch = project.create_batch(name=name, data_rows=data_row_ids, priority=priority)  # type: ignore
    click.echo(f"New batch has been created. ID: {batch.uid}")
    sys.exit(0)


@batch.command("create-from-dataset")
@click.option(
    "--project-id",
    "--pi",
    required=True,
    help="Project ID for which to create a batch.",
)
@click.option("--name-prefix", "--n", required=True, help="Prefix for batch name.")
@click.option(
    "--dataset-id",
    "--di",
    required=True,
    help="Dataset ID from which to create a batch.",
)
@click.option(
    "--priority", "--p", default=5, help="Batch priority.", show_default=True, type=int
)
@click.pass_obj
def create_batch_from_dataset(
    client: Client, project_id: str, name_prefix: str, dataset_id: str, priority: int
):
    """
    Creates batch from the dataset. Default batch priority is 5.
    Returns empty list when attempt to add the same batch.
    """
    project = client.get_project(project_id)
    batch_task = project.create_batches_from_dataset(name_prefix, dataset_id, priority)
    batch_task.wait_till_done()

    if err := batch_task.errors():
        click.echo(f"There were errors while creating batch: {err}")
        sys.exit(1)

    click.echo("New batch(es) has been created.")
    click.echo(batch_task.result())
    sys.exit(0)


@batch.command("delete")
@click.argument("project_id", nargs=1)
@click.argument("batch_id", nargs=1)
@click.pass_obj
def delete_batch(client: Client, project_id: str, batch_id: str):
    """
    Deletes batch by Project and Batch ID.
    """
    batch = client.get_batch(project_id, batch_id)
    batch.delete()
    click.echo(f"Batch with ID {batch_id} has been deleted.")
    sys.exit(0)


@batch.command("delete-labels")
@click.argument("project_id", nargs=1)
@click.argument("batch_id", nargs=1)
@click.option(
    "--set-as-template",
    is_flag=True,
    default=False,
    show_default=True,
    help="Re-queue the data with labels as templates.",
)
@click.pass_obj
def delete_labels(
    client: Client, project_id: str, batch_id: str, set_as_template: bool
):
    """
    Deletes labels from the batch.
    Provide --set-as-template flag to requeue labels as templates for the future usage.
    """
    batch = client.get_batch(project_id, batch_id)
    batch.delete_labels(set_labels_as_template=set_as_template)
    click.echo(f"Labels has been deleted.")
    sys.exit(0)
