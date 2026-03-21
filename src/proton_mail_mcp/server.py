from mcp.server.fastmcp import FastMCP

from proton_mail_mcp.tools.ping import ping

mcp = FastMCP("proton-mail-mcp")

mcp.tool()(ping)


def run_server() -> None:
    mcp.run()
