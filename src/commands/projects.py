import click


@click.group()
def projects():
    """
    Command for interacting with Projects in the workspace. Use subcommands for retrieveing necessary data.
    """
    pass


@projects.command()
@click.option(
    "--n", default=10, help="List number of available projects.", show_default=True
)
def list(n):
    """
    Lists available projects.
    """
    ...


@projects.command()
@click.argument("project_id", nargs=1)
def get(project_id):
    """
    Retrieves project with given ID.
    """
    ...


@projects.command()
@click.option("--name", required=True, type=str, help="Name for a project.")
@click.option(
    "--media_type",
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
def create(name, description, media_type):
    """
    Creates new project.
    """
    ...
