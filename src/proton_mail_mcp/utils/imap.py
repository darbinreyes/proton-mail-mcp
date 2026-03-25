from imaplib import IMAP4, IMAP4_SSL

from proton_mail_mcp.utils.config import BridgeConfig
from proton_mail_mcp.utils.email_parser import EmailSummary, parse_email


def connect_imap(config: BridgeConfig) -> IMAP4:
    """Connect and authenticate to Proton Bridge via IMAP.

    Proton Bridge listens on localhost and uses STARTTLS (not SSL) by default:
      - IMAP port: 1143 or 143 (STARTTLS) — plain connection upgraded to TLS
      - IMAP port: 993 (SSL) — SSL from the start
    Raises imaplib exceptions as-is so the caller can handle them.
    """
    if config.imap_port in (143, 1143):
        M = IMAP4(host=config.host, port=config.imap_port, timeout=30)
        M.starttls()
        M.login(config.user, config.password)
        return M

    if config.imap_port == 993:
        M = IMAP4_SSL(host=config.host, port=config.imap_port, timeout=30)
        M.login(config.user, config.password)
        return M

    raise ValueError(f"Unhandled IMAP port: {config.imap_port}")


def fetch_recent_emails(M: IMAP4, n: int = 5) -> list[EmailSummary]:
    """Fetch the n most recent emails from INBOX and return parsed summaries."""
    M.select("INBOX", readonly=True)
    _, data = M.search(None, "ALL")
    # data[0] is a space-separated list of message IDs e.g. b"1 2 3 4 5"
    all_ids = data[0].split()
    recent_ids = all_ids[-n:]  # last n = most recent
    summaries = []
    for msg_id in reversed(recent_ids):  # newest first
        _, msg_data = M.fetch(msg_id, "(RFC822)")
        raw = msg_data[0][1]
        summaries.append(parse_email(raw))
    return summaries
