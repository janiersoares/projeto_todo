import uuid


def test_list_requires_token(client):
    response = client.get("/tasks")
    assert response.status_code == 401


def test_create_then_list_with_token(client, auth_headers):
    created = client.post(
        "/tasks",
        json={"title": "Minha tarefa"},
        headers=auth_headers,
    )
    assert created.status_code == 201

    listed = client.get("/tasks", headers=auth_headers)
    assert listed.status_code == 200
    titles = [task["title"] for task in listed.json()]
    assert "Minha tarefa" in titles


def test_user_cannot_read_another_users_task(client, auth_headers):
    created = client.post(
        "/tasks",
        json={"title": "Privada"},
        headers=auth_headers,
    )
    task_id = created.json()["id"]

    email = f"other-{uuid.uuid4().hex[:8]}@example.com"
    client.post(
        "/auth/register",
        json={"email": email, "password": "12345678"},
    )
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "12345678"},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.get(f"/tasks/{task_id}", headers=other_headers)
    assert response.status_code == 404


def test_user_cannot_delete_another_users_task(client, auth_headers):
    created = client.post(
        "/tasks",
        json={"title": "Não apagar"},
        headers=auth_headers,
    )
    task_id = created.json()["id"]

    email = f"intruder-{uuid.uuid4().hex[:8]}@example.com"
    client.post(
        "/auth/register",
        json={"email": email, "password": "12345678"},
    )
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "12345678"},
    )
    intruder_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.delete(f"/tasks/{task_id}", headers=intruder_headers)
    assert response.status_code == 404

    still_there = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert still_there.status_code == 200