"""Shared test fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient

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
    app.dependency_overrides[get_settings] = demo_settings
    yield TestClient(app)
    app.dependency_overrides.clear()
