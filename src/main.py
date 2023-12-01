import json
from pathlib import Path

import click
from click import Context
from labelbox import Client

from .commands.projects import projects

CONFIG_FILE = Path.home() / ".labelbox-cli.json"


def find_active_profile(profiles, key="active", value=True):
    if key in profiles and profiles[key] == value:
        return profiles

    for _, v in profiles.items():
        if isinstance(v, dict):
            result = find_active_profile(v, key, value)
            if result is not None:
                return result


def read_config_file(config_file_path):
    with open(config_file_path, "rb") as f:
        return json.load(f)


def write_to_config_file(config_file_path, profile):
    with open(config_file_path, "w+", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=4)


# TODO: Add support for multiple profiles
@click.group()
@click.pass_context
def cli(ctx: Context):
    if CONFIG_FILE.is_file():
        content = read_config_file(CONFIG_FILE)
        profile = find_active_profile(content)
        client = Client(api_key=profile["api_key"], endpoint=profile["endpoint"])  # type: ignore
        ctx.obj = client
    else:
        click.echo("Looks like you have not configured any profiles yet.")
        click.echo(
            "Create new profile that will be later used to access your workspace."
        )
        click.echo(f"Profile information is stored locally inside {CONFIG_FILE} file.")

        api_key = input("Enter API key for your workspace: ")
        endpoint = input("Enter GraphQL endpoint. Leave blank if you don't have one: ")
        profile_name = input("Profile name. Ex: dev, stage, labeler etc: ")
        profile = {
            profile_name: {
                "name": profile_name,
                "api_key": api_key,
                "endpoint": endpoint,
                "active": True,
            }
        }

        write_to_config_file(CONFIG_FILE, profile)
        click.echo(f"Configuration saved into: {CONFIG_FILE}")


cli.add_command(projects)
