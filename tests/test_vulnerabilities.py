"""Tests for the vulnerabilities router using demo mode fixtures."""

from fastapi.testclient import TestClient


def test_list_vulnerabilities(client: TestClient) -> None:
    response = client.get("/vulnerabilities")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 3
    vuln = data["resources"][0]
    assert vuln["id"] == "openssl-cve-2022-0778"
    assert vuln["severity"] == "Critical"


def test_list_vulnerabilities_with_severity_filter(client: TestClient) -> None:
    response = client.get("/vulnerabilities?severity=Critical")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data


def test_get_vulnerability(client: TestClient) -> None:
    response = client.get("/vulnerabilities/openssl-cve-2022-0778")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "openssl-cve-2022-0778"
    assert data["cvssV3Score"] == 7.5
    assert "CVE-2022-0778" in data["cves"]
    assert data["exploits"] == 1


def test_get_vulnerability_has_description(client: TestClient) -> None:
    response = client.get("/vulnerabilities/openssl-cve-2022-0778")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] is not None
    assert len(data["description"]) > 0
