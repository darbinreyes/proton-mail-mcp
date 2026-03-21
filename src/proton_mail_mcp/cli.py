import click

from proton_mail_mcp.commands.serve import serve


@click.group()
def main() -> None:
    """Proton Mail MCP server."""


main.add_command(serve)
