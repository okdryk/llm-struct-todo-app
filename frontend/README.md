# フロントエンド (簡易 React + Vite)

ローカル開発手順

1. 依存をインストール

```bash
cd frontend
npm install
```

2. 開発サーバ起動

```bash
npm run dev
```

デフォルトでは `VITE_API_BASE_URL` は `http://localhost:8000` を参照します。バックエンドを別ポートで実行する場合は、`frontend/.env` に `VITE_API_BASE_URL` を設定してください。

バックエンドの起動例

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

注意: バックエンドにCORSを追加済みのため、開発サーバからのアクセスは許可されています。