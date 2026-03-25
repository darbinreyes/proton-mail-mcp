from proton_mail_mcp.utils.config import load_bridge_config
from proton_mail_mcp.utils.imap import connect_imap, fetch_recent_emails


def list_emails(n: int = 5) -> str:
    """Fetch the n most recent emails from INBOX and return a text summary."""
    config = load_bridge_config()
    M = connect_imap(config)
    summaries = fetch_recent_emails(M, n)
    M.logout()

    lines = []
    for i, email in enumerate(summaries):
        lines.append(
            f"[{i}] From: {email.sender}\n"
            f"    Date: {email.date}\n"
            f"    Subject: {email.subject}\n"
            f"    {email.snippet}"
        )
    return "\n\n".join(lines) if lines else "No emails found."
