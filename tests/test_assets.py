"""Tests for the assets router using demo mode fixtures."""

from fastapi.testclient import TestClient


def test_get_asset(client: TestClient) -> None:
    response = client.get("/assets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["ip"] == "192.168.1.100"
    assert data["hostName"] == "prod-web-01.example.com"
    assert data["vulnerabilities"]["critical"] == 3
    assert data["vulnerabilities"]["total"] == 83


def test_get_asset_os(client: TestClient) -> None:
    response = client.get("/assets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["os"]["family"] == "Linux"
    assert data["os"]["version"] == "22.04"


def test_search_assets(client: TestClient) -> None:
    payload = {
        "filters": [{"field": "ip-address", "operator": "starts-with", "value": "192.168"}],
        "match": "all",
    }
    response = client.post("/assets/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 2


def test_search_assets_empty_filters(client: TestClient) -> None:
    response = client.post("/assets/search", json={"filters": [], "match": "all"})
    assert response.status_code == 200


def test_get_asset_vulnerabilities(client: TestClient) -> None:
    response = client.get("/assets/1/vulnerabilities")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert "page" in data
