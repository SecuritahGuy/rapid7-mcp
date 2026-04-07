"""Assets router — InsightVM managed assets."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightVMClient, get_client
from rapid7_mcp.models import Asset, AssetList, AssetSearchRequest, AssetVulnerabilityList

router = APIRouter()


@router.get(
    "/{asset_id}",
    response_model=Asset,
    operation_id="get_asset",
    summary="Get an asset by ID",
    description=(
        "Returns full details for a single asset including IP, hostname, operating system, "
        "vulnerability counts by severity, and risk score."
    ),
)
async def get_asset(
    asset_id: int,
    client: InsightVMClient = Depends(get_client),
) -> Asset:
    data = await client.get(f"/assets/{asset_id}")
    return Asset(**data)


@router.post(
    "/search",
    response_model=AssetList,
    operation_id="search_assets",
    summary="Search assets by filter criteria",
    description=(
        "Search for assets using field filters. "
        "Supported fields: ip-address, host-name, os-family, site-id, tag. "
        "Operators: is, is-not, contains, starts-with, ends-with, like. "
        "Example: filter by IP range or hostname pattern."
    ),
)
async def search_assets(
    body: AssetSearchRequest,
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    client: InsightVMClient = Depends(get_client),
) -> AssetList:
    data = await client.post(
        f"/assets/search?page={page}&size={size}",
        body=body.model_dump(),
    )
    return AssetList(**data)


@router.get(
    "/{asset_id}/vulnerabilities",
    response_model=AssetVulnerabilityList,
    operation_id="get_asset_vulnerabilities",
    summary="List vulnerabilities for an asset",
    description=(
        "Returns all vulnerabilities found on a specific asset, with status and instance counts. "
        "Use the vulnerability ID from results with get_vulnerability for full details."
    ),
)
async def get_asset_vulnerabilities(
    asset_id: int,
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    client: InsightVMClient = Depends(get_client),
) -> AssetVulnerabilityList:
    data = await client.get(
        f"/assets/{asset_id}/vulnerabilities",
        params={"page": page, "size": size},
    )
    return AssetVulnerabilityList(**data)
