from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def owner_id(client: TestClient) -> str:
    """Create a user and return their id for use as project owner."""
    resp = client.post(
        "/users/",
        json={
            "email": "owner@test.com",
            "full_name": "Project Owner",
            "is_active": True,
            "password": "secret",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


@pytest.fixture()
def project_id(client: TestClient, owner_id: str) -> str:
    """Create a project and return its id for use in todo endpoints."""
    resp = client.post(
        "/projects/",
        json={"name": "Todo Project", "owner_id": owner_id},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_create_and_get_todo(client: TestClient, project_id: str) -> None:
    payload = {
        "title": "My first todo",
        "description": "Get it done",
        "status": "todo",
        "priority": 2,
        "position": 0,
    }
    resp = client.post(f"/projects/{project_id}/todos/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]
    assert data["priority"] == payload["priority"]
    assert data["project_id"] == project_id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    todo_id = data["id"]

    resp_get = client.get(f"/projects/{project_id}/todos/{todo_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["title"] == payload["title"]


def test_create_todo_minimal(client: TestClient, project_id: str) -> None:
    payload = {"title": "Minimal todo"}
    resp = client.post(f"/projects/{project_id}/todos/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "todo"
    assert data["priority"] == 2  # MEDIUM
    assert data["description"] is None


def test_list_todos(client: TestClient, project_id: str) -> None:
    resp = client.get(f"/projects/{project_id}/todos/")
    assert resp.status_code == 200
    assert resp.json() == []

    client.post(f"/projects/{project_id}/todos/", json={"title": "One"})
    client.post(f"/projects/{project_id}/todos/", json={"title": "Two"})

    resp_list = client.get(f"/projects/{project_id}/todos/")
    assert resp_list.status_code == 200
    todos = resp_list.json()
    assert len(todos) == 2
    titles = [t["title"] for t in todos]
    assert "One" in titles
    assert "Two" in titles


def test_update_todo(client: TestClient, project_id: str) -> None:
    create_resp = client.post(
        f"/projects/{project_id}/todos/",
        json={"title": "Original", "description": "Old", "status": "todo"},
    )
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]

    resp = client.patch(
        f"/projects/{project_id}/todos/{todo_id}",
        json={"title": "Updated", "status": "in_progress"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated"
    assert data["status"] == "in_progress"

    resp_get = client.get(f"/projects/{project_id}/todos/{todo_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["title"] == "Updated"


def test_update_todo_partial(client: TestClient, project_id: str) -> None:
    create_resp = client.post(
        f"/projects/{project_id}/todos/",
        json={"title": "Original", "priority": 1},
    )
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]

    resp = client.patch(
        f"/projects/{project_id}/todos/{todo_id}",
        json={"title": "Only title changed"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Only title changed"
    assert data["priority"] == 1


def test_delete_todo(client: TestClient, project_id: str) -> None:
    create_resp = client.post(
        f"/projects/{project_id}/todos/",
        json={"title": "To Delete"},
    )
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]

    resp_del = client.delete(f"/projects/{project_id}/todos/{todo_id}")
    assert resp_del.status_code == 204

    resp_get = client.get(f"/projects/{project_id}/todos/{todo_id}")
    assert resp_get.status_code == 404
    assert resp_get.json()["detail"] == "Todo not found"


def test_list_todos_project_not_found(client: TestClient) -> None:
    project_id = uuid4()
    resp = client.get(f"/projects/{project_id}/todos/")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Project not found"


def test_create_todo_project_not_found(client: TestClient) -> None:
    project_id = uuid4()
    resp = client.post(
        f"/projects/{project_id}/todos/",
        json={"title": "Orphan"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Project not found"


def test_get_todo_not_found(client: TestClient, project_id: str) -> None:
    todo_id = uuid4()
    resp = client.get(f"/projects/{project_id}/todos/{todo_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Todo not found"


def test_update_todo_not_found(client: TestClient, project_id: str) -> None:
    todo_id = uuid4()
    resp = client.patch(
        f"/projects/{project_id}/todos/{todo_id}",
        json={"title": "Updated"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Todo not found"


def test_delete_todo_not_found(client: TestClient, project_id: str) -> None:
    todo_id = uuid4()
    resp = client.delete(f"/projects/{project_id}/todos/{todo_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Todo not found"
