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

class TestAuthors:
    def test_create_author(self, client):
        author_data = {
            "name": "Gabriel García Márquez",
            "nationality": "Colombian",
            "birth_year": 1927
        }
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == author_data["name"]
        assert data["nationality"] == author_data["nationality"]
        assert data["birth_year"] == author_data["birth_year"]
        assert "id" in data

    def test_get_authors(self, client):
        authors_data = [
            {"name": "Jorge Luis Borges", "nationality": "Argentine", "birth_year": 1899},
            {"name": "Mario Vargas Llosa", "nationality": "Peruvian", "birth_year": 1936}
        ]
        for author_data in authors_data:
            client.post("/authors/", json=author_data)
        response = client.get("/authors/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_author_by_id(self, client):
        author_data = {
            "name": "Octavio Paz",
            "nationality": "Mexican",
            "birth_year": 1914
        }
        create_response = client.post("/authors/", json=author_data)
        author_id = create_response.json()["id"]
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == author_data["name"]

    def test_update_author(self, client):
        author_data = {
            "name": "Isabel Allende",
            "nationality": "Chilean",
            "birth_year": 1942
        }
        create_response = client.post("/authors/", json=author_data)
        author_id = create_response.json()["id"]
        update_data = {"nationality": "Chilean-American"}
        response = client.put(f"/authors/{author_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nationality"] == update_data["nationality"]
        assert data["name"] == author_data["name"]  # No cambió

    def test_delete_author(self, client):
        author_data = {
            "name": "Julio Cortázar",
            "nationality": "Argentine",
            "birth_year": 1914
        }
        create_response = client.post("/authors/", json=author_data)
        author_id = create_response.json()["id"]
        response = client.delete(f"/authors/{author_id}")
        assert response.status_code == 200
        get_response = client.get(f"/authors/{author_id}")
        assert get_response.status_code == 404

    def test_get_nonexistent_author(self, client):
        response = client.get("/authors/999")
        assert response.status_code == 404