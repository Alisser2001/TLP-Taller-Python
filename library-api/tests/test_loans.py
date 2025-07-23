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
def sample_author_and_book(client):
    # Crear autor
    author_data = {
        "name": "Gabriel García Márquez",
        "nationality": "Colombian",
        "birth_year": 1927
    }
    author_response = client.post("/authors/", json=author_data)
    author = author_response.json()
    book_data = {
        "title": "Cien años de soledad",
        "isbn": "978-0307474728",
        "pages": 417,
        "price": 25.99,
        "author_id": author["id"]
    }
    book_response = client.post("/books/", json=book_data)
    book = book_response.json()
    return {"author": author, "book": book}


class TestLoans:
    def test_create_loan(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Juan Pérez",
            "user_email": "juan.perez@email.com",
            "book_id": book["id"]
        }
        response = client.post("/loans/", json=loan_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_name"] == loan_data["user_name"]
        assert data["user_email"] == loan_data["user_email"]
        assert data["book_id"] == loan_data["book_id"]
        assert data["returned"] == False
        assert "id" in data
        assert "loan_date" in data

    def test_create_loan_unavailable_book(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "María García",
            "user_email": "maria.garcia@email.com",
            "book_id": book["id"]
        }
        client.post("/loans/", json=loan_data)
        loan_data2 = {
            "user_name": "Carlos López",
            "user_email": "carlos.lopez@email.com",
            "book_id": book["id"]
        }
        response = client.post("/loans/", json=loan_data2)
        assert response.status_code == 400

    def test_get_loans(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Ana Rodríguez",
            "user_email": "ana.rodriguez@email.com",
            "book_id": book["id"]
        }
        client.post("/loans/", json=loan_data)
        response = client.get("/loans/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_get_loan_by_id(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Pedro Martínez",
            "user_email": "pedro.martinez@email.com",
            "book_id": book["id"]
        }
        create_response = client.post("/loans/", json=loan_data)
        loan_id = create_response.json()["id"]
        response = client.get(f"/loans/{loan_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["user_name"] == loan_data["user_name"]

    def test_return_book(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Laura Fernández",
            "user_email": "laura.fernandez@email.com",
            "book_id": book["id"]
        }
        create_response = client.post("/loans/", json=loan_data)
        loan_id = create_response.json()["id"]
        response = client.patch(f"/loans/{loan_id}/return")
        assert response.status_code == 200
        data = response.json()
        assert data["returned"] == True
        assert data["return_date"] is not None
        book_response = client.get(f"/books/{book['id']}")
        book_data = book_response.json()
        assert book_data["available"] == True

    def test_get_active_loans(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Roberto Silva",
            "user_email": "roberto.silva@email.com",
            "book_id": book["id"]
        }
        client.post("/loans/", json=loan_data)
        response = client.get("/loans/active")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["returned"] == False

    def test_get_loans_by_user(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        user_email = "sofia.morales@email.com"
        loan_data = {
            "user_name": "Sofía Morales",
            "user_email": user_email,
            "book_id": book["id"]
        }
        client.post("/loans/", json=loan_data)
        response = client.get(f"/loans/user/{user_email}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_email"] == user_email

    def test_delete_loan(self, client, sample_author_and_book):
        book = sample_author_and_book["book"]
        loan_data = {
            "user_name": "Diego Herrera",
            "user_email": "diego.herrera@email.com",
            "book_id": book["id"]
        }
        create_response = client.post("/loans/", json=loan_data)
        loan_id = create_response.json()["id"]
        response = client.delete(f"/loans/{loan_id}")
        assert response.status_code == 200
        get_response = client.get(f"/loans/{loan_id}")
        assert get_response.status_code == 404
        book_response = client.get(f"/books/{book['id']}")
        book_data = book_response.json()
        assert book_data["available"] == True