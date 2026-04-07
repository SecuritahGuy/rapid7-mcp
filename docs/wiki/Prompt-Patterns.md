# Prompt Patterns

Use these reusable patterns with any tool.

## 1) Discovery prompt

> "Show me what data is available for [scope], and highlight anything high risk."

## 2) Triage prompt

> "From those results, prioritize the top 3 issues by business impact and explain why."

## 3) Action prompt

> "Recommend the next remediation/investigation step and list which tool call should run next."

## 4) Refinement prompt

> "Filter that to only [severity/status/site/time range], and return just the fields [x,y,z]."

## 5) Executive summary prompt

> "Summarize this in 5 bullets for leadership: current risk, active incidents, progress blockers, and next actions."

## Prompt anti-patterns

- Too broad: "Tell me everything about security"
- No scope: "Show vulnerabilities" (without site/asset/severity)
- No objective: "Give data" (without what decision you’re making)

## Better versions

- "List critical vulnerabilities for Production Network with exploit count and remediation status."
- "Show OPEN CRITICAL investigations from the last 24h and recommended analyst next steps."
