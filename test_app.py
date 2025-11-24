
import pytest
from fastapi.testclient import TestClient
from app.database import SessionLocal, init_db
from app import models
from app.main import app, get_db


@pytest.fixture(scope="function")
def db_session():
    # Ensure DB file exists and tables are created
    init_db()
    db = SessionLocal()
    # Clean todos table before each test for isolation
    db.query(models.Todo).delete()
    db.commit()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Test: /health endpoint returns status and payload
# Terminal: Should show status 200 and JSON {"status": "ok"}
def test_health(client):
    print("TEST: /health endpoint returns status and payload")
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# Test: Create a todo and list todos
# Terminal: Should show status 201 for creation, 200 for listing, and correct todo data
def test_create_and_list(client):
    print("TEST: Create a todo and list todos")
    r = client.get("/todos")
    assert r.status_code == 200
    assert r.json() == []
    r = client.post("/todos", json={"title": "Task 1"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Task 1"
    assert data["id"] == 1
    assert data["done"] is False
    r = client.get("/todos")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["title"] == "Task 1"


# Test: Update todo title and done status
# Terminal: Should show status 200 and updated fields for title and done
def test_update_title_and_done(client):
    print("TEST: Update todo title and done status")
    r = client.post("/todos", json={"title": "Initial"})
    assert r.status_code == 201
    tid = r.json()["id"]
    r = client.put(f"/todos/{tid}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"
    r = client.put(f"/todos/{tid}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True


# Test: Delete a todo and check not found
# Terminal: Should show status 204 for delete, 404 for repeated delete
def test_delete_and_not_found(client):
    print("TEST: Delete a todo and check not found")
    client.post("/todos", json={"title": "a"})
    client.post("/todos", json={"title": "b"})
    r = client.delete("/todos/1")
    assert r.status_code == 204
    r = client.delete("/todos/1")
    assert r.status_code == 404


# Test: Update a non-existent todo
# Terminal: Should show status 404 for missing todo
def test_update_nonexistent_returns_404(client):
    print("TEST: Update a non-existent todo")
    r = client.put("/todos/999", json={"title": "x"})
    assert r.status_code == 404


# Test: Create todo without title (validation)
# Terminal: Should show status 422 for missing required field
def test_create_requires_title(client):
    print("TEST: Create todo without title (validation)")
    r = client.post("/todos", json={})
    assert r.status_code == 422


# Test: Send invalid JSON to create endpoint
# Terminal: Should show status 422 for invalid request body
def test_invalid_json(client):
    print("TEST: Send invalid JSON to create endpoint")
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="httpx")
        r = client.post("/todos", data="not-json", headers={"Content-Type": "application/json"})
    assert r.status_code == 422
