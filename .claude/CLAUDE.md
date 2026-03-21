
@./summary.CLAUDE.md

# proton-mail-mcp Planning Conversation

## Proton Mail MCP — Install Command?

**Darbin:** command to install proton mail mcp

**Claude:** There's no official Proton Mail MCP server available — Proton isn't in the list of connected MCP servers, and there's no widely-adopted community MCP for it yet either.

A few options depending on what you're trying to do:

1. **Use the Proton Mail Bridge** — it exposes your Proton account via IMAP/SMTP locally, so you could build an MCP server on top of that using the MCP Python SDK or TypeScript SDK.
2. **Check community repos** — search GitHub for `proton mail mcp` or `protonmail mcp`; some community servers exist but none are officially maintained.
3. **Use a generic email MCP** — if you just need email read/send capabilities, the Gmail MCP is already connected to your account and works out of the box.

---

## What Can a Custom Proton Mail MCP Do?

**Darbin:** what kinds of things can I do with "a custom Proton Mail MCP server using the Bridge + Python"

**Claude:** With Proton Mail Bridge exposing a local IMAP/SMTP interface, an MCP server on top of it could give Claude the ability to:

**Read**
- Search and fetch emails (by sender, subject, date, label)
- Summarize threads or inboxes
- Extract attachments
- Monitor for new mail

**Write**
- Compose and send emails
- Reply / reply-all / forward
- Draft emails without sending

**Organize**
- Move messages to folders/labels
- Mark as read/unread/starred
- Delete or archive messages

**Agentic workflows**
- "Check my inbox and summarize anything urgent from today"
- "Reply to all emails from X saying I'll get back to them next week"
- "Find all emails with invoices attached and list the amounts"
- "Draft responses to these 5 emails for my review"

The main **constraint** is that Proton Bridge must be running locally and authenticated — so this works great for a personal setup on your machine, but isn't something you could deploy to a server without Bridge running there too.

---

## GitHub Repo?

**Darbin:** sounds interesting, supposing I want to proceed, should I create a github repo for it?

**Claude:** Yes, worth doing — a few reasons specific to MCP servers:

**Practical reasons**
- Claude Desktop / other MCP clients often reference servers by git URL for installation (`npx`, `uvx`, or cloning directly)
- Makes it easy to share your config snippet (the `mcpServers` JSON) with others
- Version pinning matters — you'll want tags so a working config doesn't break when you update

**If you ever want others to use it**
- There's no official Proton MCP, so yours would fill a real gap
- Anthropic maintains a community MCP servers list where you could submit it
- Proton users are generally privacy-conscious and likely to prefer a self-hosted solution like this over a cloud one

**If it's just for yourself**
- Still useful for tracking changes and rolling back if something breaks
- Gives you a clean place to store the Bridge config, `.env` structure, and `README` with setup steps (which are non-trivial for Bridge)

**Suggested repo structure:**

```
proton-mcp/
├── server.py          # MCP server entrypoint
├── imap_client.py     # Bridge IMAP logic
├── smtp_client.py     # Bridge SMTP logic
├── tools/             # One file per MCP tool group
├── pyproject.toml     # uvx-installable
├── .env.example
└── README.md          # Bridge setup steps are critical to document
```

Making it `uvx`-installable from the start is worth the small upfront cost — it's the cleanest install story for Python MCP servers.

---

## Image Rendering in CLI?

**Darbin:** when reading emails from claude CLI, is there a way to render images occurring in the email?

**Claude:** Short answer: **no, not in Claude CLI (Claude Code)** — it's a terminal environment, so there's no image rendering pipeline.

**Claude Code (terminal)**
- Text only in the interface
- You could pass image attachments as base64 to the Claude API within your MCP server, so Claude can understand the image content and describe it — but you won't see a rendered image in the terminal
- Inline HTML emails with `<img>` tags would just show up as extracted URLs or alt text

**Claude.ai (web/desktop) — where it gets interesting**
- If your MCP server extracts images from emails and returns them properly, Claude.ai can display them inline in the conversation
- This would require your MCP tool to return image data in the MCP content format (base64 + mime type), which the web client knows how to render

**Practical middle ground for CLI**
- Extract and save attachments/inline images to a temp directory and open them with your system viewer (`xdg-open`, `open` on Mac)
- Your MCP tool could do this automatically when fetching an email — Claude triggers the tool, image pops open in your default viewer

So if image rendering matters to you, **claude.ai desktop app** is the better client for this MCP server than Claude Code. Worth keeping in mind when you design the tool return types — structuring them to return proper image content blocks would make the server work well in both contexts.

---

## Where to Build: claude.ai vs Claude Code CLI?

**Darbin:** Should we create it from here or should I open a session in claude code CLI

**Claude:** Either works, but here's the honest tradeoff:

**From here (claude.ai)**
- Good for scaffolding the initial structure, talking through design decisions
- I can generate all the files and you download them
- But I can't run/test the code, install packages, or iterate on errors

**Claude Code CLI**
- Can actually run the server, install deps, test IMAP connections against your live Bridge
- Iterates on errors in place — much better for the parts where Bridge config and auth will inevitably need debugging
- Better for a project that will live on your filesystem anyway

**Suggestion: hybrid**
- Finalize design decisions here (takes 5 minutes)
- Then open Claude Code and build+test there

The main design question worth settling first: **scope**. Do you want to start minimal (read inbox, send email) or go broader from the start? That affects whether `tools/` needs to be a package or if `server.py` can stay flat for now.

---

## Stepped Development Plan

**Darbin:** if I decide to start implementing it would probably start simple, text only CLI with images saved to a temp dir, then add what is necessary to interface with claude.ia to support image rendering. The goal is understand how things work by developing in steps, not one shot coding it. The end result should provide allow interfacing via CLI and Claude.ai.

Let's take into account that I will develop and test on this machine, but ultimately will move it to a standalone Mac that will be my always on server. Any concerns WRT that?

**Claude:** Good development philosophy. The stepped approach will also naturally surface Bridge quirks early.

**On the Mac server deployment — a few real concerns:**

**Bridge specifically**
- Proton Bridge requires a GUI session to authenticate initially (it's an Electron app) — no headless first-launch
- Once authenticated it can run as a background process, but on macOS it needs a logged-in user session
- Updates to Bridge can break auth and require re-login
- Worth checking: Bridge has a CLI/headless mode (`proton-bridge --cli`) which is better suited for a server than the GUI version

**MCP server process management**
- On the always-on Mac you'll want `launchd` (not `cron`, not `pm2`) — it's the native macOS way to keep a process alive across reboots and crashes
- Your `.env` / credentials path will need to be absolute, not relative, for launchd to find them

**Dev → server portability**
- Use `pyproject.toml` + `uv` from day one so the install story is identical on both machines
- Keep Bridge host/port/credentials in `.env` — don't hardcode anything assuming your dev machine's setup
- Python version: pin it explicitly (`requires-python = ">=3.11"`) so there's no surprise on the server

**One forward-looking concern**
- If the always-on Mac is on a different network than where you're running Claude Code or claude.ai, the MCP server won't be reachable unless you expose it (tunnel, VPN, etc.) — MCP currently assumes localhost or local network. Worth thinking about topology early even if you don't solve it now.

---

## Bare Bones Feature Set / Hello World

**Darbin:** what is the bare bones feature set to aim for initially? Perhaps a hello world, this is my first mcp?

**Claude:** For a true "hello world MCP" that also validates your Bridge setup:

**Step 1 — MCP handshake only**
A server with a single dummy tool that returns a hardcoded string. No Bridge at all. Goal: confirm the MCP server registers correctly in Claude Code / claude.ai, you understand the tool definition pattern, and the plumbing works.

```python
# tool: ping
# returns: "pong from proton-mcp"
```

**Step 2 — Bridge connection**
Add one tool that just connects to Bridge IMAP and returns success/failure + your email address. No reading yet. Goal: confirm Bridge auth, host, port, SSL are all correct.

```python
# tool: check_connection
# returns: "Connected as user@proton.me"
```

**Step 3 — Read inbox**
One tool, fetch N most recent emails, text only, no attachments. Subject, sender, date, body snippet.

```python
# tool: list_emails(n=5)
```

**Step 4 — Send**
One tool, send a plain text email.

```python
# tool: send_email(to, subject, body)
```

That's it for v0. Steps 1 and 2 are the ones most likely to surface surprises, which is exactly why they're worth isolating.

---

## Handoff Summary for Claude Code

**Darbin:** yes, but let make a note of "`proton-bridge --cli`) which is better suited for a server than the GUI version" since the server based setup is the ultimate goal. What is the best way to hand off the context of our planning here to claude code?

**Claude:** Simplest approach — copy-paste this summary into your Claude Code session as the opening message.

**Darbin:** modify the summary. for top level dir name "proton-mail-mcp", for dir structure, use src style layout, src/proton_mail_mcp as the top level module, we will be using click for any CLI interfacing, also follow the style of CLI that uses a cli.py and a __main__.py, subcommands of the CLI will go in src/proton_mail_mcp/commands, auxillary code will go in src/proton_mail_mcp/utils, pyproject.toml should specify that the server will be invoked as simply proton_mail_mcp (i.e. when installed via uv), we will use hatch as a build back end, ruff for formatting, pytest for testing, along with some bare bones initial tests in the tests directory. Testing will also involve tox, setup tox.ini to test python 3.14 and 3.13, integrated with pytest.

---

## Final Handoff Summary (for `.claude/CLAUDE.md`)

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

## Notes

- `proton-bridge --cli` (headless mode) is the target for the always-on server deployment, not the GUI version
- MCP topology: if the always-on Mac is on a different network, the MCP server will need a tunnel or VPN to be reachable from Claude Code / claude.ai
- `.claude/CLAUDE.md` is the right location for the handoff summary in the repo — Claude Code picks it up automatically every session