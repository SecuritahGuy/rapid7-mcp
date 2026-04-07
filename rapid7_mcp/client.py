"""Async HTTP clients for Rapid7 InsightVM, InsightIDR, and Metasploit Pro."""

import json
from pathlib import Path
from typing import Any

import httpx
from fastapi import Depends

from rapid7_mcp.config import Settings, get_settings

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures"

_EMPTY_PAGE = {
    "resources": [],
    "page": {"number": 0, "size": 0, "totalPages": 0, "totalResources": 0},
}


def _load_fixture(name: str) -> dict[str, Any]:
    path = FIXTURES_DIR / name
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# InsightVM fixture resolution
# ---------------------------------------------------------------------------


def _resolve_vm_fixture(method: str, path: str) -> str | None:
    """Map an InsightVM API path to a fixture filename."""
    clean = path.split("?")[0].rstrip("/")
    parts = [p for p in clean.split("/") if p]

    if method == "POST" and clean == "/assets/search":
        return "assets.json"

    if not parts:
        return None

    root = parts[0]

    if root == "sites":
        return "sites.json" if len(parts) == 1 else "site.json"

    if root == "asset_groups":
        return "asset_groups.json" if len(parts) == 1 else "asset_group.json"

    if root == "assets" and len(parts) == 3 and parts[2] == "vulnerabilities":
        return "asset_vulnerabilities.json"

    if root == "assets" and len(parts) == 3 and parts[2] == "tags":
        return "asset_tags.json"

    if root == "assets" and len(parts) == 2:
        return "asset.json"

    if root == "vulnerabilities":
        return "vulnerabilities.json" if len(parts) == 1 else "vulnerability.json"

    if root == "scans":
        return "scans.json" if len(parts) == 1 else "scan.json"

    if root == "remediation_projects":
        return "remediation_projects.json" if len(parts) == 1 else "remediation_project.json"

    if root == "reports":
        if len(parts) == 1:
            return "reports.json"
        if len(parts) == 3 and parts[2] == "generate":
            return "report_generate.json"
        return "report.json"

    return None


# ---------------------------------------------------------------------------
# InsightIDR fixture resolution
# ---------------------------------------------------------------------------


def _resolve_idr_fixture(method: str, path: str) -> str | None:
    """Map an InsightIDR API path to a fixture filename.

    Paths are full API paths, e.g. /idr/v2/investigations or /log_search/query/logs.
    """
    clean = path.split("?")[0].rstrip("/")
    parts = [p for p in clean.split("/") if p]

    if not parts:
        return None

    # /idr/v2/investigations[/{id}]
    if "investigations" in parts:
        idx = parts.index("investigations")
        return "investigations.json" if idx == len(parts) - 1 else "investigation.json"

    # /idr/v2/iocs
    if "iocs" in parts:
        return "indicators.json"

    # POST /log_search/query/logs
    if method == "POST" and "logs" in parts:
        return "log_search_results.json"

    return None


# ---------------------------------------------------------------------------
# Metasploit Pro fixture resolution
# ---------------------------------------------------------------------------


def _resolve_msp_fixture(method: str, path: str) -> str | None:
    """Map a Metasploit Pro API path to a fixture filename."""
    clean = path.split("?")[0].rstrip("/")
    parts = [p for p in clean.split("/") if p]

    if not parts:
        return None

    root = parts[0]

    if root == "workspaces":
        return "workspaces.json" if len(parts) == 1 else "workspace.json"

    if root == "sessions":
        return "sessions.json"

    if root == "looted_credentials":
        return "loot.json"

    if root == "tasks":
        return "msp_tasks.json"

    return None


# ---------------------------------------------------------------------------
# InsightVM clients
# ---------------------------------------------------------------------------


class InsightVMClient:
    """Async HTTP wrapper for the InsightVM REST API (v3).

    Uses Basic Auth against an on-prem console.
    """

    def __init__(self, settings: Settings) -> None:
        self.base_url = f"{settings.console_url}/api/3"
        self._auth = (settings.username, settings.password)
        self._verify = settings.verify_ssl

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            r = await client.get(f"{self.base_url}{path}", auth=self._auth, params=params)
            r.raise_for_status()
            return r.json()

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            r = await client.post(f"{self.base_url}{path}", auth=self._auth, json=body or {})
            r.raise_for_status()
            return r.json()

    async def put(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            r = await client.put(f"{self.base_url}{path}", auth=self._auth, json=body or {})
            r.raise_for_status()
            return r.json()


class DemoInsightVMClient(InsightVMClient):
    """Returns fixture data — no live console required (``DEMO_MODE=true``)."""

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_vm_fixture("GET", path)
        return _load_fixture(fixture) if fixture else _EMPTY_PAGE.copy()

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_vm_fixture("POST", path)
        return _load_fixture(fixture) if fixture else _EMPTY_PAGE.copy()


def get_client(settings: Settings = Depends(get_settings)) -> InsightVMClient:
    """FastAPI dependency — InsightVM client, real or demo."""
    if settings.demo_mode:
        return DemoInsightVMClient(settings)
    return InsightVMClient(settings)


# ---------------------------------------------------------------------------
# InsightIDR clients
# ---------------------------------------------------------------------------


class InsightIDRClient:
    """Async HTTP wrapper for the Insight Platform API (InsightIDR v2).

    Uses ``X-Api-Key`` header auth against the Rapid7 cloud API.
    Region must be one of: us, us2, us3, eu, ca, au, ap.
    """

    def __init__(self, settings: Settings) -> None:
        self.base_url = f"https://{settings.idr_region}.api.insight.rapid7.com"
        self._headers = {
            "X-Api-Key": settings.idr_api_key,
            "Content-Type": "application/json",
        }

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}{path}", headers=self._headers, params=params)
            r.raise_for_status()
            return r.json()

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.base_url}{path}", headers=self._headers, json=body or {})
            r.raise_for_status()
            return r.json()


class DemoInsightIDRClient(InsightIDRClient):
    """Returns fixture data for InsightIDR (``DEMO_MODE=true``)."""

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_idr_fixture("GET", path)
        return _load_fixture(fixture) if fixture else {"data": [], "metadata": {"total_data": 0}}

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_idr_fixture("POST", path)
        return _load_fixture(fixture) if fixture else {"data": [], "metadata": {"total_data": 0}}


def get_idr_client(settings: Settings = Depends(get_settings)) -> InsightIDRClient:
    """FastAPI dependency — InsightIDR client, real or demo."""
    if settings.demo_mode:
        return DemoInsightIDRClient(settings)
    return InsightIDRClient(settings)


# ---------------------------------------------------------------------------
# Metasploit Pro clients
# ---------------------------------------------------------------------------


class MetasploitClient:
    """Async HTTP wrapper for the Metasploit Pro REST API (v1).

    Uses ``X-Metasploit-Token`` header auth. All operations are read-only —
    this client intentionally exposes no exploit execution or mutation methods.
    """

    def __init__(self, settings: Settings) -> None:
        self.base_url = f"{settings.msp_url}/api/v1"
        self._headers = {
            "X-Metasploit-Token": settings.msp_token,
            "Content-Type": "application/json",
        }
        self._verify = settings.msp_verify_ssl

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            r = await client.get(f"{self.base_url}{path}", headers=self._headers, params=params)
            r.raise_for_status()
            return r.json()


class DemoMetasploitClient(MetasploitClient):
    """Returns fixture data for Metasploit Pro (``DEMO_MODE=true``)."""

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_msp_fixture("GET", path)
        return _load_fixture(fixture) if fixture else {"data": []}


def get_msp_client(settings: Settings = Depends(get_settings)) -> MetasploitClient:
    """FastAPI dependency — Metasploit Pro client, real or demo."""
    if settings.demo_mode:
        return DemoMetasploitClient(settings)
    return MetasploitClient(settings)
