"""Tests for the InsightIDR router."""

from fastapi.testclient import TestClient


def test_list_investigations(client: TestClient) -> None:
    response = client.get("/idr/investigations")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2
    inv = data["data"][0]
    assert inv["status"] == "OPEN"
    assert inv["priority"] == "HIGH"
    assert "title" in inv


def test_list_investigations_filters(client: TestClient) -> None:
    response = client.get("/idr/investigations?status=INVESTIGATING&priority=CRITICAL")
    assert response.status_code == 200


def test_get_investigation(client: TestClient) -> None:
    response = client.get("/idr/investigations/INV-002")
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "CRITICAL"
    assert len(data["alerts"]) == 2


def test_query_logs(client: TestClient) -> None:
    payload = {
        "query": 'where(destination_ip = "185.220.101.1")',
        "from_time": 1705276800000,
        "to_time": 1705363200000,
        "logs": ["firewall-logs"],
    }
    response = client.post("/idr/logs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert len(data["events"]) == 3


def test_list_indicators(client: TestClient) -> None:
    response = client.get("/idr/iocs")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 3
    ioc = data["data"][0]
    assert ioc["indicator_type"] == "IP_ADDRESS"
    assert ioc["active"] is True


def test_list_indicators_type_filter(client: TestClient) -> None:
    response = client.get("/idr/iocs?indicator_type=FILE_HASH")
    assert response.status_code == 200
