
def test_create_and_read_book(client):
    user_resp = client.post("/users/", json={"email": "b@example.com", "password": "secret"})
    user_id = user_resp.json()["id"]

    response = client.post("/books/", json={"title": "Book", "owner_id": user_id})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book"
    assert data["owner_id"] == user_id
    book_id = data["id"]

    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["title"] == "Book"
    assert fetched["owner_id"] == user_id

    list_resp = client.get("/books/")
    assert list_resp.status_code == 200
    books = list_resp.json()
    assert any(b["id"] == book_id for b in books)
