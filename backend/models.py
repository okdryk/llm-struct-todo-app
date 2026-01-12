from pydantic import BaseModel, Field
from typing import Optional, Literal


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    due_date: Optional[str] = None


class TodoAction(BaseModel):
    """
    LLMが返す構造化出力の契約
    - update_todo: タスクを更新するための出力（id または title で対象を指定）
    """
    action: Literal["add_todo", "complete_todo", "update_todo", "unknown"] = Field(
        description="実行すべき操作"
    )
    id: Optional[int] = Field(
        description="対象となるタスクの ID（可能なら）"
    )
    title: Optional[str] = Field(
        description="対象となるタスク名 / 更新後のタイトル"
    )
    due_date: Optional[str] = Field(
        description="期限（相対表現可、ISO形式 YYYY-MM-DD）"
    )
    completed: Optional[bool] = Field(
        description="完了フラグ（true/false）、指定があれば更新される"
    )
