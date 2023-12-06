import sys

import click
from labelbox import Client, MediaType


@click.group()
def ontology():
    """
    Command for interacting with Ontologies. Use subcommands to perform CRUD operation.
    """
    pass


@ontology.command("get")
@click.argument("ontology_id", nargs=1)
@click.pass_obj
def get_ontology(client: Client, ontology_id: str):
    """
    Retrieve ontology by ID. Prints result into the console.
    """
    ontology = client.get_ontology(ontology_id)
    click.echo(ontology)
    sys.exit(0)


@ontology.command("list")
@click.option(
    "--name_contains", required=True, help="Retrieves list of ontology matched by name."
)
@click.option("--n", default=5, help="List available ontologies.", show_default=True)
@click.pass_obj
def list_ontologies(client: Client, name_contains: str, n: int):
    """
    List available ontologies in the workspace. By default print only first 10.
    """
    ontologies = client.get_ontologies(name_contains=name_contains)

    # Apperantly Click for some reasons cannot convert generators into lists
    # hence this ugly workaround
    for ontology in ontologies:
        click.echo(ontology)

        n -= 1
        if n == 0:
            break

    sys.exit(0)


@ontology.command("create")
@click.option("--name", required=True, help="Name for the ontology.")
@click.option(
    "--media_type", required=True, help="Ontology media type. Ex: image, video etc."
)
@click.option(
    "--tools",
    default="",
    help='List of comma separated ID values. Ex: "toolId1,toolId2".',
    type=str,
)
@click.option(
    "--classifications",
    "--c",
    "classifications",
    default="",
    help='List of comma separated ID values. Ex: "classificationId1,classificationId2".',
    type=str,
)
@click.pass_obj
def create_ontology(
    client: Client, name: str, media_type: str, tools: str, classifications: str
):
    """
    Create new ontology from existing tools and classifications.
    Creates empty ontology if no tools or classifications provided.
    """
    feature_schema_ids = (tools + "," + classifications).split(",")
    feature_schema_ids = [
        feature.strip() for feature in feature_schema_ids
    ]  # remove whitespaces
    feature_schema_ids = list(
        filter(None, feature_schema_ids)
    )  # remove empty strings from default values
    ontology = client.create_ontology_from_feature_schemas(
        name, feature_schema_ids, MediaType(media_type.upper())
    )
    click.echo("New ontology has been created:\n")
    click.echo(ontology)
    sys.exit(0)


@ontology.command("delete")
@click.argument("ontology_id", nargs=1)
@click.pass_obj
def delete_ontology(client: Client, ontology_id: str):
    """
    Deletes unused ontology by ID.
    """
    client.delete_unused_ontology(ontology_id)
    click.echo(f"Ontology with ID {ontology_id} has been deleted.")
    sys.exit(0)
