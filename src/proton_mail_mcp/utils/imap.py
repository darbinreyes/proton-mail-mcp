from imaplib import IMAP4, IMAP4_SSL

from proton_mail_mcp.utils.config import BridgeConfig


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
