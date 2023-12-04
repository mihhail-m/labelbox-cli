import sys

import click
from labelbox import Client


@click.group
def ontology():
    """
    Command for interacting with Ontologies. Use subcommands to perform CRUD operation.
    """
    pass


@ontology.command()
@click.argument("--ontology_id", nargs=1)
@click.pass_obj
def get(client: Client, ontology_id: str):
    """
    Retrieve ontology by ID. Prints result into the console.
    """
    ontology = client.get_ontology(ontology_id)
    click.echo(ontology)
    sys.exit(0)


@ontology.command()
@click.option(
    "--name_contains", required=True, help="Retrieves list of ontology matched by name."
)
@click.option("--n", default=10, help="List available ontologies.", show_default=True)
@click.pass_obj
def list(client: Client, name_contains: str, n: int):
    """
    List available ontologies in the workspace. By default print only first 10.
    """
    ontologies = list(client.get_ontologies(name_contains=name_contains))

    # Apperantly Click for some reasons cannot convert generators into lists
    # hence this ugly workaround
    for ontology in ontologies:
        click.echo(ontology)

        n -= 1
        if n == 0:
            break

    sys.exit(0)
