"""Tests for the Metasploit Pro (read-only) router."""

from fastapi.testclient import TestClient


def test_list_workspaces(client: TestClient) -> None:
    response = client.get("/metasploit/workspaces")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2
    ws = data["data"][0]
    assert ws["name"] == "default"


def test_get_workspace(client: TestClient) -> None:
    response = client.get("/metasploit/workspaces/2")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "prod-external-pentest-2024"
    assert data["sessions_count"] == 1


def test_list_sessions(client: TestClient) -> None:
    response = client.get("/metasploit/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2
    session = data["data"][0]
    assert session["session_type"] == "meterpreter"
    assert session["platform"] == "windows"


def test_list_sessions_workspace_filter(client: TestClient) -> None:
    response = client.get("/metasploit/sessions?workspace=default")
    assert response.status_code == 200


def test_get_loot(client: TestClient) -> None:
    response = client.get("/metasploit/loot")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2
    entry = data["data"][0]
    assert entry["loot_type"] == "hash"
    assert entry["service_name"] == "smb"


def test_list_msp_tasks(client: TestClient) -> None:
    response = client.get("/metasploit/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2
    task = data["data"][0]
    assert task["task_type"] == "nexpose_import"
    assert task["status"] == "completed"
