import click
from click import Context

from .commands.auth import auth
from .commands.projects import projects


@click.group()
@click.pass_context
def cli(ctx: Context):
    ctx.ensure_object(dict)


cli.add_command(projects)
cli.add_command(auth)

if __name__ == "__main__":
    cli(obj={})
