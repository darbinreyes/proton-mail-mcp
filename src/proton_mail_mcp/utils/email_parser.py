import email
import email.policy
from dataclasses import dataclass
from email.message import Message

from bs4 import BeautifulSoup


@dataclass
class EmailSummary:
    subject: str
    sender: str
    date: str
    snippet: str


def parse_html_body(html: str) -> str:
    """Extract visible text from an HTML string using BeautifulSoup.

    Uses Python's stdlib html.parser as the backend — no C extensions needed.
    BeautifulSoup finds the <body> tag and returns its text content with
    whitespace normalized.
    """
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body") or soup
    return " ".join(body.get_text().split())


def extract_text_snippet(msg: Message, max_chars: int = 200) -> str:
    """Extract a plain text snippet from a MIME email message.

    Uses the modern email.policy.default API (Python 3.6+): EmailMessage.get_body()
    searches the MIME tree and returns the best matching part directly, handling
    multipart/alternative preference logic internally.

    Falls back to manual walk() for messages parsed without the modern policy
    (e.g. already-parsed Message objects passed in directly).
    """
    # Modern path: EmailMessage with policy.default exposes get_body()
    if hasattr(msg, "get_body"):
        part = msg.get_body(preferencelist=("plain", "html"))
        if part is not None:
            content = part.get_content()  # decoded str, charset-aware
            if part.get_content_type() == "text/html":
                content = parse_html_body(content)
            return content.strip()[:max_chars]

    # Fallback: legacy Message object — walk manually
    plain: str | None = None
    html_fallback: str | None = None

    for part in msg.walk():
        if part.get_content_type() == "text/plain" and plain is None:
            raw = part.get_payload(decode=True)
            plain = raw.decode(part.get_content_charset() or "utf-8", errors="replace")
        elif part.get_content_type() == "text/html" and html_fallback is None:
            raw = part.get_payload(decode=True)
            html_str = raw.decode(part.get_content_charset() or "utf-8", errors="replace")
            html_fallback = parse_html_body(html_str)

    text = plain or html_fallback or "[no text content]"
    return text.strip()[:max_chars]


def parse_email(raw: bytes) -> EmailSummary:
    """Parse a raw RFC822 email into an EmailSummary.

    Uses email.policy.default (modern API) so the returned object is an
    EmailMessage with get_body(), get_content(), etc. available.
    """
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    return EmailSummary(
        subject=msg.get("Subject", "(no subject)"),
        sender=msg.get("From", "(unknown)"),
        date=msg.get("Date", "(unknown)"),
        snippet=extract_text_snippet(msg),
    )
