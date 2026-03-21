# TODO

## Testing

- [ ] Test ping tool via raw stdio (Option 2) to understand the underlying MCP protocol:
  ```bash
  echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ping","arguments":{}}}' \
    | uv run proton_mail_mcp serve
  ```
  Expected response: `"pong from proton-mcp"`
