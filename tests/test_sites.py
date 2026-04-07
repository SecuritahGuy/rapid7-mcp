"""Tests for the sites router using demo mode fixtures."""

from fastapi.testclient import TestClient


def test_list_sites(client: TestClient) -> None:
    response = client.get("/sites")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 3
    site = data["resources"][0]
    assert site["name"] == "Production Network"
    assert site["assets"] == 152
    assert "riskScore" in site


def test_list_sites_pagination_params(client: TestClient) -> None:
    response = client.get("/sites?page=0&size=5")
    assert response.status_code == 200


def test_get_site_returns_fixture(client: TestClient) -> None:
    # Demo client returns the sites fixture for any /sites/{id} path
    response = client.get("/sites/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
