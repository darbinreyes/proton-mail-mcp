from mcp.server.fastmcp import FastMCP

from proton_mail_mcp.tools.check_connection import check_connection
from proton_mail_mcp.tools.ping import ping

mcp = FastMCP("proton-mail-mcp")

mcp.tool()(ping)
mcp.tool()(check_connection)


def run_server() -> None:
    mcp.run()
