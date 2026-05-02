from fastapi.testclient import TestClient
from main import app
from models import db

client = TestClient(app)

def setup_function():
    db.clear()

def test_add_book():
    response = client.post("/books", json={
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "description": "Збірка поезій",
        "status": "available",
        "year": 1840
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Кобзар"

def test_get_books():
    client.post("/books", json={"title": "1984", "author": "Орвелл", "status": "available", "year": 1949})
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_book_not_found():
    response = client.get("/books/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404

def test_delete_book_idempotent():
    post_resp = client.post("/books", json={"title": "Тест", "author": "Автор", "status": "available", "year": 2020})
    book_id = post_resp.json()["id"]

    del_resp1 = client.delete(f"/books/{book_id}")
    assert del_resp1.status_code == 204

    del_resp2 = client.delete(f"/books/{book_id}")
    assert del_resp2.status_code == 204