"""FastAPI アプリ（demoの出題API）。

エンドポイント:
  GET /health           動作確認＋建設業レコード件数
  GET /keywords         作業キーワードのプリセット一覧
  GET /quiz?keyword=... キーワードに応じた4択クイズを1問返す
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import quiz
from fetch_data import load

app = FastAPI(title="建設KYクイズ demo", version="0.1.0")

# ローカルのNext.js（既定 :3000）からの取得を許可する（demo用に緩め）。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "records": int(len(load()))}


@app.get("/keywords")
def keywords() -> dict:
    return {"keywords": quiz.list_keywords()}


@app.get("/quiz")
def get_quiz(keyword: str = Query(..., description="作業キーワード（/keywords のいずれか）")) -> dict:
    try:
        return quiz.make_quiz(keyword)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
