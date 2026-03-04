from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def owner_id(client: TestClient) -> str:
    """Create a user and return their id for use as project owner."""
    resp = client.post(
        "/users/",
        json={
            "email": f"owner@test.com",
            "full_name": "Project Owner",
            "is_active": True,
            "password": "secret",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_create_and_get_project(client: TestClient, owner_id: str) -> None:
    payload = {
        "name": "My Project",
        "description": "A test project",
        "owner_id": owner_id,
    }
    resp = client.post("/projects/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["owner_id"] == owner_id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    project_id = data["id"]

    resp_get = client.get(f"/projects/{project_id}")
    assert resp_get.status_code == 200
    data_get = resp_get.json()
    assert data_get["name"] == payload["name"]
    assert data_get["id"] == project_id


def test_create_project_minimal(client: TestClient, owner_id: str) -> None:
    payload = {"name": "Minimal Project", "owner_id": owner_id}
    resp = client.post("/projects/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["name"] == payload["name"]
    assert data["description"] is None


def test_list_projects(client: TestClient, owner_id: str) -> None:
    resp = client.get("/projects/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

    # Create two projects
    client.post("/projects/", json={"name": "First", "owner_id": owner_id})
    client.post("/projects/", json={"name": "Second", "owner_id": owner_id})

    resp_list = client.get("/projects/")
    assert resp_list.status_code == 200
    projects = resp_list.json()
    assert len(projects) >= 2
    names = [p["name"] for p in projects]
    assert "First" in names
    assert "Second" in names


def test_list_projects_filter_by_owner(client: TestClient, owner_id: str) -> None:
    # Create another user and project
    user_resp = client.post(
        "/users/",
        json={
            "email": "other@test.com",
            "full_name": "Other",
            "is_active": True,
            "password": "secret",
        },
    )
    assert user_resp.status_code == 201
    other_owner_id = user_resp.json()["id"]

    client.post("/projects/", json={"name": "Owned by first", "owner_id": owner_id})
    client.post("/projects/", json={"name": "Owned by other", "owner_id": other_owner_id})

    resp = client.get(f"/projects/?owner_id={owner_id}")
    assert resp.status_code == 200
    projects = resp.json()
    assert all(p["owner_id"] == owner_id for p in projects)
    names = [p["name"] for p in projects]
    assert "Owned by first" in names
    assert "Owned by other" not in names


def test_update_project(client: TestClient, owner_id: str) -> None:
    create_resp = client.post(
        "/projects/",
        json={"name": "Original", "description": "Old", "owner_id": owner_id},
    )
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    resp = client.patch(
        f"/projects/{project_id}",
        json={"name": "Updated", "description": "New description"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated"
    assert data["description"] == "New description"

    resp_get = client.get(f"/projects/{project_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["name"] == "Updated"


def test_update_project_partial(client: TestClient, owner_id: str) -> None:
    create_resp = client.post(
        "/projects/",
        json={"name": "Original", "description": "Keep me", "owner_id": owner_id},
    )
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    resp = client.patch(f"/projects/{project_id}", json={"name": "Only name changed"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Only name changed"
    assert data["description"] == "Keep me"


def test_delete_project(client: TestClient, owner_id: str) -> None:
    create_resp = client.post(
        "/projects/",
        json={"name": "To Delete", "owner_id": owner_id},
    )
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    resp_del = client.delete(f"/projects/{project_id}")
    assert resp_del.status_code == 204

    resp_get = client.get(f"/projects/{project_id}")
    assert resp_get.status_code == 404
    assert resp_get.json()["detail"] == "Project not found"


def test_get_project_not_found(client: TestClient) -> None:
    project_id = uuid4()
    resp = client.get(f"/projects/{project_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Project not found"


def test_update_project_not_found(client: TestClient) -> None:
    project_id = uuid4()
    resp = client.patch(
        f"/projects/{project_id}",
        json={"name": "Updated"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Project not found"


def test_delete_project_not_found(client: TestClient) -> None:
    project_id = uuid4()
    resp = client.delete(f"/projects/{project_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Project not found"
