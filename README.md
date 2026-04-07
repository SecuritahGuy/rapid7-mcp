# rapid7-mcp

A locally-runnable MCP server that wraps the [Rapid7 InsightVM](https://www.rapid7.com/products/insightvm/) REST API (v3) and exposes vulnerability management tools to LLM clients — Claude, Cursor, or any [MCP-compatible](https://modelcontextprotocol.io) client.

Built with [fastapi-mcp](https://github.com/tadata-ru/fastapi-mcp), [FastAPI](https://fastapi.tiangolo.com/), and [httpx](https://www.python-httpx.org/). Uses `uv` for dependency management.

> **No Rapid7 instance?** Set `DEMO_MODE=true` and explore all tools against realistic fixture data without any credentials.

---

## Architecture

```text
Claude / Cursor / MCP Client
        │  MCP protocol (SSE)
        ▼
┌─────────────────────────────────┐
│  FastAPI  (uvicorn)  :8000      │
│                                 │
│  /sites          → Sites router │
│  /assets         → Assets router│
│  /vulnerabilities→ Vulns router │
│  /scans          → Scans router │
│                                 │
│  /mcp  ← FastApiMCP (HTTP)       │
└──────────────┬──────────────────┘
               │  httpx (async)
               ▼
      Rapid7 InsightVM Console
         REST API v3 :3780
```

`fastapi-mcp` automatically converts every FastAPI route into an MCP tool — operation IDs become tool names, docstrings become descriptions, and Pydantic schemas become input/output schemas.

---

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 1. Clone and install

```bash
git clone https://github.com/SecuritahGuy/rapid7-mcp.git
cd rapid7-mcp
uv sync
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your InsightVM console URL and credentials
# Or just set DEMO_MODE=true to use fixture data
```

### 3. Run

```bash
# Demo mode (no credentials needed)
DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --reload --port 8000

# With a live console
uv run uvicorn rapid7_mcp.main:app --reload --port 8000
```

The MCP endpoint is available at `http://localhost:8000/mcp`.
The interactive API docs are at `http://localhost:8000/docs`.

---

## Connect to Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "rapid7": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/rapid7-mcp",
        "run", "uvicorn", "rapid7_mcp.main:app", "--port", "8000"
      ],
      "env": {
        "R7_CONSOLE_URL": "https://your-console:3780",
        "R7_USERNAME": "apiuser",
        "R7_PASSWORD": "changeme",
        "R7_VERIFY_SSL": "false"
      }
    }
  }
}
```

For demo mode, add `"DEMO_MODE": "true"` to the `env` block and omit the `R7_*` vars.

---

## Available MCP Tools

| Tool | Description |
| --- | --- |
| `list_sites` | List all InsightVM scan sites with asset counts and risk scores |
| `get_site` | Get details for a single site by ID |
| `get_asset` | Get full asset details — IP, hostname, OS, vulnerability counts by severity |
| `search_assets` | Search assets by field filters (IP, hostname, OS family, site, tag) |
| `get_asset_vulnerabilities` | List all vulnerabilities found on a specific asset |
| `list_vulnerabilities` | Browse the vulnerability library, optionally filtered by severity |
| `get_vulnerability` | Get full vulnerability details — CVSS scores, CVEs, exploit count, description |
| `list_scans` | List recent scans with status, timing, and vulnerability summaries |
| `get_scan` | Get details for a single scan |

### Example prompts

```text
What are the top 3 critical vulnerabilities across my assets?

Which sites have the highest risk scores?

Search for all Linux assets in the production network.

What does CVE-2021-44228 (Log4Shell) look like in InsightVM?

Show me all running scans.
```

---

## Demo Mode

`DEMO_MODE=true` makes the server return realistic fixture data based on the InsightVM v3 API schema — no console required. Fixtures live in [`tests/fixtures/`](tests/fixtures/) and include:

- 3 sites (production, dev, cloud)
- 2 assets with full OS and vulnerability details
- 3 vulnerabilities including Log4Shell and OpenSSL CVE-2022-0778
- 2 scans (one finished, one running)

This is the fastest way to evaluate the server or develop new tools.

---

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest --cov=rapid7_mcp tests/

# Lint
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy rapid7_mcp/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new tool.

---

## Configuration Reference

All settings can be set via environment variables or a `.env` file.

| Variable | Default | Description |
| --- | --- | --- |
| `R7_CONSOLE_URL` | `https://localhost:3780` | InsightVM console base URL |
| `R7_USERNAME` | `admin` | InsightVM username (needs Global Admin role) |
| `R7_PASSWORD` | `password` | InsightVM password |
| `R7_VERIFY_SSL` | `false` | Verify SSL certificates (disable for self-signed) |
| `DEMO_MODE` | `false` | Return fixture data instead of hitting a live console |

---

## License

MIT — see [LICENSE](LICENSE).
