# 建設KYクイズ demo

その日の作業を選ぶ → 実際の建設業災害事例（JNIOSH 2017）の「災害状況」を提示 →
起こりうる「事故の型」を4択で当てる → 公式ラベル（事故の型＋起因物）で答え合わせ。
データのみ・自己採点。LLM/RAGなし。

## 構成
- `api/` … FastAPI（データ層 `fetch_data.py` ＋ 出題 `quiz.py` / `main.py`）。env はSprint内（`api/.venv`）
- `web/` … Next.js（TS, App Router）1画面

## 起動手順
2つのターミナルで:

```sh
# ① バックエンド（:8000）
cd api
uv run uvicorn main:app --port 8000
#   初回のみ JNIOSH からデータを実行時取得（数秒）。以降は data/ のスナップショットを読む

# ② フロントエンド（:3000）
cd web
npm install   # 初回のみ
npm run dev
```

ブラウザで http://localhost:3000 を開く。

## API
- `GET /health` … 動作確認＋建設業レコード件数
- `GET /keywords` … 作業キーワード一覧（UIのプリセット）
- `GET /quiz?keyword=<ラベル>` … 4択クイズを1問（状況＋選択肢＋正解/起因物を同梱）

フロントのAPI接続先は `NEXT_PUBLIC_API_BASE`（既定 `http://localhost:8000`）。

## 既知の割り切り（v1）
- 正解・解説は `/quiz` 応答に同梱しフロントが回答後に開示（サーバ状態なし＝自己採点）
- 災害状況の文に結末が含まれ答えが漏れる場合がある（末尾結末の軽量マスクのみ）
- スコア履歴・出題スケジューリング・レベル別出し分けは未実装（2本目以降）
- データはJNIOSH規約によりコードのみ追跡（`data/` は .gitignore、実レコードは非公開）
