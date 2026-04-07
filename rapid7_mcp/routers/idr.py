"""InsightIDR router — cloud SIEM investigations and log search."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightIDRClient, get_idr_client
from rapid7_mcp.models import (
    IndicatorList,
    Investigation,
    InvestigationList,
    LogSearchRequest,
    LogSearchResults,
)

router = APIRouter()


@router.get(
    "/investigations",
    response_model=InvestigationList,
    operation_id="list_investigations",
    summary="List InsightIDR investigations",
    description=(
        "Returns InsightIDR investigations (security incidents). Each investigation aggregates "
        "related alerts with an assigned priority, status, and optional assignee. "
        "Filter by status to focus on open incidents requiring attention. "
        "Use get_investigation for the full alert timeline."
    ),
)
async def list_investigations(
    status: str = Query("OPEN", description="Filter by status: OPEN, CLOSED, INVESTIGATING"),
    priority: str | None = Query(
        None, description="Filter by priority: CRITICAL, HIGH, MEDIUM, LOW"
    ),
    page_token: str | None = Query(None, description="Pagination cursor from previous response"),
    size: int = Query(20, ge=1, le=100),
    client: InsightIDRClient = Depends(get_idr_client),
) -> InvestigationList:
    params: dict = {"statuses": status, "size": size}
    if priority:
        params["priorities"] = priority
    if page_token:
        params["index"] = page_token
    data = await client.get("/idr/v2/investigations", params=params)
    return InvestigationList(**data)


@router.get(
    "/investigations/{investigation_id}",
    response_model=Investigation,
    operation_id="get_investigation",
    summary="Get an investigation by ID",
    description=(
        "Returns full details for a single InsightIDR investigation including all associated alerts, "
        "timeline, assignee, priority, and disposition. Use this to understand the full context "
        "of an active security incident."
    ),
)
async def get_investigation(
    investigation_id: str,
    client: InsightIDRClient = Depends(get_idr_client),
) -> Investigation:
    data = await client.get(f"/idr/v2/investigations/{investigation_id}")
    return Investigation(**data)


@router.post(
    "/logs",
    response_model=LogSearchResults,
    operation_id="query_logs",
    summary="Search logs with LEQL",
    description=(
        "Execute a LEQL (Log Entry Query Language) query against InsightIDR log sets. "
        "Use this to hunt for indicators of compromise — search for specific IPs, file hashes, "
        "domain names, or user activity across firewall, proxy, DNS, and endpoint logs. "
        "Example LEQL: 'where(destination_ip = \"1.2.3.4\")'. "
        "Time range is specified as Unix epoch milliseconds."
    ),
)
async def query_logs(
    body: LogSearchRequest,
    client: InsightIDRClient = Depends(get_idr_client),
) -> LogSearchResults:
    payload: dict = {"leql": {"statement": body.query}}
    if body.from_time:
        payload["from"] = body.from_time
    if body.to_time:
        payload["to"] = body.to_time
    if body.logs:
        payload["logs"] = body.logs
    data = await client.post("/log_search/query/logs", body=payload)
    return LogSearchResults(**data)


@router.get(
    "/iocs",
    response_model=IndicatorList,
    operation_id="list_indicators",
    summary="List threat intelligence indicators (IOCs)",
    description=(
        "Returns active Indicators of Compromise (IOCs) being tracked in InsightIDR's threat "
        "intelligence feed. Indicators include malicious IPs, domains, file hashes, and URLs "
        "associated with known threat actors or malware families. "
        "Use this to check whether an IP or domain seen in logs is a known bad actor."
    ),
)
async def list_indicators(
    indicator_type: str | None = Query(
        None,
        description="Filter by type: IP_ADDRESS, DOMAIN, URL, FILE_HASH",
    ),
    client: InsightIDRClient = Depends(get_idr_client),
) -> IndicatorList:
    params: dict = {}
    if indicator_type:
        params["type"] = indicator_type
    data = await client.get("/idr/v2/iocs", params=params)
    return IndicatorList(**data)
