from fastapi.testclient import TestClient
from app import app
from models import TodoAction

client = TestClient(app)


def test_llm_add_multiple(monkeypatch):
    import todo as todo_module

    # reset
    todo_module.todos.clear()
    todo_module._next_id = 1

    # monkeypatch parse_user_input used by app (imported name)
    def fake_parse(text, now=None):
        return TodoAction(action="add_todo", title=text, due_date=None)

    import app as app_module
    monkeypatch.setattr(app_module, "parse_user_input", fake_parse)

    # Call /input twice
    r1 = client.post("/input", params={"text": "taskA"})
    assert r1.status_code == 200
    r2 = client.post("/input", params={"text": "taskB"})
    assert r2.status_code == 200

    r = client.get("/todos")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["title"] == "taskA"
    assert data[1]["title"] == "taskB"


def test_llm_missing_title_is_ignored(monkeypatch):
    import todo as todo_module

    todo_module.todos.clear()
    todo_module._next_id = 1

    # monkeypatch parse_user_input to return add_todo with no title
    from models import TodoAction

    def fake_parse(text, now=None):
        return TodoAction(action="add_todo", title=None, due_date=None)

    import app as app_module
    monkeypatch.setattr(app_module, "parse_user_input", fake_parse)

    r = client.post("/input", params={"text": "something"})
    assert r.status_code == 200
    assert r.json().get("result") == "invalid"

    r2 = client.get("/todos")
    assert r2.status_code == 200
    assert len(r2.json()) == 0


def test_llm_update_todo(monkeypatch):
    import todo as todo_module
    from models import TodoAction

    todo_module.todos.clear()
    todo_module._next_id = 1

    # create initial todo
    res = client.post("/todos", json={"title": "orig", "due_date": None})
    assert res.status_code == 200
    todo = res.json()["todo"]
    tid = todo["id"]

    # monkeypatch parse_user_input to return update_todo action
    def fake_update(text, now=None):
        return TodoAction(action="update_todo", id=tid, title="updated", due_date=None, completed=True)

    import app as app_module
    monkeypatch.setattr(app_module, "parse_user_input", fake_update)

    r = client.post("/input", params={"text": "更新してください"})
    assert r.status_code == 200
    assert r.json().get("result") == "updated"

    r2 = client.get("/todos")
    data = r2.json()
    assert len(data) == 1
    assert data[0]["title"] == "updated"
    assert data[0]["completed"] is True
