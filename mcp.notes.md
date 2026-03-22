# How MCPs work

-Testing ping tool via raw stdio (Option 2) to understand the underlying MCP protocol.

  MCP uses JSON-RPC 2.0 over stdin/stdout. The protocol requires a 4-step sequence
  before any tool call can be made:

  1. **Client → Server: `initialize`** — client declares its protocol version and
     capabilities; `id: 0` marks it as a request (expects a response).
  2. **Server → Client: `initialize` response** — server replies with its own
     capabilities and metadata; matched by `id: 0`.
  3. **Client → Server: `notifications/initialized`** — client signals it is ready;
     no `id` field because this is a notification (no response expected).
  4. **Client → Server: `tools/call`** — now tool calls are allowed; `id: 1` expects
     a response.

  The server delineates messages using **newline-delimited JSON (NDJSON)** — it reads
  one line at a time from stdin and parses each line as a complete JSON object. The
  `\n` separators in the `printf` command below mark the boundary between messages.
  No framing headers or length prefixes are needed; one JSON object per line is the
  entire protocol framing.

  Send all three client messages at once (the server processes them in order). Pipe
  through `jq .` to pretty-print the JSON responses (`brew install jq` if needed):

  ```bash
  printf '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}\n{"jsonrpc":"2.0","method":"notifications/initialized"}\n{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ping","arguments":{}}}\n' \
    | uv run proton_mail_mcp serve | jq .
  ```

  Expected output — 2 responses (step 2 and step 4; step 3 is a notification so no
  response is sent):

  ```json
  {
    "jsonrpc": "2.0",
    "id": 0,
    "result": {
      "protocolVersion": "2024-11-05",
      "capabilities": {
        "experimental": {},
        "prompts": { "listChanged": false },
        "resources": { "subscribe": false, "listChanged": false },
        "tools": { "listChanged": false }
      },
      "serverInfo": { "name": "proton-mail-mcp", "version": "1.26.0" }
    }
  }
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "content": [{ "type": "text", "text": "pong from proton-mcp" }],
      "structuredContent": { "result": "pong from proton-mcp" },
      "isError": false
    }
  }
  ```
