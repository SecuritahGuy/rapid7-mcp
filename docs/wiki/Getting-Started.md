# Getting Started

## Prerequisites

- Python 3.11+
- `uv` installed
- Local clone of this repo

## Run in demo mode

```bash
DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --reload --port 8000
```

- MCP endpoint: `http://localhost:8000/mcp`
- API docs: `http://localhost:8000/docs`

## Connect your MCP client

Use your client’s MCP server config and point it to:

- `http://localhost:8000/mcp`

## Prompting tips

- Ask for a **specific output shape** (table, top 5, grouped by severity)
- Include **scope qualifiers** (site, asset, workspace, time range)
- Ask for a **follow-up action** (recommend remediation, suggest next query)

See [Prompt Patterns](Prompt-Patterns) for reusable prompt templates.
