import json
import sys
import time
from pathlib import Path

import click
from labelbox import Client, MediaType, Project

from ..utils import write_json_file


@click.group()
def projects():
    """
    Command for interacting with Projects in the workspace. Use subcommands for retrieveing necessary data.
    """
    pass


@projects.command()
@click.option(
    "--match_projects",
    required=True,
    help="Match projects with the given name",
    type=str,
)
@click.option(
    "--n", default=10, help="List number of available projects.", show_default=True
)
@click.pass_obj
def list(client: Client, match_projects: str, n: int):
    """
    Lists available projects with matching name.
    By default shows only first 10.
    """
    projects = client.get_projects(where=Project.name == match_projects)

    # Apperantly Click for some reasons cannot convert generators into lists
    # hence this ugly workaround
    for project in projects:
        click.echo(project)

        n -= 1
        if n == 0:
            break


@projects.command()
@click.argument("project_id", nargs=1)
@click.pass_obj
def get(client: Client, project_id: str):
    """
    Retrieves project by ID.
    """
    project = client.get_project(project_id)
    click.echo(project)


@projects.command()
@click.option(
    "--name",
    required=True,
    type=str,
    help="Name for a project. But between double quotes if name contains spaces.",
)
@click.option(
    "--project_type",
    required=True,
    type=str,
    help="Type of the project. Ex: image, video etc.",
)
@click.option(
    "--desc",
    "description",
    default="",
    type=str,
    help="Project description. Default is empty string.",
)
@click.pass_obj
def create(client: Client, name: str, description: str, project_type: str):
    """
    Creates new project.
    """
    media_type = MediaType(project_type.upper())
    project = client.create_project(
        name=name, description=description, media_type=media_type
    )
    click.echo(f"New project has been created: \n{project}")


@projects.command()
@click.argument("project_id", nargs=1)
@click.pass_obj
def delete(client: Client, project_id: str):
    """
    Delete project by ID.
    """
    project = client.get_project(project_id)
    project.delete()
    click.echo(f"Project with ID {project_id} has been deleted.")


@projects.command()
@click.argument("project_id", nargs=1)
@click.option("--attachements", is_flag=True, default=False, show_default=True)
@click.option("--metadata_fields", is_flag=True, default=False, show_default=True)
@click.option("--data_row_details", is_flag=True, default=False, show_default=True)
@click.option("--project_details", is_flag=True, default=False, show_default=True)
@click.option("--performance_details", is_flag=True, default=False, show_default=True)
@click.option(
    "--save",
    is_flag=True,
    default=False,
    show_default=True,
    help="Saves export results into file with the following format: project_export_epoch_time.json.",
)
@click.pass_obj
def export(
    client: Client,
    project_id: str,
    attachements: bool,
    metadata_fields: bool,
    data_row_details: bool,
    project_details: bool,
    performance_details: bool,
    save: bool,
):
    """
    Exports project's information.
    """
    export_params = {
        "attachments": attachements,
        "metadata_fields": metadata_fields,
        "data_row_details": data_row_details,
        "project_details": project_details,
        "performance_details": performance_details,
    }
    project = client.get_project(project_id)
    export_task = project.export_v2(params=export_params)  # type: ignore
    export_task.wait_till_done()

    if err := export_task.errors:
        click.echo("There were errors in the export.")
        click.echo(err)
        sys.exit(1)

    if save:
        filename = Path.home() / f"project_export_{int(time.time())}.json"
        write_json_file(filename, export_task.result)
        click.echo(f"Project's export results were saved into {filename}.")
    else:
        click.echo(f"Project {project_id} export results:\n")
        click.echo(json.dumps(export_task.result, indent=2))

    sys.exit(0)
