# Troubleshooting & FAQ

## I get no results

- Confirm `DEMO_MODE=true` for local testing
- Check filters are not too narrow (severity/status/site)
- Retry without optional filters to validate base connectivity

## Authentication failures

- InsightVM uses username/password
- InsightIDR uses API key + region
- Metasploit Pro uses token

Verify values in `.env` and restart the server.

## Pagination confusion

- InsightVM endpoints generally use `page` + `size`
- InsightIDR investigations use cursor-style pagination (`page_token` semantics)

## Severity vs risk vs CVSS

- **Severity**: categorical label (Critical/Severe/Moderate/...)
- **Severity score**: normalized numeric severity
- **Risk score**: contextual/platform risk scoring
- **CVSS**: standardized vulnerability scoring model

## Is Metasploit control supported?

No. The Metasploit toolset is intentionally **read-only telemetry** in this project.

## Why does report generation feel async?

`execute_report` starts generation and returns report instance metadata/URI. Depending on environment load, artifact availability may lag.
