import csv
import json
import sys
import time
import uuid
from pathlib import Path

import click
from labelbox import Client, IAMIntegration

from ..utils import read_json_file, write_json_file


@click.group()
def dataset():
    """
    Commands for interacting with Datasets in the workspace.
    """
    pass


@dataset.command("get")
@click.argument("dataset_id", nargs=1)
@click.pass_obj
def get_dataset_by_id(client: Client, dataset_id: str):
    """
    Get Dataset by ID.
    """
    dataset = client.get_dataset(dataset_id)
    click.echo(dataset)
    sys.exit(0)


@dataset.command("create")
@click.option("--name", "--n", help="Dataset name.", required=True)
@click.option("--desc", "--d", default="", help="Dataset description.")
@click.option(
    "--iam",
    default=IAMIntegration._DEFAULT,
    help="IAM integration, provides default if none is given.",
)
@click.pass_obj
def create_new_dataset(client: Client, name: str, desc: str, iam: str):
    """
    Creates new empty Dataset in the Catalog.
    """
    dataset = client.create_dataset(name=name, description=desc, iam_integration=iam)
    click.echo("New dataset has been created.")
    click.echo(dataset)
    sys.exit(0)


@dataset.command("delete")
@click.argument("dataset_id", nargs=1)
@click.pass_obj
def delete_dataset(client: Client, dataset_id: str):
    """
    Deletes Dataset by ID.
    """
    dataset = client.get_dataset(dataset_id)
    dataset.delete()
    click.echo("Dataset has been deleted.")
    sys.exit(0)


@dataset.command("append")
@click.option(
    "--dataset-id", "--di", required=True, help="Dataset ID to which append rows."
)
@click.option(
    "--rows",
    "--r",
    default="",
    help='List of comma separated URLs. Ex: "rowUrl1.png,rowUrl2.png"',
)
@click.option(
    "--global-keys",
    "--gk",
    default="",
    help="List of comma separated global keys. In same order as URLs. By default random UUID assigned as global key.",
)
@click.option(
    "--local-file",
    "--f",
    default="",
    type=click.Path(),
    help="Path to the local file for upload.",
)
@click.option(
    "--json",
    "json_file",
    default="",
    type=click.Path(),
    help="Path to the JSON file. For supported format see official docs.",
)
@click.option(
    "--csv",
    "csv_file",
    default="",
    type=click.Path(),
    help="Path to the CSV file. For supported format see GitHub page.",
)
@click.pass_obj
def add_data_rows(
    client: Client,
    dataset_id: str,
    rows: str,
    global_keys: str,
    local_file: Path,
    json_file: Path,
    csv_file: Path,
):
    """
    Add data rows to a selected Dataset.
    """
    dataset = client.get_dataset(dataset_id)
    upload_task = None
    assets = []

    if rows != "":
        urls = rows.split(",")
        keys = []

        if global_keys == "":
            keys = [str(uuid.uuid4()) for _ in range(len(urls))]
        else:
            keys = global_keys.split(",")

        urls_keys_pairs = list(zip(urls, keys))
        assets = [
            {"row_data": pair[0], "global_key": pair[1]} for pair in urls_keys_pairs
        ]

    if local_file:
        file_url = client.upload_file(str(local_file))

        if global_keys == "":
            assets = [{"row_data": file_url, "global_key": str(uuid.uuid4())}]
        else:
            assets = [{"row_data": file_url, "global_key": global_keys.strip()}]

    if json_file:
        assets = read_json_file(json_file)

    if csv_file:
        with open(csv_file, "r") as f:
            assets = list(csv.DictReader(f))

    upload_task = dataset.create_data_rows(assets)
    upload_task.wait_till_done()  # type: ignore

    if errs := upload_task.errors:  # type: ignore
        click.echo(errs)
        sys.exit(1)

    click.echo("Assets have been uploaded.")
    sys.exit(0)


@dataset.command("export")
@click.argument("dataset_id", nargs=1)
@click.option("--attachements", is_flag=True, show_default=True)
@click.option("--metadata-fields", is_flag=True, show_default=True)
@click.option("--data-row-details", is_flag=True, show_default=True)
@click.option("--project-details", is_flag=True, show_default=True)
@click.option("--performance-details", is_flag=True, show_default=True)
@click.option(
    "--project-ids",
    "--pi",
    default="",
    help="Comma separated list of Project IDs for which to export data.",
)
@click.option(
    "--model-run-ids",
    "--mi",
    default="",
    help="Comma separated list of Model Run IDs for which to export data.",
)
@click.option(
    "--save",
    "--s",
    is_flag=True,
    default=False,
    show_default=True,
    help="Saves export results into file with the following format: dataset_export_epoch_time.json.",
)
@click.pass_obj
def export_dataset(
    client: Client,
    dataset_id: str,
    attachements: bool,
    metadata_fields: bool,
    data_row_details: bool,
    project_details: bool,
    performance_details: bool,
    project_ids: str,
    model_run_ids: str,
    save: bool,
):
    """
    Exports dataset's information.
    """
    projects = [
        project_id for project_id in project_ids.split(",") if project_ids != ""
    ]
    model_runs = [
        model_run_id for model_run_id in model_run_ids.split(",") if model_run_ids != ""
    ]

    export_params = {
        "attachments": attachements,
        "metadata_fields": metadata_fields,
        "data_row_details": data_row_details,
        "project_details": project_details,
        "performance_details": performance_details,
    }

    if len(projects) > 0:
        export_params["project_ids"] = projects  # type: ignore

    if len(model_runs) > 0:
        export_params["model_runs_ids"] = model_runs  # type: ignore

    dataset = client.get_dataset(dataset_id)
    export_task = dataset.export_v2(params=export_params)  # type: ignore
    export_task.wait_till_done()

    if err := export_task.errors:
        click.echo(err)
        sys.exit(1)

    if save:
        filename = Path.home() / "Desktop" / f"dataset_export_{int(time.time())}.json"
        write_json_file(filename, export_task.result)
        click.echo(f"Dataset's export results were saved into {filename}.")
    else:
        click.echo(f"Dataset {dataset_id} export results:\n")
        click.echo(json.dumps(export_task.result, indent=2))
        sys.exit(1)

    sys.exit(0)


@dataset.command("update")
@click.argument("dataset_id", nargs=1)
@click.argument("name", nargs=1)
@click.pass_obj
def update_dataset_name(client: Client, dataset_id: str, name: str):
    """
    Updates dataset name.
    """
    dataset = client.get_dataset(dataset_id)
    dataset.update(name=name)
    click.echo("Dataset name has been updated.")
    sys.exit(0)
