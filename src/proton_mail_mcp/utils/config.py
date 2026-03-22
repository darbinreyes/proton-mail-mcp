import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BridgeConfig:
    host: str
    imap_port: int
    smtp_port: int
    user: str
    password: str


def load_bridge_config() -> BridgeConfig:
    return BridgeConfig(
        host=os.getenv("BRIDGE_HOST", "127.0.0.1"),
        imap_port=int(os.getenv("BRIDGE_IMAP_PORT", "1143")),
        smtp_port=int(os.getenv("BRIDGE_SMTP_PORT", "1025")),
        user=os.environ["BRIDGE_USER"],
        password=os.environ["BRIDGE_PASSWORD"],
    )
