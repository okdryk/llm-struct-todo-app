from typing import List
from models import Todo

todos: List[Todo] = []
_next_id = 1


def add_todo(title: str, due_date: str | None) -> Todo:
    global _next_id
    todo = Todo(
        id=_next_id,
        title=title,
        due_date=due_date,
        completed=False,
    )
    todos.append(todo)
    _next_id += 1
    return todo


def complete_todo(title: str) -> Todo | None:
    for todo in todos:
        if todo.title == title:
            todo.completed = True
            return todo
    return None


def complete_todo_by_id(todo_id: int) -> Todo | None:
    """IDでタスクを完了にするユーティリティ（フロントエンドから直接呼ぶために追加）"""
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return todo
    return None


def update_todo_by_id(todo_id: int, title: str | None = None, due_date: str | None = None, completed: bool | None = None) -> Todo | None:
    """IDでタスクを更新するユーティリティ。未指定フィールドは変更しない。"""
    for todo in todos:
        if todo.id == todo_id:
            if title is not None:
                todo.title = title
            if due_date is not None:
                todo.due_date = due_date
            if completed is not None:
                todo.completed = completed
            return todo
    return None


def list_todos() -> List[Todo]:
    return todos
