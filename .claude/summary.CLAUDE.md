Here's the updated handoff summary:

---

> I'm building a Python MCP server called `proton-mail-mcp` that interfaces with Proton Mail via Proton Bridge. Here's the plan:
>
> **Goal:** MCP server usable from both Claude Code (CLI) and claude.ai. Images from emails saved to temp dir for CLI, proper image content blocks for claude.ai.
>
> **Deployment:** Develop/test on current Mac, then move to always-on Mac server. Use `proton-bridge --cli` (headless) for the server deployment. Use `launchd` for process management. Use `uv` + `pyproject.toml` for portable install.
>
> **Build in steps:**
> 1. Dummy `ping` tool — validate MCP plumbing only
> 2. `check_connection` — validate Bridge IMAP auth
> 3. `list_emails(n=5)` — fetch recent emails, text only
> 4. `send_email(to, subject, body)` — send plain text
>
> **Project structure:**
> ```
> proton-mail-mcp/
> ├── src/
> │   └── proton_mail_mcp/
> │       ├── __init__.py
> │       ├── __main__.py
> │       ├── cli.py
> │       ├── server.py
> │       ├── commands/
> │       ├── utils/
> │       └── tools/
> ├── tests/
> ├── pyproject.toml
> ├── tox.ini
> ├── .env.example
> └── README.md
> ```
>
> **Tooling:**
> - Build backend: `hatch`
> - CLI: `click`, following the `cli.py` + `__main__.py` pattern, subcommands in `commands/`
> - Auxiliary code in `utils/`
> - Entry point: installed via `uv` and invoked as `proton_mail_mcp`
> - Formatter/linter: `ruff`
> - Tests: `pytest` with bare bones initial tests in `tests/`
> - `tox.ini` configured to test Python 3.13 and 3.14, integrated with pytest
>
> Start with step 1. Keep things flat and simple until the structure earns its complexity.

---

That should give Claude Code everything it needs to scaffold the project correctly from the first message.