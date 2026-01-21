# LLM Structured Output Todo App

LLM（大規模言語モデル）を活用した構造化出力対応のTodoアプリです。自然言語でタスクを追加・完了・更新でき、バックエンドはFastAPI、フロントエンドはReact+Viteで構成されています。

## 構成

- `backend/` : FastAPIによるAPIサーバー（LLM連携、タスク管理）
- `frontend/` : React + Viteによるフロントエンド

---

## セットアップ手順

### 1. バックエンド

1. Python仮想環境の作成・有効化
   ```bash
   cd backend
   python3 -m venv llm-venv
   source llm-venv/bin/activate
   ```
2. 依存パッケージのインストール
   ```bash
   pip install -r requirements.txt
   ```
3. 環境変数（`.env`）の設定例
   ```env
   LLM_API_KEY=sk-...   # OpenAI APIキー等
   LLM_API_BASE=https://api.openai.com/v1
   LLM_MODEL=gpt-3.5-turbo
   ```
4. サーバー起動
   ```bash
   uvicorn app:app --reload
   ```

### 2. フロントエンド

1. 依存パッケージのインストール
   ```bash
   cd ../frontend
   npm install
   ```
2. 環境変数ファイル（`.env`）の作成例
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```
   ※APIのURLはバックエンドの起動ポート・環境に合わせて調整してください。
3. 開発サーバー起動
   ```bash
   npm run dev
   ```

---

## 主なAPIエンドポイント（バックエンド）

- `POST /input` : 自然言語入力をLLMで解釈し、タスク操作
- `GET /todos` : タスク一覧取得
- `POST /todos` : タスク追加
- `PUT /todos/{id}` : タスク更新
- `POST /todos/{id}/complete` : タスク完了
