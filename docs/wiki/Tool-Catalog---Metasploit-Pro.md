# Tool Catalog - Metasploit Pro

> These tools are **read-only telemetry**. They do not execute exploits or control sessions.

## Workspaces

### `list_workspaces`

**Use case:** Discover active pentest project scopes.

**Prompts:**

- "List all Metasploit workspaces and summarize their size/activity."
- "Which workspace appears most active based on available counts?"

### `get_workspace`

**Use case:** Inspect one workspace’s host/session/credential footprint.

**Prompts:**

- "Get workspace 1 and summarize host/session/credential counts."
- "Does workspace 2 show evidence of broad compromise scope?"

## Sessions

### `list_sessions`

**Use case:** Track active access channels.

**Prompts:**

- "List active sessions and group by platform and username."
- "Show sessions in workspace 'default' and identify highest-risk access paths."

## Loot

### `get_loot`

**Use case:** Review extracted credentials/artifacts.

**Prompts:**

- "List collected loot and classify by type (hash/password/file)."
- "Show credential-type loot for workspace 'default' and explain potential blast radius."

## Tasks

### `list_msp_tasks`

**Use case:** Monitor background operations.

**Prompts:**

- "List Metasploit tasks and flag any failed operations."
- "Show running tasks and explain what follow-up checks are needed."

## Suggested chaining flow

1. `list_workspaces` → 2. `get_workspace` → 3. `list_sessions` → 4. `get_loot` → 5. `list_msp_tasks`
