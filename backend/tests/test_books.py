import zipfile


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


def _create_sample_epub(tmp_path):
    epub_path = tmp_path / "sample.epub"
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        container_xml = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>"
            "<rootfiles><rootfile full-path='OEBPS/content.opf' media-type='application/oebps-package+xml'/></rootfiles></container>"
        )
        zf.writestr("META-INF/container.xml", container_xml)
        content_opf = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<package xmlns='http://www.idpf.org/2007/opf' version='3.0'>"
            "<metadata xmlns:dc='http://purl.org/dc/elements/1.1/'><dc:title>Sample Book</dc:title></metadata>"
            "<manifest><item id='ch1' href='ch1.xhtml' media-type='application/xhtml+xml'/></manifest>"
            "<spine><itemref idref='ch1'/></spine></package>"
        )
        zf.writestr("OEBPS/content.opf", content_opf)
        chapter_html = (
            "<html xmlns='http://www.w3.org/1999/xhtml'><head><title>Chapter 1</title></head>"
            "<body><h1>Chapter 1</h1><p>Hello world.</p><p>Second paragraph.</p></body></html>"
        )
        zf.writestr("OEBPS/ch1.xhtml", chapter_html)
    return epub_path


def test_upload_book_success(client, tmp_path):
    client.post("/users/register", json={"email": "c@example.com", "password": "secret"})
    login_resp = client.post(
        "/users/login", json={"email": "c@example.com", "password": "secret"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    epub_path = _create_sample_epub(tmp_path)
    with open(epub_path, "rb") as f:
        resp = client.post(
            "/books/upload",
            files={"file": ("sample.epub", f, "application/epub+zip")},
            headers=headers,
        )
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]

    status_resp = client.get(f"/books/jobs/{job_id}/status", headers=headers)
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "completed"

    result_resp = client.get(f"/books/jobs/{job_id}/result", headers=headers)
    assert result_resp.status_code == 200
    markup = result_resp.json()
    assert markup["bookTitle"] == "Sample Book"

    list_resp = client.get("/books/", headers=headers)
    assert list_resp.status_code == 200
    books = list_resp.json()
    assert books[0]["id"] == job_id
    assert books[0]["markup"]["bookTitle"] == "Sample Book"


def test_job_status_and_result(client, tmp_path):
    client.post("/users/register", json={"email": "e@example.com", "password": "secret"})
    login_resp = client.post(
        "/users/login", json={"email": "e@example.com", "password": "secret"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    epub_path = _create_sample_epub(tmp_path)
    with open(epub_path, "rb") as f:
        upload_resp = client.post(
            "/books/upload",
            files={"file": ("sample.epub", f, "application/epub+zip")},
            headers=headers,
        )

    job_id = upload_resp.json()["job_id"]

    status_resp = client.get(f"/books/jobs/{job_id}/status", headers=headers)
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "completed"

    result_resp = client.get(f"/books/jobs/{job_id}/result", headers=headers)
    assert result_resp.status_code == 200
    data = result_resp.json()
    assert data["bookTitle"] == "Sample Book"


def test_upload_book_invalid_file(client, tmp_path):
    client.post("/users/register", json={"email": "d@example.com", "password": "secret"})
    login_resp = client.post(
        "/users/login", json={"email": "d@example.com", "password": "secret"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    bad_path = tmp_path / "bad.epub"
    bad_path.write_bytes(b"not an epub")
    with open(bad_path, "rb") as f:
        resp = client.post(
            "/books/upload",
            files={"file": ("bad.epub", f, "application/epub+zip")},
            headers=headers,
        )
    assert resp.status_code == 400
