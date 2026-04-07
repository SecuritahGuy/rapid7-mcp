# Tool Catalog - InsightIDR

This page covers InsightIDR investigation and log-hunting tools.

## Investigations

### `list_investigations`

**Use case:** Triage open incidents by priority.

**Prompts:**

- "List OPEN investigations and prioritize CRITICAL/HIGH first."
- "Show current investigations and tell me which one should be handled first."

### `get_investigation`

**Use case:** Deep-dive a single incident timeline.

**Prompts:**

- "Get investigation [id] and summarize timeline, alerts, and likely root cause."
- "For investigation [id], what should an analyst do in the next 30 minutes?"

## Log Search

### `query_logs`

**Use case:** Hunt IoCs and suspicious activity with LEQL.

**Prompts:**

- "Query logs for destination_ip 185.220.101.1 in the last 24h and summarize hits by source host."
- "Search logs for repeated failed SSH activity and identify top offending IPs."

## Threat Intelligence

### `list_indicators`

**Use case:** Pull known-bad IoCs from active feeds.

**Prompts:**

- "List IOC indicators of type DOMAIN and summarize notable threats."
- "Show active IP_ADDRESS indicators and suggest how to validate exposure in logs."

## Suggested chaining flow

1. `list_investigations` → 2. `get_investigation` → 3. `list_indicators` → 4. `query_logs`
