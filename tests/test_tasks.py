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
engine = create_engine(
    "sqlite:///", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
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
    response = client.post(
        "/tasks", json={"title": "Test Task", "description": "A test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


# Test 2: Listing all tasks  |  GET /tasks
# Expected Result: 200 Status Code, initially an empty list,
# then a list with one task after creating one.
def test_list_all_tasks(client):
    initial_response = client.get("/tasks")
    assert initial_response.status_code == 200
    assert initial_response.json() == []

    post_response = client.post(
        "/tasks", json={"title": "Test Task", "description": "A test"}
    )
    assert post_response.status_code == 201

    finial_response = client.get("/tasks")
    assert finial_response.status_code == 200
    data = finial_response.json()

    assert len(data) == 1

    assert data[0]["title"] == "Test Task"
    assert data[0]["description"] == "A test"
    assert data[0]["completed"] is False
    assert "id" in data[0]
    assert "created_at" in data[0]


# Test 3: Get a single task by task_id PASS  |  GET /tasks/{task_id}
# Expected result: 200 Status Code, initially an empty list,
# then a list with the single task that has the task_id.
def test_get_task_by_id_pass(client):
    initial_response = client.get("/tasks")
    assert initial_response.status_code == 200

    post_response = client.post(
        "/tasks", json={"title": "Test Task", "description": "A test"}
    )
    assert post_response.status_code == 201

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 200

    data = get_response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "A test"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


# Test 4: Get a single task by id FAIL  |  GET /tasks/{task_id}
# Expected result: 404 Status Code upon looking for a task
# where the task_id doesn't exist.
def test_get_task_by_id_fail(client):
    initial_response = client.get("/tasks")
    assert initial_response.status_code == 200

    get_response = client.get("/tasks/9999")
    assert get_response.status_code == 404

    data = get_response.json()
    assert data["detail"] == "Task not found"


# Test 5: Update a task via task id PASS  |  PUT /tasks/{task_id}
# Expected result: 200 Status Code with the updated fields
# in the JSON body.
def test_update_single_task_pass(client):
    post_response = client.post(
        "/tasks", json={"title": "Test Task", "description": "A test"}
    )
    assert post_response.status_code == 201

    put_response = client.put(
        "/tasks/1",
        json={
            "title": "NEW Test Task",
            "description": "NEW description",
            "completed": True,
        },
    )
    assert put_response.status_code == 200

    new_data = put_response.json()
    assert new_data["title"] == "NEW Test Task"
    assert new_data["description"] == "NEW description"
    assert new_data["completed"] is True
    assert "id" in new_data
    assert "created_at" in new_data


# Test 6: Update a task via task id FAIL  |  PUT /tasks/{task_id}
# Expected result: 404 Status Code for a task where task_id is
# not found.
def test_update_single_task_fail(client):
    put_response = client.put(
        "/tasks/9999",
        json={
            "title": "NEW Test Task",
            "description": "NEW description",
            "completed": True,
        },
    )
    assert put_response.status_code == 404

    new_data = put_response.json()
    assert new_data["detail"] == "Task not found"


# Test 7: Delete a task via task id PASS  |  DELETE /tasks/{task_id}
# Expected result: 204 Status with no response body
# Checks GET /tasks/{task_id} to ensure a 404 response
def test_delete_task_pass(client):
    post_response = client.post(
        "/tasks", json={"title": "Test Task", "description": "A test"}
    )
    assert post_response.status_code == 201

    delete_response = client.delete("/tasks/1")
    assert delete_response.status_code == 204

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 404

    data = get_response.json()
    assert data["detail"] == "Task not found"


# Test 8: Delete a task via task id FAIL  |  DELETE /tasks/{task_id}
# Expected result: 404 Status Code, task to be deleted couldn't be found.
def test_delete_task_fail(client):
    delete_response = client.delete("/tasks/9999")
    assert delete_response.status_code == 404

    data = delete_response.json()
    assert data["detail"] == "Task not found"
