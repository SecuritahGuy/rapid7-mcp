"""Asset Groups router — InsightVM logical asset groupings."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightVMClient, get_client
from rapid7_mcp.models import AssetGroup, AssetGroupList

router = APIRouter()


@router.get(
    "",
    response_model=AssetGroupList,
    operation_id="list_asset_groups",
    summary="List asset groups",
    description=(
        "Returns all InsightVM asset groups — logical collections of assets used for scoping, "
        "reporting, and policy. Groups can represent business units, compliance scope (e.g. PCI, "
        "DMZ), or asset criticality tiers. Use this to understand the organizational context "
        "of an asset before assessing its vulnerabilities."
    ),
)
async def list_asset_groups(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    type: str | None = Query(None, description="Filter by group type: static or dynamic"),
    client: InsightVMClient = Depends(get_client),
) -> AssetGroupList:
    params: dict = {"page": page, "size": size}
    if type:
        params["type"] = type
    data = await client.get("/asset_groups", params=params)
    return AssetGroupList(**data)


@router.get(
    "/{group_id}",
    response_model=AssetGroup,
    operation_id="get_asset_group",
    summary="Get an asset group by ID",
    description=(
        "Returns details for a single asset group including name, type, asset count, "
        "and aggregate risk score."
    ),
)
async def get_asset_group(
    group_id: int,
    client: InsightVMClient = Depends(get_client),
) -> AssetGroup:
    data = await client.get(f"/asset_groups/{group_id}")
    return AssetGroup(**data)
