# TODO

## Code Review: extract_text_snippet() — homework submission

### What was good
- **Correct use of `msg.walk()`** — the right way to recurse the MIME tree.
- **Correct content type checks** — `"text/plain"` and `"text/html"` are exactly the right strings to check.
- **Correct slicing for max_chars** — `plain[:200]` works correctly.
- **Type annotation on `payload_list`** — good habit.

### Issues found

**1. `decode=False` — should be `decode=True` (most important)**
```python
# Wrong — returns raw encoded string (may be base64 or quoted-printable)
part.get_payload(i=None, decode=False)

# Correct — decodes the transfer encoding, returns bytes
part.get_payload(decode=True)
```
With `decode=False`, you get the raw transport-encoded payload. A
quoted-printable encoded body looks like `Hello=2C=20world=21`. With
`decode=True`, imaplib/email decodes it to bytes first, then you decode
to str with the part's charset.

**2. No charset handling**
After `get_payload(decode=True)` you get `bytes`, not `str`. You must
decode them using the part's declared charset:
```python
raw = part.get_payload(decode=True)
text = raw.decode(part.get_content_charset() or "utf-8", errors="replace")
```
Without this, you'd get a `TypeError` when trying to use the bytes as a string.

**3. Private API usage — `_structure` is not for production code**
`from email.iterators import _structure` — the leading underscore means
it's internal to the stdlib and not part of the public API. It may change
or disappear between Python versions. Fine for exploration; remove before
shipping.

**4. Appends all MIME parts including multipart containers**
`multipart/alternative` and `multipart/mixed` container parts have no
meaningful text payload. Appending them to `payload_list` then joining
with commas produces noise. Only leaf parts (`text/plain`, `text/html`)
should contribute to the snippet.

**5. Joins all parts with comma instead of preferring plain over HTML**
The correct strategy is: find the best single part (prefer `text/plain`,
fall back to `text/html`), not concatenate everything together.

**6. Debug prints not removed**
`print(f"text/plain = {payload}")` etc. would spam the MCP server's
stdout on every tool call, which interferes with the JSON-RPC protocol
(the client reads stdout expecting only JSON).

### Summary
The structural approach was correct — `walk()` + content type checks is
exactly the right pattern. The issues were around the details of the
`email` API (`decode=True`, charset decoding) and output hygiene (debug
prints, not joining unrelated parts). These are typical first-pass issues
when learning a new stdlib module.
