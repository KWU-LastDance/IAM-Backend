import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.models.products import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./products_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db():
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


def test_create_product(client, db):
    response = client.post(
        "/products",
        json={"name": "test", "description": "test", "category": "test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert data["description"] == "test"
    assert data["category"] == "test"
    assert "id" in data


def test_get_product(client, db):
    response = client.get(
        "/products/"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test"
    assert data[0]["description"] == "test"
    assert data[0]["category"] == "test"
    assert "id" in data[0]

def test_get_product_by_id(client, db):
    response = client.get(
        "/products/1"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert data["description"] == "test"
    assert data["category"] == "test"
    assert "id" in data

def test_update_product(client, db):
    response = client.patch(
        "/products/1",
        json={"name": "test1", "description": "test1", "category": "test1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test1"
    assert data["description"] == "test1"
    assert data["category"] == "test1"
    assert "id" in data

def test_delete_product(client, db):
    response = client.delete(
        "/products/1"
    )
    assert response.status_code == 200
    response = client.get(
        "/products/"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
