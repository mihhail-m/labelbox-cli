from pathlib import Path

import click
from click import Context
from labelbox import Client

from .commands.batch import batch
from .commands.ontology import ontology
from .commands.projects import project
from .utils import find_active_profile, read_json_file, write_json_file

CONFIG_FILE = Path.home() / ".labelbox-cli.json"
SUBCOMMANDS = [project, ontology, batch]


# TODO: Add support for multiple profiles
@click.group()
@click.pass_context
def cli(ctx: Context):
    if CONFIG_FILE.is_file():
        content = read_json_file(CONFIG_FILE)
        profile = find_active_profile(content)
        client = Client(api_key=profile["api_key"], endpoint=profile["endpoint"], rest_endpoint=profile["rest_endpoint"])  # type: ignore
        ctx.obj = client
    else:
        click.echo("Looks like you have not configured any profiles yet.")
        click.echo(
            "Create new profile that will be later used to access your workspace."
        )
        click.echo(f"Profile information is stored locally inside {CONFIG_FILE} file.")

        api_key = input("Enter API key for your workspace: ")
        endpoint = input("Enter GraphQL endpoint. Leave blank if you don't have one: ")
        rest_endpoint = input(
            "Enter REST endpoint. Leave blank if you don't have one: "
        )
        profile_name = input("Profile name. Ex: dev, stage, labeler etc: ")
        profile = {
            profile_name: {
                "name": profile_name,
                "api_key": api_key,
                "endpoint": endpoint,
                "rest_endpoint": rest_endpoint,
                "active": True,
            }
        }

        write_json_file(CONFIG_FILE, profile)
        click.echo(f"Configuration saved into: {CONFIG_FILE}")


for subcommand in SUBCOMMANDS:
    cli.add_command(subcommand)
