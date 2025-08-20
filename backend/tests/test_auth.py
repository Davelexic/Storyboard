from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from backend.app.main import app
from backend.app.db import get_session
from sqlalchemy.pool import StaticPool

# Setup in-memory test database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(test_engine)


def get_session_override():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override
client = TestClient(app)


def test_registration_login_and_protected_routes():
    # Register user
    resp = client.post("/users/register", json={"email": "user@example.com", "password": "secret"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Login user
    login_resp = client.post("/users/login", json={"email": "user@example.com", "password": "secret"})
    assert login_resp.status_code == 200
    login_token = login_resp.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {login_token}"}

    # Unauthorized access
    assert client.get("/books").status_code == 401

    # Create book with auth
    book_resp = client.post("/books", json={"title": "Test Book"}, headers=auth_headers)
    assert book_resp.status_code == 200
    book = book_resp.json()
    assert book["owner_id"] == 1

    # Retrieve books with auth
    books_resp = client.get("/books", headers=auth_headers)
    assert books_resp.status_code == 200
    books = books_resp.json()
    assert len(books) == 1
    assert books[0]["title"] == "Test Book"

    # Unauthorized book creation
    assert client.post("/books", json={"title": "Bad"}).status_code == 401
