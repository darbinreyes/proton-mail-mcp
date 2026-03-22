from unittest.mock import MagicMock, patch

from proton_mail_mcp.tools.check_connection import check_connection


@patch("proton_mail_mcp.tools.check_connection.connect_imap")
@patch("proton_mail_mcp.tools.check_connection.load_bridge_config")
def test_check_connection_returns_user(
    mock_config: MagicMock, mock_connect: MagicMock
) -> None:
    mock_config.return_value.user = "test@proton.me"
    mock_connect.return_value = MagicMock()

    result = check_connection()

    assert result == "Connected as test@proton.me"
    mock_connect.return_value.logout.assert_called_once()


@patch("proton_mail_mcp.tools.check_connection.connect_imap")
@patch("proton_mail_mcp.tools.check_connection.load_bridge_config")
def test_check_connection_calls_logout(
    mock_config: MagicMock, mock_connect: MagicMock
) -> None:
    mock_config.return_value.user = "test@proton.me"
    mock_imap = MagicMock()
    mock_connect.return_value = mock_imap

    check_connection()

    mock_imap.logout.assert_called_once()
