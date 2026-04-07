"""Tests for the remediation projects router."""

from fastapi.testclient import TestClient


def test_list_remediation_projects(client: TestClient) -> None:
    response = client.get("/remediation_projects")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 2
    project = data["resources"][0]
    assert "name" in project
    assert "owner" in project
    assert project["completed"] is False


def test_list_remediation_projects_status_filter(client: TestClient) -> None:
    response = client.get("/remediation_projects?status=active")
    assert response.status_code == 200


def test_get_remediation_project(client: TestClient) -> None:
    response = client.get("/remediation_projects/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Q1 2024 — Critical Patching Sprint"
    assert data["owner"] == "alice@example.com"
