import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_author(client):
    author_data = {
        "name": "Gabriel García Márquez",
        "nationality": "Colombian",
        "birth_year": 1927
    }
    response = client.post("/authors/", json=author_data)
    return response.json()

class TestBooks:
    def test_create_book(self, client, sample_author):
        book_data = {
            "title": "Cien años de soledad",
            "isbn": "978-0307474728",
            "pages": 417,
            "price": 25.99,
            "author_id": sample_author["id"]
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["isbn"] == book_data["isbn"]
        assert data["pages"] == book_data["pages"]
        assert data["price"] == book_data["price"]
        assert data["available"] == True
        assert "id" in data

    def test_create_book_duplicate_isbn(self, client, sample_author):
        book_data = {
            "title": "Libro 1",
            "isbn": "978-0307474728",
            "pages": 300,
            "price": 20.00,
            "author_id": sample_author["id"]
        }
        client.post("/books/", json=book_data)
        book_data["title"] = "Libro 2"
        response = client.post("/books/", json=book_data)
        assert response.status_code == 400

    def test_get_books(self, client, sample_author):
        books_data = [
            {
                "title": "El amor en los tiempos del cólera",
                "isbn": "978-0307389732",
                "pages": 348,
                "price": 24.99,
                "author_id": sample_author["id"]
            },
            {
                "title": "Crónica de una muerte anunciada",
                "isbn": "978-1400034713",
                "pages": 120,
                "price": 15.99,
                "author_id": sample_author["id"]
            }
        ]

        for book_data in books_data:
            client.post("/books/", json=book_data)
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_book_by_id(self, client, sample_author):
        book_data = {
            "title": "Del amor y otros demonios",
            "isbn": "978-1400034666",
            "pages": 147,
            "price": 18.99,
            "author_id": sample_author["id"]
        }
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == book_data["title"]

    def test_update_book(self, client, sample_author):
        book_data = {
            "title": "La hojarasca",
            "isbn": "978-0060531041",
            "pages": 112,
            "price": 16.99,
            "author_id": sample_author["id"]
        }
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]
        update_data = {"pages": 120, "price": 19.99}
        response = client.put(f"/books/{book_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["pages"] == update_data["pages"]
        assert data["price"] == update_data["price"]
        assert data["title"] == book_data["title"]  # No cambió

    def test_delete_book(self, client, sample_author):
        book_data = {
            "title": "Memoria de mis putas tristes",
            "isbn": "978-1400095803",
            "pages": 115,
            "price": 17.99,
            "author_id": sample_author["id"]
        }
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 200
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404

    def test_apply_discount(self, client, sample_author):
        book_data = {
            "title": "Vivir para contarla",
            "isbn": "978-1400095809",
            "pages": 565,
            "price": 30.00,
            "author_id": sample_author["id"]
        }
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["id"]
        discount_data = {"discount_percentage": 20.0}
        response = client.patch(f"/books/{book_id}/discount", json=discount_data)
        assert response.status_code == 200
        data = response.json()
        expected_price = 30.00 * 0.8  # 20% descuento
        assert data["price"] == expected_price

    def test_get_available_books(self, client, sample_author):
        book_data = {
            "title": "Noticia de un secuestro",
            "isbn": "978-1400034710",
            "pages": 292,
            "price": 22.99,
            "author_id": sample_author["id"]
        }
        client.post("/books/", json=book_data)
        response = client.get("/books/available")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["available"] == True