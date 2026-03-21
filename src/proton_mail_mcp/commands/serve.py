import click

from proton_mail_mcp.server import run_server


@click.command()
def serve() -> None:
    """Start the MCP server."""
    run_server()
