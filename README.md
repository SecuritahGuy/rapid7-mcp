# rapid7-mcp

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/SecuritahGuy/rapid7-mcp/actions/workflows/ci.yml/badge.svg)

An MCP server that exposes [Rapid7 InsightVM](https://www.rapid7.com/products/insightvm/) as tools for Claude, Cursor, and any MCP-compatible LLM client. Ask natural-language questions about your vulnerability data — sites, assets, CVEs, scan status — and get structured answers back without writing a single API call.

Built with [fastapi-mcp](https://github.com/tadata-ru/fastapi-mcp), [FastAPI](https://fastapi.tiangolo.com/), and [httpx](https://www.python-httpx.org/).

> **No Rapid7 instance?** Set `DEMO_MODE=true` to explore all tools against realistic fixture data. Clone, run, connect — no credentials required.

---

## What you can do

Once connected to Claude, you can ask things like:

> _"Which of my sites has the highest risk score?"_
> _"What are the critical vulnerabilities on the production web server?"_
> _"Is Log4Shell present anywhere in my environment? Show me the CVSS score and any available exploits."_
> _"What scans are currently running?"_
> _"Search for all Linux assets in the production network."_

The server translates these into InsightVM API calls and returns clean, structured data that Claude can reason over, summarize, and act on.

---

## Architecture

```text
Claude / Cursor / MCP Client
        │  MCP (Streamable HTTP)
        ▼
┌──────────────────────────────────┐
│  FastAPI + fastapi-mcp  :8000    │
│                                  │
│  GET  /sites                     │
│  GET  /sites/{id}                │
│  GET  /assets/{id}               │
│  POST /assets/search             │
│  GET  /assets/{id}/vulns         │
│  GET  /vulnerabilities           │
│  GET  /vulnerabilities/{id}      │
│  GET  /scans                     │
│  GET  /scans/{id}                │
│                                  │
│  /mcp  ← MCP endpoint            │
└─────────────────┬────────────────┘
                  │  httpx async
                  ▼
       Rapid7 InsightVM Console
            REST API v3 :3780
```

Every FastAPI route is automatically published as an MCP tool via `fastapi-mcp`. Operation IDs become tool names, Pydantic schemas become input/output schemas, and docstrings become tool descriptions — the LLM client sees all of this.

---

## Quick Start

**Prerequisites:** Python 3.11+, [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# 1. Clone and install
git clone https://github.com/SecuritahGuy/rapid7-mcp.git
cd rapid7-mcp
uv sync

# 2. Configure (or skip this step and use DEMO_MODE)
cp .env.example .env
# edit .env with your console URL and credentials

# 3. Start the server
DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --port 8000
```

- MCP endpoint: `http://localhost:8000/mcp`
- Interactive API docs: `http://localhost:8000/docs`

---

## Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "rapid7": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Start the server first, then restart Claude Desktop. For demo mode:

```bash
DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --port 8000
```

For a live console, set the env vars in your `.env` file and run without `DEMO_MODE`.

---

## Available MCP Tools

| Tool | Method | Description |
| --- | --- | --- |
| `list_sites` | GET | List all scan sites — names, asset counts, risk scores, last scan time |
| `get_site` | GET | Full details for a single site |
| `get_asset` | GET | Asset details — IP, hostname, OS, vulnerability counts by severity, risk score |
| `search_assets` | POST | Filter assets by IP, hostname, OS family, site ID, or tag |
| `get_asset_vulnerabilities` | GET | All vulnerabilities found on a specific asset |
| `list_vulnerabilities` | GET | Browse the vulnerability library, filter by severity |
| `get_vulnerability` | GET | Full vuln details — CVSS v2/v3, CVEs, exploit count, description, categories |
| `list_scans` | GET | Recent scans with status, duration, and vulnerability summaries |
| `get_scan` | GET | Details for a single scan |

---

## Demo Mode

`DEMO_MODE=true` replaces all API calls with fixture data — realistic responses that match the InsightVM v3 schema. No console, no credentials, no VPN.

Fixtures in [`tests/fixtures/`](tests/fixtures/):

| Fixture | Contents |
| --- | --- |
| `sites.json` | 3 sites: Production Network, Development, Cloud Infrastructure |
| `asset.json` / `assets.json` | Ubuntu and RHEL assets with full vulnerability breakdowns |
| `vulnerability.json` / `vulnerabilities.json` | Log4Shell, OpenSSL CVE-2022-0778, POODLE |
| `asset_vulnerabilities.json` | Vulnerabilities scoped to a single asset |
| `scans.json` / `scan.json` | One finished scan, one running |

This is the fastest way to evaluate the project, develop a new tool, or write a demo.

---

## Configuration

All settings via environment variable or `.env` file.

| Variable | Default | Description |
| --- | --- | --- |
| `R7_CONSOLE_URL` | `https://localhost:3780` | InsightVM console base URL |
| `R7_USERNAME` | `admin` | InsightVM user (Global Administrator role required) |
| `R7_PASSWORD` | `password` | InsightVM password |
| `R7_VERIFY_SSL` | `false` | Set to `true` if your console has a valid certificate |
| `DEMO_MODE` | `false` | Return fixture data; skips all console connectivity |

---

## Development

```bash
uv sync                                          # install deps + dev extras
uv run pytest --cov=rapid7_mcp tests/           # run tests with coverage
uv run ruff check . && uv run ruff format .      # lint + format
uv run mypy rapid7_mcp/                          # type check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new tool, extend fixtures, and open a pull request.

---

## Tech Stack

| Library | Why |
| --- | --- |
| [fastapi-mcp](https://github.com/tadata-ru/fastapi-mcp) | Converts FastAPI routes to MCP tools automatically — auth, deps, and schemas carry through |
| [httpx](https://www.python-httpx.org/) | Async HTTP client, consistent with FastAPI's async model |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Type-safe config from env vars and `.env` files |
| [uv](https://docs.astral.sh/uv/) | Fast dependency management, becoming the standard for MCP Python projects |
| [ruff](https://docs.astral.sh/ruff/) | Replaces flake8 + black + isort in one tool |

---

## License

MIT — see [LICENSE](LICENSE).
