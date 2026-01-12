from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_add_multiple_todos():
    # reset module state
    import todo as todo_module
    todo_module.todos.clear()
    todo_module._next_id = 1

    res1 = client.post("/todos", json={"title": "t1", "due_date": None})
    assert res1.status_code == 200
    res2 = client.post("/todos", json={"title": "t2", "due_date": None})
    assert res2.status_code == 200

    r = client.get("/todos")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2


def test_mark_complete():
    import todo as todo_module
    todo_module.todos.clear()
    todo_module._next_id = 1

    res = client.post("/todos", json={"title": "t1", "due_date": None})
    assert res.status_code == 200
    todo = res.json()["todo"]
    tid = todo["id"]

    res2 = client.post(f"/todos/{tid}/complete")
    assert res2.status_code == 200

    r = client.get("/todos")
    data = r.json()
    assert len(data) == 1
    assert data[0]["completed"] is True


def test_update_todo():
    import todo as todo_module
    from datetime import date

    todo_module.todos.clear()
    todo_module._next_id = 1

    res = client.post("/todos", json={"title": "orig", "due_date": None})
    assert res.status_code == 200
    todo = res.json()["todo"]
    tid = todo["id"]

    new_due = (date.today()).isoformat()

    # update title and due_date
    res2 = client.put(
        f"/todos/{tid}", json={"title": "updated", "due_date": new_due})
    assert res2.status_code == 200

    r = client.get("/todos")
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == "updated"
    assert data[0]["due_date"] == new_due

    # update completed flag
    res3 = client.put(f"/todos/{tid}", json={"completed": True})
    assert res3.status_code == 200
    r2 = client.get("/todos")
    assert r2.json()[0]["completed"] is True
