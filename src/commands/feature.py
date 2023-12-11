import sys

import click
from labelbox import Classification, Client, Option, Tool


@click.group()
def feature():
    """
    Command for interacting with Features in the workspace.
    """
    pass


@feature.command("get")
@click.argument("feature_schema_id", nargs=1)
@click.pass_obj
def get_feature_by_id(client: Client, feature_schema_id: str):
    """
    Get Feature by ID (featureSchemaId).
    """
    feature = client.get_feature_schema(feature_schema_id)
    click.echo(feature)
    sys.exit(0)


@feature.command("get-by-name")
@click.argument("feature_name", nargs=1)
@click.pass_obj
def get_feature_by_name(client: Client, feature_name: str):
    """
    Get Feature by name.
    """
    feature = next(client.get_feature_schemas(feature_name))
    click.echo(feature)
    sys.exit(0)


@feature.command("delete")
@click.argument("feature_schema_id", nargs=1)
@click.pass_obj
def delete_feature_schema(client: Client, feature_schema_id: str):
    """
    Deletes ununsed feature schema by ID (featureSchemaId).
    """
    client.delete_unused_feature_schema(feature_schema_id)
    click.echo(f"Feature with ID {feature_schema_id} has been deleted.")
    sys.exit(0)


@feature.command("create-tool")
@click.option("--name", "--n", required=True, help="Tool name.")
@click.option(
    "--type",
    "--t",
    "tool_type",
    required=True,
    type=click.Choice(
        ["bbox", "polygon", "raster_segmentation", "point", "line", "ner"]
    ),
)
@click.option(
    "--color",
    "--c",
    default="",
    help='HEX value of a color between double quotes. Ex: --c "#127361". Otherwise random color assigned.',
)
@click.option(
    "--required",
    "--r",
    is_flag=True,
    default=False,
    help="Whether or not make Tool required.",
)
@click.pass_obj
def create_tool(client: Client, name: str, tool_type: str, color: str, required: bool):
    """
    Creates a Tool of a choosen type.
    """
    tool_type_map = {val.name: val.value for val in Tool.Type}
    lb_tool_type = Tool.Type(tool_type_map[tool_type.upper()])
    tool = Tool(tool=lb_tool_type, name=name, required=required, color=color)
    feature = client.create_feature_schema(tool.asdict())
    click.echo("Tool has been created.")
    click.echo(feature)
    sys.exit(0)


@feature.command("create-classification")
@click.option("--name", "--n", required=True, help="Classification name.")
@click.option(
    "--class_type",
    "--t",
    required=True,
    help="Classification type",
    type=click.Choice(["text", "checklist", "radio", "dropdown"]),
)
@click.option(
    "--required",
    "--r",
    is_flag=True,
    default=False,
    help="Whether or not make Classification required.",
)
@click.option(
    "--options",
    "--o",
    default="",
    help='List of options separated by comma. Ex: "option1,option2".',
)
@click.pass_obj
def create_classification(
    client: Client, name: str, class_type: str, required: bool, options: str
):
    """
    Creates a Classification of choosen type.
    """
    lb_options = []

    if options and options.strip():
        lb_options = [Option(option) for option in options.split(",")]

    lb_type = Classification.Type(class_type)
    classification = Classification(
        name=name, class_type=lb_type, options=lb_options, required=required
    )
    feature = client.create_feature_schema(classification.asdict())
    click.echo("Classification has been create.")
    click.echo(feature)
    sys.exit(0)
