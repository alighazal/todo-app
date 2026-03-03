from fastapi.testclient import TestClient


def test_create_and_get_user(client: TestClient) -> None:
    payload = {
        "email": "alice@example.com",
        "full_name": "Alice",
        "is_active": True,
        "password": "secret",
    }
    resp = client.post("/users/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["email"] == payload["email"]
    user_id = data["id"]

    resp_get = client.get(f"/users/{user_id}")
    assert resp_get.status_code == 200
    data_get = resp_get.json()
    assert data_get["email"] == payload["email"]


def test_list_users(client: TestClient) -> None:
    resp = client.get("/users/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_soft_delete_user(client: TestClient) -> None:
    # Create a user
    payload = {
        "email": "bob@example.com",
        "full_name": "Bob",
        "is_active": True,
        "password": "secret",
    }
    resp = client.post("/users/", json=payload)
    assert resp.status_code == 201, resp.text
    user_id = resp.json()["id"]

    # Delete the user (soft delete)
    resp_del = client.delete(f"/users/{user_id}")
    assert resp_del.status_code == 204

    # Getting the user should now return 404
    resp_get = client.get(f"/users/{user_id}")
    assert resp_get.status_code == 404

    # List users should not include the deleted user
    resp_list = client.get("/users/")
    assert resp_list.status_code == 200
    emails = [u["email"] for u in resp_list.json()]
    assert payload["email"] not in emails

