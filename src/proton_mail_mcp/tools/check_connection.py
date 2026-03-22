from proton_mail_mcp.utils.config import load_bridge_config
from proton_mail_mcp.utils.imap import connect_imap


def check_connection() -> str:
    """Connect to Proton Bridge IMAP and confirm the authenticated user."""
    config = load_bridge_config()
    M = connect_imap(config)
    M.logout()
    return f"Connected as {config.user}"
