# proton-mail-mcp

MCP server for Proton Mail via [Proton Bridge](https://proton.me/mail/bridge).

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Proton Bridge running locally (use `proton-bridge --cli` for headless/server deployments)

## Install

```bash
uv pip install -e ".[dev]"
```

## Usage

```bash
proton_mail_mcp serve
```

Or as a module:

```bash
python -m proton_mail_mcp serve
```

## Configuration

Copy `.env.example` to `.env` and fill in your Bridge credentials:

```bash
cp .env.example .env
```

## Development

```bash
# Run tests
pytest

# Run tests across Python versions
tox

# Lint / format
ruff check .
ruff format .
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `ping` | Validates MCP plumbing — returns `"pong from proton-mcp"` |
