
def test_create_and_read_book(client):
    client.post(
        "/users/register", json={"email": "b@example.com", "password": "secret"}
    )
    login_resp = client.post(
        "/users/login", json={"email": "b@example.com", "password": "secret"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/books/", json={"title": "Book"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book"
    assert data["owner_id"] == 1
    book_id = data["id"]

    get_resp = client.get(f"/books/{book_id}", headers=headers)
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["title"] == "Book"
    assert fetched["owner_id"] == 1

    list_resp = client.get("/books/", headers=headers)
    assert list_resp.status_code == 200
    books = list_resp.json()
    assert any(b["id"] == book_id for b in books)
