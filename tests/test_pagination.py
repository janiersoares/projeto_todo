def test_list_respects_limit_and_offset(client, auth_headers):
    for number in range(3):
        client.post("/tasks", json={"title": f"Task {number}"}, headers=auth_headers)

    first_page = client.get("/tasks?limit=2&offset=0", headers=auth_headers).json()
    second_page = client.get("/tasks?limit=2&offset=2", headers=auth_headers).json()

    assert [task["title"] for task in first_page] == ["Task 0", "Task 1"]
    assert [task["title"] for task in second_page] == ["Task 2"]


def test_invalid_limit_returns_422(client, auth_headers):
    response = client.get("/tasks?limit=0", headers=auth_headers)
    assert response.status_code == 422
