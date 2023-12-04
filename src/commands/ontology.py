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
