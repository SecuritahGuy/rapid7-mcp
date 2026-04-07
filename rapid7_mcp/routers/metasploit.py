"""Metasploit Pro router — read-only telemetry from an MSP console.

IMPORTANT: This router is intentionally read-only. No exploit execution,
session interaction, or state mutation is exposed. All tools here provide
situational awareness only — the LLM can see what Metasploit knows, but
a human must initiate any active operations.
"""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import MetasploitClient, get_msp_client
from rapid7_mcp.models import LootList, MspTaskList, SessionList, Workspace, WorkspaceList

router = APIRouter()


@router.get(
    "/workspaces",
    response_model=WorkspaceList,
    operation_id="list_workspaces",
    summary="List Metasploit Pro workspaces",
    description=(
        "Returns all Metasploit Pro workspaces (projects). Each workspace is an isolated "
        "scope containing its own hosts, sessions, credentials, and loot. "
        "Use this to understand what engagements or environments are tracked in Metasploit "
        "before querying sessions or loot."
    ),
)
async def list_workspaces(
    client: MetasploitClient = Depends(get_msp_client),
) -> WorkspaceList:
    data = await client.get("/workspaces")
    return WorkspaceList(**data)


@router.get(
    "/workspaces/{workspace_id}",
    response_model=Workspace,
    operation_id="get_workspace",
    summary="Get a Metasploit Pro workspace",
    description="Returns details for a single workspace including host, session, and credential counts.",
)
async def get_workspace(
    workspace_id: int,
    client: MetasploitClient = Depends(get_msp_client),
) -> Workspace:
    data = await client.get(f"/workspaces/{workspace_id}")
    return Workspace(**data)


@router.get(
    "/sessions",
    response_model=SessionList,
    operation_id="list_sessions",
    summary="List active Metasploit sessions",
    description=(
        "Returns currently active Meterpreter and shell sessions. Each session entry includes "
        "the target host/port, exploit and payload used, platform, username, and last check-in time. "
        "This is read-only — use the Metasploit Pro console to interact with sessions."
    ),
)
async def list_sessions(
    workspace: str | None = Query(None, description="Filter by workspace name"),
    client: MetasploitClient = Depends(get_msp_client),
) -> SessionList:
    params: dict = {}
    if workspace:
        params["workspace"] = workspace
    data = await client.get("/sessions", params=params)
    return SessionList(**data)


@router.get(
    "/loot",
    response_model=LootList,
    operation_id="get_loot",
    summary="List collected loot and credentials",
    description=(
        "Returns credentials, hashes, files, and other artifacts collected from compromised hosts. "
        "Loot entries include the source host/port, service name, data type, and captured content. "
        "Use this to understand what has been extracted during a pentest engagement. "
        "This is read-only — the data has already been collected."
    ),
)
async def get_loot(
    workspace: str | None = Query(None, description="Filter by workspace name"),
    loot_type: str | None = Query(None, description="Filter by loot type (e.g. password, hash)"),
    client: MetasploitClient = Depends(get_msp_client),
) -> LootList:
    params: dict = {}
    if workspace:
        params["workspace"] = workspace
    if loot_type:
        params["type"] = loot_type
    data = await client.get("/looted_credentials", params=params)
    return LootList(**data)


@router.get(
    "/tasks",
    response_model=MspTaskList,
    operation_id="list_msp_tasks",
    summary="List Metasploit Pro background tasks",
    description=(
        "Returns background tasks running in Metasploit Pro — including active scan imports, "
        "bruteforce jobs, and report generation. Check this to see if a vulnerability import "
        "from InsightVM is in progress or has completed."
    ),
)
async def list_msp_tasks(
    status: str | None = Query(None, description="Filter by status: running, completed, failed"),
    client: MetasploitClient = Depends(get_msp_client),
) -> MspTaskList:
    params: dict = {}
    if status:
        params["status"] = status
    data = await client.get("/tasks", params=params)
    return MspTaskList(**data)
