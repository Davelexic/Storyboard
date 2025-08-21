def test_user_preferences_roundtrip(client):
    register_resp = client.post(
        "/users/register", json={"email": "pref@example.com", "password": "secret"}
    )
    assert register_resp.status_code == 200

    login_resp = client.post(
        "/users/login", json={"email": "pref@example.com", "password": "secret"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # default preferences
    get_resp = client.get("/users/me/preferences", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json() == {
        "effectsEnabled": True,
        "fontSize": 16,
        "brightness": 1.0,
        "adaptiveBrightness": False,
        "effects": {
            "motion": {"enabled": True, "intensity": 1.0},
            "color": {"enabled": True, "intensity": 1.0},
        },
    }

    prefs = {
        "effectsEnabled": False,
        "fontSize": 20,
        "brightness": 0.8,
        "adaptiveBrightness": True,
        "effects": {
            "motion": {"enabled": False, "intensity": 0.4},
            "color": {"enabled": True, "intensity": 0.9},
        },
    }
    put_resp = client.put("/users/me/preferences", headers=headers, json=prefs)
    assert put_resp.status_code == 200
    assert put_resp.json() == prefs

    get_resp = client.get("/users/me/preferences", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json() == prefs


def test_partial_preference_update(client):
    register_resp = client.post(
        "/users/register", json={"email": "partial@example.com", "password": "secret"}
    )
    assert register_resp.status_code == 200

    login_resp = client.post(
        "/users/login", json={"email": "partial@example.com", "password": "secret"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update = {"fontSize": 24}
    put_resp = client.put("/users/me/preferences", headers=headers, json=update)
    assert put_resp.status_code == 200
    assert put_resp.json()["fontSize"] == 24

    get_resp = client.get("/users/me/preferences", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["fontSize"] == 24
