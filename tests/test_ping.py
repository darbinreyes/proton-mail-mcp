from proton_mail_mcp.tools.ping import ping


def test_ping_returns_pong() -> None:
    assert ping() == "pong from proton-mcp"


def test_ping_returns_string() -> None:
    assert isinstance(ping(), str)
