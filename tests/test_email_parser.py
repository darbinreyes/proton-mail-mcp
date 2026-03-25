import textwrap
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from proton_mail_mcp.utils.email_parser import parse_email


def make_plaintext_email() -> bytes:
    """Simple text/plain email — the straightforward case."""
    msg = MIMEText("Hello,\n\nThis is a plain text email body.\n\nRegards,\nAlice", "plain")
    msg["Subject"] = "Plain text test"
    msg["From"] = "alice@proton.me"
    msg["Date"] = "Mon, 17 Mar 2026 10:00:00 +0000"
    return msg.as_bytes()


def make_html_only_email() -> bytes:
    """text/html only — no plain text part (common for newsletters)."""
    body = textwrap.dedent("""\
        <html><body>
          <h1>Hello!</h1>
          <p>This email has <b>only</b> an HTML part.</p>
        </body></html>
    """)
    msg = MIMEText(body, "html")
    msg["Subject"] = "HTML only test"
    msg["From"] = "newsletter@example.com"
    msg["Date"] = "Mon, 17 Mar 2026 11:00:00 +0000"
    return msg.as_bytes()


def make_multipart_email() -> bytes:
    """multipart/alternative with both text/plain and text/html parts.
    This is the most common real-world format — clients show whichever
    part they support; MUAs prefer text/plain for readability.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Multipart test"
    msg["From"] = "bob@proton.me"
    msg["Date"] = "Mon, 17 Mar 2026 12:00:00 +0000"
    msg.attach(MIMEText("Hello, this is the plain text version.", "plain"))
    msg.attach(MIMEText("<html><body><p>Hello, this is the <b>HTML</b> version.</p></body></html>", "html"))
    return msg.as_bytes()


def test_parse_plaintext_email_headers() -> None:
    summary = parse_email(make_plaintext_email())
    assert summary.subject == "Plain text test"
    assert summary.sender == "alice@proton.me"
    assert summary.date == "Mon, 17 Mar 2026 10:00:00 +0000"


def test_parse_plaintext_email_snippet() -> None:
    summary = parse_email(make_plaintext_email())
    assert "plain text email body" in summary.snippet


def test_parse_html_only_email_headers() -> None:
    summary = parse_email(make_html_only_email())
    assert summary.subject == "HTML only test"
    assert summary.sender == "newsletter@example.com"


def test_parse_html_only_email_snippet() -> None:
    summary = parse_email(make_html_only_email())
    # Should not be empty — either stripped HTML text or a placeholder
    assert summary.snippet != ""


def test_parse_multipart_email_prefers_plain() -> None:
    summary = parse_email(make_multipart_email())
    assert "plain text version" in summary.snippet


def test_parse_multipart_email_no_html_tags_in_snippet() -> None:
    summary = parse_email(make_multipart_email())
    assert "<html>" not in summary.snippet
    assert "<b>" not in summary.snippet