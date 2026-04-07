"""Scans router — InsightVM scan management."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightVMClient, get_client
from rapid7_mcp.models import Scan, ScanList

router = APIRouter()


@router.get(
    "",
    response_model=ScanList,
    operation_id="list_scans",
    summary="List scans",
    description=(
        "Returns recent scans across all sites. "
        "Includes scan status (running, finished, stopped, paused), "
        "asset counts, vulnerability findings, and duration."
    ),
)
async def list_scans(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    active: bool | None = Query(None, description="Filter to only active (running) scans"),
    client: InsightVMClient = Depends(get_client),
) -> ScanList:
    params: dict = {"page": page, "size": size}
    if active is not None:
        params["active"] = active
    data = await client.get("/scans", params=params)
    return ScanList(**data)


@router.get(
    "/{scan_id}",
    response_model=Scan,
    operation_id="get_scan",
    summary="Get a scan by ID",
    description="Returns details for a single scan including status, timing, and vulnerability summary.",
)
async def get_scan(
    scan_id: int,
    client: InsightVMClient = Depends(get_client),
) -> Scan:
    data = await client.get(f"/scans/{scan_id}")
    return Scan(**data)
