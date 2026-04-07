# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

---

## [0.1.0] — 2026-04-07

### Added

#### InsightVM — Vulnerability Management (17 tools)
- `list_sites` / `get_site` — scan sites with asset counts, risk scores, and last scan times
- `list_asset_groups` / `get_asset_group` — logical asset groupings (static and dynamic)
- `get_asset` — full asset details: IP, hostname, OS, vulnerability counts by severity, risk score
- `search_assets` — filter assets by IP, hostname, OS family, site ID, or tag using InsightVM field filters
- `get_asset_vulnerabilities` — all vulnerabilities found on a specific asset
- `get_asset_tags` — owner, environment, and compliance tags assigned to an asset
- `list_vulnerabilities` / `get_vulnerability` — vulnerability library with CVSS v2/v3, CVEs, exploit count, and description
- `list_scans` / `get_scan` — scan status, timing, asset counts, and vulnerability summaries
- `list_remediation_projects` / `get_remediation_project` — in-flight fix tracking with owner, due date, and scope
- `list_reports` / `get_report` / `execute_report` — browse and trigger InsightVM reports (PDF, HTML, CSV)

#### InsightIDR — SIEM & Investigations (4 tools)
- `list_investigations` — open security incidents with priority, status, and assignee
- `get_investigation` — full alert timeline for a specific investigation
- `query_logs` — LEQL log search across firewall, proxy, DNS, and endpoint log sets
- `list_indicators` — active threat intelligence IOCs (IPs, domains, file hashes, URLs)

#### Metasploit Pro — Pentest Telemetry, read-only (5 tools)
- `list_workspaces` / `get_workspace` — active pentest projects with host and session counts
- `list_sessions` — active Meterpreter and shell sessions with exploit, payload, and platform details
- `get_loot` — credentials, hashes, and files extracted from compromised hosts
- `list_msp_tasks` — background task status (scan imports, report generation)

#### Infrastructure
- Multi-client architecture: separate async HTTP clients for InsightVM (Basic Auth), InsightIDR (`X-Api-Key`), and Metasploit Pro (`X-Metasploit-Token`) — each with a fixture-backed demo counterpart
- `DEMO_MODE=true` returns realistic fixture data for all three products — no live credentials required
- 16 fixture files covering all endpoints across InsightVM, InsightIDR, and Metasploit Pro
- 37 tests covering all routers in demo mode
- GitHub Actions CI: test matrix (Python 3.11, 3.12), ruff lint, mypy type check
- VS Code workspace config (`.vscode/mcp.json`, `.vscode/tasks.json`) for one-command local setup
- `pyproject.toml` managed with `uv`, ruff, and mypy configured

[Unreleased]: https://github.com/SecuritahGuy/rapid7-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SecuritahGuy/rapid7-mcp/releases/tag/v0.1.0
