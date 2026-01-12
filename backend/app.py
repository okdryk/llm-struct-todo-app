from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from llm import parse_user_input
from todo import add_todo, complete_todo, list_todos, complete_todo_by_id, update_todo_by_id

app = FastAPI(title="LLM Structured Output Todo Demo")

# 開発時にフロントエンド（Viteなど）からアクセスできるようCORSを許可します
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateTodo(BaseModel):
    title: str
    due_date: Optional[str] = None


@app.post("/todos")
def create_todo(payload: CreateTodo):
    """
    直接タスクを追加するエンドポイント（LLMを使わないデバッグ用／フロントエンドの直接追加用）
    """
    # 正規化: 相対表現（"明日まで" など）を ISO 日付に変換します
    try:
        from date_utils import normalize_due_date
        norm = normalize_due_date(payload.due_date)
    except Exception:
        norm = payload.due_date

    todo = add_todo(payload.title, norm)
    return {"result": "added", "todo": todo}


class UpdateTodo(BaseModel):
    title: Optional[str] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None


@app.put("/todos/{todo_id}")
def update_todo_endpoint(todo_id: int, payload: UpdateTodo):
    """直接タスクを更新するエンドポイント（部分更新を許可）"""
    # due_date が相対表現の場合は正規化する
    norm = None
    if payload.due_date is not None:
        try:
            from date_utils import normalize_due_date
            norm = normalize_due_date(payload.due_date)
        except Exception:
            norm = payload.due_date

    todo = update_todo_by_id(todo_id, title=payload.title,
                             due_date=norm, completed=payload.completed)
    if todo:
        return {"result": "updated", "todo": todo}
    return {"result": "not_found"}


@app.post("/input")
def handle_input(text: str):
    """
    自然言語入力を受け取り、LLMで解釈してTodo操作を行う
    """
    from datetime import datetime

    now = datetime.now().astimezone().isoformat()
    action = parse_user_input(text, now=now)
    print(action)
    match action.action:
        case "add_todo":
            # タイトルがない場合は追加しないでエラーを返す（LLMの応答が不正な可能性）
            if not action.title or action.title.strip() == "":
                print("[handle_input] skipped add: missing title", action)
                return {"result": "invalid", "reason": "missing_title"}

            todo = add_todo(action.title, action.due_date)
            # デバッグログ
            try:
                print(
                    f"[handle_input] added todo id={todo.id} title={todo.title} total={len(list_todos())}")
            except Exception:
                pass
            return {"result": "added", "todo": todo}

        case "complete_todo":
            todo = complete_todo(action.title)
            if todo:
                return {"result": "completed", "todo": todo}
            return {"result": "not_found"}

        case "update_todo":
            # サポート: id を優先して更新、なければ title で先頭マッチを探す
            if action.id is None and (action.title is None or action.title.strip() == ""):
                return {"result": "invalid", "reason": "missing_target"}

            # 正規化
            from date_utils import normalize_due_date
            norm = None
            if action.due_date is not None:
                norm = normalize_due_date(action.due_date)

            # update by id
            if action.id is not None:
                todo = update_todo_by_id(
                    action.id, title=action.title, due_date=norm, completed=action.completed)
                if todo:
                    return {"result": "updated", "todo": todo}
                return {"result": "not_found"}

            # update by title (first match)
            for t in list_todos():
                if t.title == action.title:
                    todo = update_todo_by_id(
                        t.id, title=action.title, due_date=norm, completed=action.completed)
                    return {"result": "updated", "todo": todo}
            return {"result": "not_found"}

        case _:
            return {"result": "unknown"}


@app.post("/todos/{todo_id}/complete")
def complete_todo_endpoint(todo_id: int):
    """フロントエンドから直接呼ぶための完了エンドポイント（LLMを経由しない）"""
    todo = complete_todo_by_id(todo_id)
    if todo:
        return {"result": "completed", "todo": todo}
    return {"result": "not_found"}


@app.get("/todos")
def get_todos():
    """
    Todo一覧（状態表示用）
    """
    return list_todos()
