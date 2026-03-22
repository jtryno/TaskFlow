import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db

# --- Create the test database engine and session ---
# only uses sqlite:/// instead of sqlite:///... to create an in-memory db so it disappears
# after testing is complete
engine = create_engine("sqlite:///", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Make the db fixture to give each test a fresh db session
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# Make the client fixture to give each test a TestClient that uses the test db
@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Test 1: Creating a test  |  POST /tasks w/ title and descciption
# Expected Result: 201 Status Code & a Response containing the title
# and description you sent, plus id, completed (defaulting to False), 
# and created_at.
def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task", "description": "A test"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
