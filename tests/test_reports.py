"""Tests for the reports router."""

from fastapi.testclient import TestClient


def test_list_reports(client: TestClient) -> None:
    response = client.get("/reports")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 3
    report = data["resources"][0]
    assert report["name"] == "Executive Vulnerability Summary"
    assert report["format"] == "pdf"


def test_get_report(client: TestClient) -> None:
    response = client.get("/reports/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Executive Vulnerability Summary"
    assert "uri" in data


def test_execute_report(client: TestClient) -> None:
    response = client.post("/reports/1/generate")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "started"
    assert "uri" in data
