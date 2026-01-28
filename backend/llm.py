from typing import Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
from models import TodoAction

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_API_BASE"),
)

MODEL = os.getenv("LLM_MODEL")

SYSTEM_PROMPT = """
あなたはTodoアプリの操作を判断するAIです。
ユーザーの入力文から意図を読み取り、
与えられたJSON Schemaに厳密に従って出力してください。

JSON以外の文章は一切出力しないでください。
予定は日本語で記述してください。
相対表現で表された表現はそのままにしてください。
具体例を示します。

入力：2026-01-24に資料を作る
{
  "action": "add_todo",
  "id": null,
  "title": "資料を作る",
  "due_date": "2026-01-24",
  "completed": false,
  "needs_clarification": false,
  "question": null
}

入力：明日までにカレーを作る
{
  "action": "add_todo",
  "id": null,
  "title": "カレーを作る",
  "due_date": "明日",
  "completed": false,
  "needs_clarification": false,
  "question": null
}

"""


def parse_user_input(text: str, now: Optional[str] = None) -> TodoAction:
    """Parse the user input and include an optional current datetime string when calling the LLM.

    - `now` should be an ISO8601 string (e.g. produced by datetime.now().astimezone().isoformat()).
    - If `now` is not provided, the function will generate it locally.
    """
    schema = TodoAction.model_json_schema()

    if now is None:
        now = datetime.now().astimezone().isoformat()

    # Provide the current datetime to the model as additional user context; the model
    # should use it when interpreting relative date expressions.
    timestamp_message = f"現在の日時: {now} (ISO8601形式)。この日時を基準に期限表現を解釈してください。"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
            # {"role": "user", "content": timestamp_message},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "todo_action",
                "schema": schema,
            },
        },
        max_tokens=512,
        temperature=0.2,
        top_p=0.95
    )

    content = response.choices[0].message.content
    return TodoAction.model_validate_json(content)
