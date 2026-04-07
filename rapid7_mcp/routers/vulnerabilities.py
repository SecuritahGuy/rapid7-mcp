"""Vulnerabilities router — InsightVM vulnerability library."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightVMClient, get_client
from rapid7_mcp.models import Vulnerability, VulnerabilityList

router = APIRouter()


@router.get(
    "",
    response_model=VulnerabilityList,
    operation_id="list_vulnerabilities",
    summary="List vulnerabilities",
    description=(
        "Returns vulnerabilities from the InsightVM library. "
        "Filter by severity (Critical, Severe, Moderate, Low, Informational) to narrow results. "
        "Results include CVSS scores, CVE IDs, and exploit availability."
    ),
)
async def list_vulnerabilities(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    severity: str | None = Query(
        None,
        description="Filter by severity: Critical, Severe, Moderate, Low, Informational",
    ),
    client: InsightVMClient = Depends(get_client),
) -> VulnerabilityList:
    params: dict = {"page": page, "size": size}
    if severity:
        params["severity"] = severity
    data = await client.get("/vulnerabilities", params=params)
    return VulnerabilityList(**data)


@router.get(
    "/{vuln_id}",
    response_model=Vulnerability,
    operation_id="get_vulnerability",
    summary="Get vulnerability details",
    description=(
        "Returns full details for a vulnerability including title, description, CVSS v2/v3 scores, "
        "CVE IDs, affected software categories, exploit count, and available remediations."
    ),
)
async def get_vulnerability(
    vuln_id: str,
    client: InsightVMClient = Depends(get_client),
) -> Vulnerability:
    data = await client.get(f"/vulnerabilities/{vuln_id}")
    return Vulnerability(**data)
