def test_create_and_read_user(client):
    register_resp = client.post(
        "/users/register", json={"email": "a@example.com", "password": "secret"}
    )
    assert register_resp.status_code == 200
    token_data = register_resp.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    login_resp = client.post(
        "/users/login", json={"email": "a@example.com", "password": "secret"}
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
    headers = {"Authorization": f"Bearer {login_data['access_token']}"}

    user_id = 1
    get_resp = client.get(f"/users/{user_id}", headers=headers)
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == user_id
    assert fetched["email"] == "a@example.com"

    list_resp = client.get("/users/", headers=headers)
    assert list_resp.status_code == 200
    users = list_resp.json()
    assert any(u["id"] == user_id for u in users)
