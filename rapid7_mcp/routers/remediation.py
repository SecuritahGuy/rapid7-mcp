"""Remediation router — InsightVM remediation projects."""

from fastapi import APIRouter, Depends, Query

from rapid7_mcp.client import InsightVMClient, get_client
from rapid7_mcp.models import RemediationProject, RemediationProjectList

router = APIRouter()


@router.get(
    "",
    response_model=RemediationProjectList,
    operation_id="list_remediation_projects",
    summary="List remediation projects",
    description=(
        "Returns all InsightVM remediation projects — tracked work items for fixing vulnerabilities. "
        "Each project has an owner, due date, status, and a scoped set of assets and vulnerabilities. "
        "Use this to check whether a vulnerability already has a remediation effort in progress "
        "before recommending new action."
    ),
)
async def list_remediation_projects(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    status: str | None = Query(None, description="Filter by status: active, closed"),
    client: InsightVMClient = Depends(get_client),
) -> RemediationProjectList:
    params: dict = {"page": page, "size": size}
    if status:
        params["status"] = status
    data = await client.get("/remediation_projects", params=params)
    return RemediationProjectList(**data)


@router.get(
    "/{project_id}",
    response_model=RemediationProject,
    operation_id="get_remediation_project",
    summary="Get a remediation project by ID",
    description=(
        "Returns full details for a remediation project including owner, due date, "
        "completion status, and counts of affected assets and vulnerabilities."
    ),
)
async def get_remediation_project(
    project_id: int,
    client: InsightVMClient = Depends(get_client),
) -> RemediationProject:
    data = await client.get(f"/remediation_projects/{project_id}")
    return RemediationProject(**data)
