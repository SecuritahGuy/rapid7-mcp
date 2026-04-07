# Tool Catalog - InsightVM

This page covers all InsightVM tools exposed by `rapid7-mcp`.

## Sites

### `list_sites`

**Use case:** Identify highest-risk environments.

**Prompts:**

- "List all sites with asset count and risk score, sorted by highest risk first."
- "Which site looks riskiest right now, and why?"

### `get_site`

**Use case:** Deep dive into one environment.

**Prompts:**

- "Get site 1 and summarize its risk posture."
- "Show key details for site 3 and what I should investigate next."

## Assets

### `get_asset`

**Use case:** Inspect a specific host.

**Prompts:**

- "Get asset 1 and summarize OS, risk score, and vulnerability breakdown."
- "Is asset 2 a priority for remediation? Explain using its risk and severity counts."

### `search_assets`

**Use case:** Find assets by hostname, IP, site, tag, or OS family.

**Prompts:**

- "Search for assets where host-name contains 'prod' and return top 10 by risk score."
- "Find assets in site-id 1 with os-family is Linux and summarize counts by severity."

### `get_asset_vulnerabilities`

**Use case:** Review findings on one host.

**Prompts:**

- "List vulnerabilities for asset 1 and prioritize the top 5 by severity and exploitability."
- "For asset 1, show vulnerabilities that should be fixed first and why."

### `get_asset_tags`

**Use case:** Add business context before prioritization.

**Prompts:**

- "Get tags for asset 1 and explain what business context they add."
- "Use asset 1 tags to suggest remediation urgency (e.g., prod/PCI)."

## Asset Groups

### `list_asset_groups`

**Use case:** Understand organizational/compliance scoping.

**Prompts:**

- "List all asset groups and identify the highest-risk group."
- "Show only dynamic asset groups and explain what they likely represent."

### `get_asset_group`

**Use case:** Evaluate one group’s risk concentration.

**Prompts:**

- "Get asset group 1 and summarize risk score, type, and asset count."
- "Is asset group 2 a hotspot? Explain using available metrics."

## Vulnerabilities

### `list_vulnerabilities`

**Use case:** Review library-level high-risk exposure.

**Prompts:**

- "List Critical vulnerabilities and highlight those with known exploits."
- "Show top vulnerabilities by risk score and CVSS v3 score."

### `get_vulnerability`

**Use case:** Deep-dive one vuln (CVEs, CVSS, exploit context).

**Prompts:**

- "Get vulnerability log4j-cve-2021-44228 and summarize business impact."
- "Explain remediation urgency for openssl-cve-2022-0778 using CVSS and exploit data."

## Scans

### `list_scans`

**Use case:** Monitor scan activity and freshness.

**Prompts:**

- "List recent scans and flag any that are still running or failed."
- "Show active scans and estimate where follow-up triage is needed."

### `get_scan`

**Use case:** Inspect one scan result and finding density.

**Prompts:**

- "Get scan 101 and summarize critical/high findings."
- "From scan 102, what should the team do immediately?"

## Remediation Projects

### `list_remediation_projects`

**Use case:** Track remediation progress and ownership.

**Prompts:**

- "List active remediation projects with due dates and vuln counts."
- "Which remediation project is most at risk of missing deadline impact?"

### `get_remediation_project`

**Use case:** Validate project scope and urgency.

**Prompts:**

- "Get remediation project 1 and summarize owner, deadline, and scope."
- "Is project 2 sufficient to cover current risk?"

## Reports

### `list_reports`

**Use case:** Discover available reporting outputs.

**Prompts:**

- "List all configured reports and their formats."
- "Which existing report is best for executive risk visibility?"

### `get_report`

**Use case:** Inspect one report configuration/status.

**Prompts:**

- "Get report 1 and explain its audience and use."
- "Check report 3 status and whether it’s ready for distribution."

### `execute_report`

**Use case:** Trigger report generation on demand.

**Prompts:**

- "Execute report 1 and tell me what output URI was returned."
- "Generate report 2 and summarize next steps to retrieve/share it."

## Suggested chaining flow

1. `list_sites` → 2. `search_assets` / `get_asset` → 3. `get_asset_vulnerabilities` → 4. `get_vulnerability` → 5. `list_remediation_projects` / `execute_report`
