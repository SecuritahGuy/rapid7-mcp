"""Shared test fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient

from rapid7_mcp.client import get_client, get_idr_client, get_msp_client
from rapid7_mcp.config import Settings, get_settings
from rapid7_mcp.main import app


def demo_settings() -> Settings:
    return Settings(
        console_url="https://test-console:3780",
        username="testuser",
        password="testpass",
        verify_ssl=False,
        demo_mode=True,
    )


@pytest.fixture
def client() -> TestClient:
    """TestClient with all dependencies overridden to demo mode."""
    app.dependency_overrides[get_settings] = demo_settings
    # The client deps read settings via get_settings, which is already overridden.
    # Override the product clients directly too so demo mode is guaranteed.
    from rapid7_mcp.client import (
        DemoInsightIDRClient,
        DemoInsightVMClient,
        DemoMetasploitClient,
    )

    settings = demo_settings()
    app.dependency_overrides[get_client] = lambda: DemoInsightVMClient(settings)
    app.dependency_overrides[get_idr_client] = lambda: DemoInsightIDRClient(settings)
    app.dependency_overrides[get_msp_client] = lambda: DemoMetasploitClient(settings)

    yield TestClient(app)
    app.dependency_overrides.clear()
