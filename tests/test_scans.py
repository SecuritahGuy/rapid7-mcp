"""Tests for the scans router using demo mode fixtures."""

from fastapi.testclient import TestClient


def test_list_scans(client: TestClient) -> None:
    response = client.get("/scans")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 2
    scan = data["resources"][0]
    assert scan["siteName"] == "Production Network"
    assert scan["status"] == "finished"


def test_list_scans_active_filter(client: TestClient) -> None:
    response = client.get("/scans?active=true")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data


def test_get_scan(client: TestClient) -> None:
    response = client.get("/scans/101")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
