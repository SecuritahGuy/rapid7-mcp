"""Pydantic models for InsightVM v3 API request/response schemas."""

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
