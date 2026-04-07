# Demo Mode Scenarios

All scenarios below work with `DEMO_MODE=true`.

## Scenario 1: Highest-risk site triage

1. Ask: "List sites by risk score."
2. Ask: "For the top site, show top assets by risk."
3. Ask: "For top asset, list vulnerabilities and prioritize fixes."

Expected: Production/Cloud-style high-risk ordering and actionable remediation narrative.

## Scenario 2: Log4Shell exposure check

1. Ask: "Find vulnerabilities related to Log4j or CVE-2021-44228."
2. Ask: "Get detailed vulnerability info and exploit context."
3. Ask: "Check if remediation projects already cover this issue."

Expected: Log4Shell appears with high severity/impact context.

## Scenario 3: Active incident + IoC correlation

1. Ask: "List OPEN investigations."
2. Ask: "Get highest priority investigation details."
3. Ask: "Search logs for suspicious destination IP 185.220.101.1."

Expected: Investigation + log hit correlation summary.

## Scenario 4: Metasploit telemetry snapshot

1. Ask: "List workspaces and active sessions."
2. Ask: "Show collected loot and classify by type."
3. Ask: "List running/failed tasks."

Expected: Read-only compromise footprint view.

## Scenario 5: Executive summary in 5 bullets

Ask:
"Create a 5-bullet executive summary combining current site risk, critical vulnerabilities, open investigations, active sessions, and remediation project status."

Expected: concise posture + next actions.
