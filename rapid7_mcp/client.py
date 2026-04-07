"""Async HTTP client for the Rapid7 InsightVM v3 REST API."""

import json
from pathlib import Path
from typing import Any

import httpx
from fastapi import Depends

from rapid7_mcp.config import Settings, get_settings

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures"


def _load_fixture(name: str) -> dict[str, Any]:
    path = FIXTURES_DIR / name
    with open(path) as f:
        return json.load(f)


def _resolve_fixture(method: str, path: str) -> str | None:
    """Return the fixture filename for a given API method + path, or None.

    Handles both collection endpoints (/sites) and item endpoints (/sites/1)
    by counting path segments after stripping query strings.
    """
    clean = path.split("?")[0].rstrip("/")
    parts = [p for p in clean.split("/") if p]

    # POST /assets/search
    if method == "POST" and clean == "/assets/search":
        return "assets.json"

    if not parts:
        return None

    root = parts[0]

    # /sites → list, /sites/{id} → single
    if root == "sites":
        return "sites.json" if len(parts) == 1 else "site.json"

    # /assets/{id}/vulnerabilities → asset vulns list
    if root == "assets" and len(parts) == 3 and parts[2] == "vulnerabilities":
        return "asset_vulnerabilities.json"

    # /assets/{id} → single asset
    if root == "assets" and len(parts) == 2:
        return "asset.json"

    # /vulnerabilities → list, /vulnerabilities/{id} → single
    if root == "vulnerabilities":
        return "vulnerabilities.json" if len(parts) == 1 else "vulnerability.json"

    # /scans → list, /scans/{id} → single
    if root == "scans":
        return "scans.json" if len(parts) == 1 else "scan.json"

    return None


class InsightVMClient:
    """Thin async wrapper around the InsightVM REST API (v3)."""

    def __init__(self, settings: Settings) -> None:
        self.base_url = f"{settings.console_url}/api/3"
        self._auth = (settings.username, settings.password)
        self._verify = settings.verify_ssl

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            response = await client.get(
                f"{self.base_url}{path}",
                auth=self._auth,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            response = await client.post(
                f"{self.base_url}{path}",
                auth=self._auth,
                json=body or {},
            )
            response.raise_for_status()
            return response.json()

    async def put(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(verify=self._verify) as client:
            response = await client.put(
                f"{self.base_url}{path}",
                auth=self._auth,
                json=body or {},
            )
            response.raise_for_status()
            return response.json()


class DemoInsightVMClient(InsightVMClient):
    """Returns fixture data instead of hitting a live console.

    Activated via ``DEMO_MODE=true`` — lets anyone explore the MCP tools
    in Claude without Rapid7 credentials.
    """

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_fixture("GET", path)
        if fixture:
            return _load_fixture(fixture)
        return {"resources": [], "page": {"number": 0, "size": 0, "totalPages": 0, "totalResources": 0}}

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        fixture = _resolve_fixture("POST", path)
        if fixture:
            return _load_fixture(fixture)
        return {"resources": [], "page": {"number": 0, "size": 0, "totalPages": 0, "totalResources": 0}}


def get_client(settings: Settings = Depends(get_settings)) -> InsightVMClient:
    """FastAPI dependency — returns a real or demo client based on config."""
    if settings.demo_mode:
        return DemoInsightVMClient(settings)
    return InsightVMClient(settings)
