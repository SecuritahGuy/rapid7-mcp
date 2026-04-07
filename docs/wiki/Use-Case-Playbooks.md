# Use Case Playbooks

## 1) Vulnerability Manager (InsightVM)

**Goal:** Find highest-risk exposure and decide remediation priorities.

**Suggested chain:**

1. `list_sites`
2. `search_assets` (scope to riskiest site)
3. `get_asset_vulnerabilities`
4. `get_vulnerability` (top 3)
5. `list_remediation_projects` / `get_remediation_project`
6. `execute_report`

**Prompt chain example:**

- "List sites by risk score and identify the riskiest."
- "Search assets in that site and show top 10 by risk."
- "For the top asset, list vulnerabilities and rank top 5 by urgency."
- "For the top two vulnerabilities, fetch details and recommend remediations."
- "Check if active remediation projects already cover these findings."
- "Generate an executive report for this remediation sprint."

## 2) SOC Analyst (InsightIDR)

**Goal:** Triage an active incident and validate IoC exposure.

**Suggested chain:**

1. `list_investigations`
2. `get_investigation`
3. `list_indicators`
4. `query_logs`

**Prompt chain example:**

- "List OPEN investigations and rank by priority."
- "Get the highest priority investigation and summarize key alerts."
- "Pull active IOC indicators for IPs/domains relevant to this incident."
- "Search logs for matching IoCs in the last 24h and summarize affected hosts."

## 3) Pentest Telemetry Review (Metasploit)

**Goal:** Understand current operator footholds and collected artifacts.

**Suggested chain:**

1. `list_workspaces`
2. `get_workspace`
3. `list_sessions`
4. `get_loot`
5. `list_msp_tasks`

**Prompt chain example:**

- "List workspaces and identify the most active engagement."
- "Get that workspace and summarize host/session counts."
- "List active sessions and highlight privileged accounts."
- "Show collected credential/hash loot and likely impact if abused."
- "Check task status for running imports or failed jobs."

## 4) Executive Posture Summary (Cross-product)

**Goal:** Provide concise, decision-ready risk snapshot.

**Suggested chain:**

1. `list_sites` / `list_vulnerabilities`
2. `list_investigations`
3. `list_sessions`
4. `list_remediation_projects`

**Prompt chain example:**

- "Summarize top infrastructure risk from sites and critical vulnerabilities."
- "Add current incident pressure from open investigations."
- "Add offensive telemetry context from active Metasploit sessions."
- "Add remediation progress and blockers, then produce a 5-bullet executive brief."
