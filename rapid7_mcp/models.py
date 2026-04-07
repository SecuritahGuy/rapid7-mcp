"""Pydantic models for InsightVM, InsightIDR, and Metasploit Pro API schemas."""

from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Shared / pagination
# ---------------------------------------------------------------------------


class PageInfo(BaseModel):
    number: int = 0
    size: int = 10
    total_pages: int = Field(0, alias="totalPages")
    total_resources: int = Field(0, alias="totalResources")

    model_config = {"populate_by_name": True}


class Link(BaseModel):
    rel: str
    href: str


# ---------------------------------------------------------------------------
# Sites
# ---------------------------------------------------------------------------


class Site(BaseModel):
    id: int
    name: str
    description: str | None = None
    assets: int = 0
    last_scan_time: str | None = Field(None, alias="lastScanTime")
    risk_score: float = Field(0.0, alias="riskScore")
    scan_template: str | None = Field(None, alias="scanTemplate")
    type: str | None = None
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class SiteList(BaseModel):
    page: PageInfo
    resources: list[Site]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------


class OperatingSystem(BaseModel):
    description: str | None = None
    family: str | None = None
    name: str | None = None
    vendor: str | None = None
    version: str | None = None


class VulnerabilityCounts(BaseModel):
    critical: int = 0
    exploits: int = 0
    high: int = 0
    info: int = 0
    low: int = 0
    malware_kits: int = Field(0, alias="malwareKits")
    medium: int = 0
    severe: int = 0
    total: int = 0

    model_config = {"populate_by_name": True}


class Asset(BaseModel):
    id: int
    ip: str | None = None
    host_name: str | None = Field(None, alias="hostName")
    os: OperatingSystem | None = None
    vulnerabilities: VulnerabilityCounts | None = None
    risk_score: float = Field(0.0, alias="riskScore")
    last_scan_time: str | None = Field(None, alias="lastScanTime")
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class AssetList(BaseModel):
    page: PageInfo
    resources: list[Asset]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Asset search
# ---------------------------------------------------------------------------


class SearchCriterion(BaseModel):
    field: str
    operator: str
    value: str


class AssetSearchRequest(BaseModel):
    filters: list[SearchCriterion] = []
    match: str = "all"


# ---------------------------------------------------------------------------
# Vulnerabilities
# ---------------------------------------------------------------------------


class CvssScore(BaseModel):
    access_complexity: str | None = Field(None, alias="accessComplexity")
    access_vector: str | None = Field(None, alias="accessVector")
    authentication: str | None = None
    availability_impact: str | None = Field(None, alias="availabilityImpact")
    confidentiality_impact: str | None = Field(None, alias="confidentialityImpact")
    exploit_score: float | None = Field(None, alias="exploitScore")
    impact_score: float | None = Field(None, alias="impactScore")
    integrity_impact: str | None = Field(None, alias="integrityImpact")
    score: float | None = None
    vector: str | None = None

    model_config = {"populate_by_name": True}


class Cvss(BaseModel):
    v2: CvssScore | None = None
    v3: CvssScore | None = None


class Vulnerability(BaseModel):
    id: str
    title: str
    description: str | None = None
    severity: str | None = None
    severity_score: float | None = Field(None, alias="severityScore")
    risk_score: float | None = Field(None, alias="riskScore")
    cvss: Cvss | None = None
    cvss_v2: float | None = Field(None, alias="cvssV2Score")
    cvss_v3: float | None = Field(None, alias="cvssV3Score")
    exploits: int = 0
    malware_kits: int = Field(0, alias="malwareKits")
    published: str | None = None
    added: str | None = None
    modified: str | None = None
    categories: list[str] = []
    cves: list[str] = []
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class VulnerabilityList(BaseModel):
    page: PageInfo
    resources: list[Vulnerability]
    links: list[Link] = []


class AssetVulnerability(BaseModel):
    id: str
    instances: int = 0
    results: list[Any] = []
    since: str | None = None
    status: str | None = None
    links: list[Link] = []


class AssetVulnerabilityList(BaseModel):
    page: PageInfo
    resources: list[AssetVulnerability]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Scans
# ---------------------------------------------------------------------------


class Scan(BaseModel):
    id: int
    site_id: int = Field(0, alias="siteId")
    site_name: str | None = Field(None, alias="siteName")
    scan_name: str | None = Field(None, alias="scanName")
    status: str | None = None
    start_time: str | None = Field(None, alias="startTime")
    end_time: str | None = Field(None, alias="endTime")
    duration: str | None = None
    assets_scanned: int = Field(0, alias="assets")
    vulnerabilities: VulnerabilityCounts | None = None
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class ScanList(BaseModel):
    page: PageInfo
    resources: list[Scan]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Asset Groups (InsightVM)
# ---------------------------------------------------------------------------


class AssetGroup(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: str | None = None
    assets: int = 0
    risk_score: float = Field(0.0, alias="riskScore")
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class AssetGroupList(BaseModel):
    page: PageInfo
    resources: list[AssetGroup]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Asset Tags (InsightVM)
# ---------------------------------------------------------------------------


class AssetTag(BaseModel):
    id: int
    name: str
    color: str | None = None
    tag_type: str | None = Field(None, alias="type")
    created_by: str | None = Field(None, alias="createdBy")
    risk_modifier: str | None = Field(None, alias="riskModifier")
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class AssetTagList(BaseModel):
    page: PageInfo
    resources: list[AssetTag]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Remediation Projects (InsightVM)
# ---------------------------------------------------------------------------


class RemediationProject(BaseModel):
    id: int
    name: str
    description: str | None = None
    status: str | None = None
    owner: str | None = None
    due_date: str | None = Field(None, alias="dueDate")
    completed: bool = False
    asset_count: int = Field(0, alias="assets")
    vulnerability_count: int = Field(0, alias="vulnerabilities")
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class RemediationProjectList(BaseModel):
    page: PageInfo
    resources: list[RemediationProject]
    links: list[Link] = []


# ---------------------------------------------------------------------------
# Reports (InsightVM)
# ---------------------------------------------------------------------------


class Report(BaseModel):
    id: int
    name: str
    format: str | None = None
    status: str | None = None
    scope: dict | None = None
    template: str | None = None
    uri: str | None = None
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class ReportList(BaseModel):
    page: PageInfo
    resources: list[Report]
    links: list[Link] = []


class ReportGenerateResponse(BaseModel):
    id: int
    status: str
    uri: str | None = None
    links: list[Link] = []

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# InsightIDR — Investigations
# ---------------------------------------------------------------------------


class InvestigationAlert(BaseModel):
    id: str | None = None
    alert_type: str | None = None
    alert_type_description: str | None = None
    first_event_time: str | None = None
    risk_score: int | None = None

    model_config = {"populate_by_name": True}


class Investigation(BaseModel):
    id: str
    title: str
    status: str
    priority: str
    assignee: dict | None = None
    source: str | None = None
    disposition: str | None = None
    alerts: list[InvestigationAlert] = []
    created_time: str | None = None
    last_accessed: str | None = None
    responsibility: str | None = None
    rrn: str | None = None

    model_config = {"populate_by_name": True}


class InvestigationList(BaseModel):
    data: list[Investigation] = []
    metadata: dict = {}


# ---------------------------------------------------------------------------
# InsightIDR — Log Search (LEQL)
# ---------------------------------------------------------------------------


class LogSearchRequest(BaseModel):
    query: str
    from_time: int | None = None
    to_time: int | None = None
    logs: list[str] = []


class LogEntry(BaseModel):
    message: str
    timestamp: int | None = None
    log_id: str | None = None
    sequence_number: int | None = None

    model_config = {"populate_by_name": True}


class LogSearchResults(BaseModel):
    id: str | None = None
    leql: dict | None = None
    logs: list[str] = []
    events: list[LogEntry] = []


# ---------------------------------------------------------------------------
# InsightIDR — Threat Intelligence / IOCs
# ---------------------------------------------------------------------------


class Indicator(BaseModel):
    id: str | None = None
    indicator_value: str
    indicator_type: str
    source: str | None = None
    threat: str | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    active: bool = True

    model_config = {"populate_by_name": True}


class IndicatorList(BaseModel):
    data: list[Indicator] = []
    metadata: dict = {}


# ---------------------------------------------------------------------------
# Metasploit Pro — Workspaces
# ---------------------------------------------------------------------------


class Workspace(BaseModel):
    id: int
    name: str
    description: str | None = None
    boundary: str | None = None
    limit_to_network: bool = False
    hosts_count: int = 0
    credentials_count: int = 0
    sessions_count: int = 0

    model_config = {"populate_by_name": True}


class WorkspaceList(BaseModel):
    data: list[Workspace] = []


# ---------------------------------------------------------------------------
# Metasploit Pro — Sessions
# ---------------------------------------------------------------------------


class Session(BaseModel):
    id: int
    session_type: str | None = None
    tunnel_local: str | None = None
    tunnel_peer: str | None = None
    via_exploit: str | None = None
    via_payload: str | None = None
    desc: str | None = None
    info: str | None = None
    workspace: str | None = None
    target_host: str | None = None
    target_port: int | None = None
    username: str | None = None
    uuid: str | None = None
    opened_at: str | None = None
    last_checkin: str | None = None
    platform: str | None = None
    arch: str | None = None
    os_name: str | None = None

    model_config = {"populate_by_name": True}


class SessionList(BaseModel):
    data: list[Session] = []


# ---------------------------------------------------------------------------
# Metasploit Pro — Loot / Credentials
# ---------------------------------------------------------------------------


class LootEntry(BaseModel):
    id: int
    host: str | None = None
    port: int | None = None
    service_name: str | None = None
    loot_type: str | None = None
    data: str | None = None
    content_type: str | None = None
    name: str | None = None
    info: str | None = None
    workspace: str | None = None
    created_at: str | None = None

    model_config = {"populate_by_name": True}


class LootList(BaseModel):
    data: list[LootEntry] = []


# ---------------------------------------------------------------------------
# Metasploit Pro — Tasks
# ---------------------------------------------------------------------------


class MspTask(BaseModel):
    id: int
    status: str | None = None
    task_type: str | None = None
    description: str | None = None
    progress: int = 0
    workspace: str | None = None
    created_at: str | None = None
    completed_at: str | None = None
    error: str | None = None

    model_config = {"populate_by_name": True}


class MspTaskList(BaseModel):
    data: list[MspTask] = []
