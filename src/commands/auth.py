import click


@click.command()
@click.option(
    "--api_key",
    required=True,
    help="API key generated in the Labelbox workspace settings.",
)
@click.pass_context
def auth(ctx, api_key):
    """
    Authorizes CLI to perform action on the Labelbox workspace.
    """
    ...
