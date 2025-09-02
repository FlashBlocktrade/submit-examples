# Flashblock Submit Examples

Ready-to-run clients for Flashblock batch submit API in multiple languages.

Current structure:
- NodeJS: `nodejs/`
- Python: `python/`
- Rust: `rust/`
- Go: `go/`

Each client includes:
- Endpoint selection (ping root URL)
- HTTP Keep-Alive
- Simple retry for 429/5xx
- Batch submit to `/api/v2/submit-batch`

Chinese documentation: see [README.zh.md](https://github.com/FlashBlocktrade/submit-examples/blob/main/README.zh.md).

## Quick Start
- NodeJS
  - `cd nodejs && npm i`
  - `AUTH_HEADER='Bearer YOUR_TOKEN' node index.js`
- Python
  - `cd python && python3 -m venv .venv && . .venv/bin/activate`
  - `pip install -r requirements.txt`
  - `AUTH_HEADER='Bearer YOUR_TOKEN' python main.py`
- Rust
  - `cd rust && AUTH_HEADER='Bearer YOUR_TOKEN' cargo run`
- Go
  - `cd go && AUTH_HEADER='Bearer YOUR_TOKEN' go run .`

Note: set environment variable `AUTH_HEADER` before running.
