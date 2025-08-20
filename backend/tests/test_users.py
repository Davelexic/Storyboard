from backend.app.models import User


def test_create_and_read_user(client):
    response = client.post("/users/", json={"email": "a@example.com", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "a@example.com"
    assert "id" in data

    user_id = data["id"]
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == user_id
    assert fetched["email"] == "a@example.com"

    list_resp = client.get("/users/")
    assert list_resp.status_code == 200
    users = list_resp.json()
    assert any(u["id"] == user_id for u in users)
