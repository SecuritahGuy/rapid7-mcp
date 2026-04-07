# rapid7-mcp

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/SecuritahGuy/rapid7-mcp/actions/workflows/ci.yml/badge.svg)

A unified MCP server for Rapid7's security platform — exposing [InsightVM](https://www.rapid7.com/products/insightvm/) (vulnerability management), [InsightIDR](https://www.rapid7.com/products/insightidr/) (SIEM/investigations), and [Metasploit Pro](https://www.rapid7.com/products/metasploit/) (pentest telemetry) as tools for Claude, Cursor, and any MCP-compatible LLM client.

Ask natural-language questions across your entire Rapid7 environment — vulnerabilities, active incidents, compromised hosts — and get structured answers without writing a single API call.

Built with [fastapi-mcp](https://github.com/tadata-ru/fastapi-mcp), [FastAPI](https://fastapi.tiangolo.com/), and [httpx](https://www.python-httpx.org/).

> **No Rapid7 instance?** Set `DEMO_MODE=true` to explore all 22 tools against realistic fixture data. Clone, run, connect — no credentials required.

---

## What you can do

Once connected to Claude, you can ask things like:

> _"Which of my sites has the highest risk score?"_
> _"What are the critical vulnerabilities on the production web server, and is there already a remediation project for them?"_
> _"Is Log4Shell present anywhere in my environment? Show me the CVSS score and any available exploits."_
> _"Are there any open InsightIDR investigations right now? What's the highest priority one?"_
> _"Search our logs for any connections to this IP address: 185.220.101.1"_
> _"What active Metasploit sessions exist and what hosts were compromised?"_
> _"Give me a full security posture summary across sites, open incidents, and active sessions."_

The server translates these into API calls across InsightVM, InsightIDR, and Metasploit Pro and returns structured data that Claude can reason over, correlate, and summarize.

---

## Architecture

```text
Claude / Cursor / MCP Client
        │  MCP (Streamable HTTP)
        ▼
┌───────────────────────────────────────────┐
│  FastAPI + fastapi-mcp  :8000             │
│                                           │
│  InsightVM        InsightIDR    MSP       │
│  ──────────────   ──────────    ───────── │
│  /sites           /idr/invest.  /workspcs │
│  /assets          /idr/logs     /sessions │
│  /asset_groups    /idr/iocs     /loot     │
│  /vulnerabilities                /tasks   │
│  /scans                                   │
│  /remediation_projects                    │
│  /reports                                 │
│                                           │
│  /mcp  ← MCP endpoint                    │
└──────┬──────────────┬──────────┬──────────┘
       │ Basic Auth   │ X-Api-Key│ Token
       ▼              ▼          ▼
  InsightVM      InsightIDR   Metasploit
  Console        Cloud API    Pro Console
  :3780          (regional)   :3790
```

Every FastAPI route is automatically published as an MCP tool via `fastapi-mcp`. Operation IDs become tool names, Pydantic schemas become input/output schemas, and docstrings become tool descriptions.

---

## Quick Start

**Prerequisites:** Python 3.11+, [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# 1. Clone and install
git clone https://github.com/SecuritahGuy/rapid7-mcp.git
cd rapid7-mcp
uv sync

# 2. Configure (or skip and use DEMO_MODE)
cp .env.example .env
# edit .env with your console URLs and credentials

# 3. Start the server
DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --port 8000
```

- MCP endpoint: `http://localhost:8000/mcp`
- Interactive API docs: `http://localhost:8000/docs`

---

## Connect to VS Code

Add `.vscode/mcp.json` to your workspace (already included in this repo):

```json
{
  "servers": {
    "rapid7-mcp": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Start the server first (`Ctrl+Shift+P` → **Tasks: Run Task** → **Start MCP Server (Demo Mode)**), then connect in the Claude Code panel.

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

Start the server first, then restart Claude Desktop.

---

## Available MCP Tools

### InsightVM — Vulnerability Management

| Tool | Description |
| --- | --- |
| `list_sites` | List all scan sites — names, asset counts, risk scores, last scan time |
| `get_site` | Full details for a single site |
| `list_asset_groups` | Logical asset groupings (PCI scope, DMZ, dynamic OS groups) |
| `get_asset_group` | Details for a single asset group |
| `get_asset` | Asset details — IP, hostname, OS, vulnerability counts by severity, risk score |
| `search_assets` | Filter assets by IP, hostname, OS family, site ID, or tag |
| `get_asset_vulnerabilities` | All vulnerabilities found on a specific asset |
| `get_asset_tags` | Owner, environment, and compliance tags assigned to an asset |
| `list_vulnerabilities` | Browse the vulnerability library, filter by severity |
| `get_vulnerability` | Full vuln details — CVSS v2/v3, CVEs, exploit count, description |
| `list_scans` | Recent scans with status, duration, and vulnerability summaries |
| `get_scan` | Details for a single scan |
| `list_remediation_projects` | In-flight fix tracking — owner, due date, affected assets |
| `get_remediation_project` | Details for a single remediation project |
| `list_reports` | All configured reports (executive summaries, PCI exports, CSV) |
| `get_report` | Configuration and status for a single report |
| `execute_report` | Trigger on-demand report generation, returns download URI |

### InsightIDR — SIEM & Investigations

| Tool | Description |
| --- | --- |
| `list_investigations` | Open security incidents — priority, status, assignee, alert summary |
| `get_investigation` | Full alert timeline for a specific investigation |
| `query_logs` | LEQL search across firewall, proxy, DNS, and endpoint logs |
| `list_indicators` | Active threat intelligence IOCs — IPs, domains, hashes, URLs |

### Metasploit Pro — Pentest Telemetry (read-only)

> These tools are intentionally read-only. The LLM can see what Metasploit knows — active sessions, collected credentials, task status — but cannot execute exploits or interact with sessions.

| Tool | Description |
| --- | --- |
| `list_workspaces` | All Metasploit Pro workspaces (pentest projects) |
| `get_workspace` | Details for a single workspace |
| `list_sessions` | Active Meterpreter and shell sessions — host, exploit, platform, username |
| `get_loot` | Credentials, hashes, and files extracted from compromised hosts |
| `list_msp_tasks` | Background tasks — scan imports, report generation, bruteforce jobs |

---

## Demo Mode

`DEMO_MODE=true` replaces all API calls with fixture data across all three products. No console, no credentials, no VPN.

Fixtures in [`tests/fixtures/`](tests/fixtures/):

| Fixture | Contents |
| --- | --- |
| `sites.json` / `site.json` | 3 sites: Production, Development, Cloud |
| `assets.json` / `asset.json` | Ubuntu and RHEL hosts with full vulnerability breakdowns |
| `asset_groups.json` / `asset_group.json` | PCI Scope, DMZ, Critical Infra, All Linux groups |
| `asset_tags.json` | Owner, environment, and compliance tags |
| `vulnerabilities.json` / `vulnerability.json` | Log4Shell, OpenSSL CVE-2022-0778, POODLE |
| `asset_vulnerabilities.json` | Vulnerabilities scoped to a single asset |
| `scans.json` / `scan.json` | One finished scan, one running |
| `remediation_projects.json` / `remediation_project.json` | Q1 patching sprint, Log4Shell project |
| `reports.json` / `report.json` / `report_generate.json` | Executive summary, PCI report, CSV export |
| `investigations.json` / `investigation.json` | PowerShell execution alert, SSH brute force |
| `log_search_results.json` | Firewall and proxy hits for a Tor exit node IP |
| `indicators.json` | Tor IP, Cobalt Strike hash, APT28 C2 domain |
| `workspaces.json` / `workspace.json` | Default workspace + Q1 external pentest |
| `sessions.json` | Meterpreter (SYSTEM) + shell (tomcat) sessions |
| `loot.json` | NTLM hashes + PostgreSQL credentials |
| `msp_tasks.json` | Completed InsightVM import + running report task |

---

## Configuration

All settings via environment variable or `.env` file. Copy `.env.example` to get started.

### InsightVM

| Variable | Default | Description |
| --- | --- | --- |
| `R7_CONSOLE_URL` | `https://localhost:3780` | InsightVM console base URL |
| `R7_USERNAME` | `admin` | InsightVM user (Global Administrator role required) |
| `R7_PASSWORD` | `password` | InsightVM password |
| `R7_VERIFY_SSL` | `false` | Set to `true` if your console has a valid certificate |

### InsightIDR

| Variable | Default | Description |
| --- | --- | --- |
| `IDR_REGION` | `us` | Insight Platform region: `us`, `us2`, `us3`, `eu`, `ca`, `au`, `ap` |
| `IDR_API_KEY` | _(empty)_ | Insight Platform API key |

### Metasploit Pro

| Variable | Default | Description |
| --- | --- | --- |
| `MSP_URL` | `https://localhost:3790` | Metasploit Pro console base URL |
| `MSP_TOKEN` | _(empty)_ | MSP REST API token |
| `MSP_VERIFY_SSL` | `false` | Set to `true` if your MSP console has a valid certificate |

### General

| Variable | Default | Description |
| --- | --- | --- |
| `DEMO_MODE` | `false` | Return fixture data for all products; skips all live connectivity |

---

## Development

```bash
uv sync                                          # install deps + dev extras
uv run pytest --cov=rapid7_mcp tests/           # run tests with coverage
uv run ruff check . && uv run ruff format .      # lint + format
uv run mypy rapid7_mcp/                          # type check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new tool, extend fixtures, and open a pull request.

## Community & Project Health

- [Security policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing guide](CONTRIBUTING.md)
- [Issue templates](.github/ISSUE_TEMPLATE/)
- [Pull request template](.github/pull_request_template.md)
- [Repository hardening checklist](.github/REPOSITORY_HARDENING.md)
- [Wiki starter docs](docs/wiki/Home.md)

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
