"""Tests for asset groups and asset tags routers."""

from fastapi.testclient import TestClient


def test_list_asset_groups(client: TestClient) -> None:
    response = client.get("/asset_groups")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 4
    group = data["resources"][0]
    assert group["name"] == "PCI Scope"
    assert group["type"] == "static"


def test_list_asset_groups_type_filter(client: TestClient) -> None:
    response = client.get("/asset_groups?type=dynamic")
    assert response.status_code == 200


def test_get_asset_group(client: TestClient) -> None:
    response = client.get("/asset_groups/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PCI Scope"
    assert data["assets"] == 23


def test_get_asset_tags(client: TestClient) -> None:
    response = client.get("/assets/1/tags")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 3
    tag = data["resources"][0]
    assert "name" in tag
