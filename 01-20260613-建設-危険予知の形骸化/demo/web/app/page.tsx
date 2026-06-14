"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type Quiz = {
  keyword: string;
  situation: string;
  choices: string[];
  answer: { accident_type: string; agent: string | null };
};

export default function Home() {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [picked, setPicked] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/keywords`)
      .then((r) => r.json())
      .then((d) => setKeywords(d.keywords))
      .catch(() => setError("APIに接続できません（バックエンドを起動してください）"));
  }, []);

  async function loadQuiz(keyword: string) {
    setPicked(null);
    setError(null);
    try {
      const r = await fetch(`${API_BASE}/quiz?keyword=${encodeURIComponent(keyword)}`);
      if (!r.ok) throw new Error();
      setQuiz(await r.json());
    } catch {
      setError("出題に失敗しました");
    }
  }

  const correct = quiz?.answer.accident_type;

  return (
    <main style={{ maxWidth: 680, margin: "0 auto", padding: 24, lineHeight: 1.7 }}>
      <h1 style={{ fontSize: 22 }}>建設KYクイズ（demo）</h1>
      <p style={{ color: "#666", fontSize: 14 }}>
        今日の作業を選ぶ → 起こりうる「事故の型」を当てる。実際の災害事例（建設業）から出題。
      </p>

      <section>
        <h2 style={{ fontSize: 15 }}>① 今日の作業を選ぶ</h2>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {keywords.map((k) => (
            <button
              key={k}
              onClick={() => loadQuiz(k)}
              style={{
                padding: "6px 12px",
                border: "1px solid #ccc",
                borderRadius: 6,
                background: quiz?.keyword === k ? "#1d4ed8" : "#fff",
                color: quiz?.keyword === k ? "#fff" : "#000",
                cursor: "pointer",
              }}
            >
              {k}
            </button>
          ))}
        </div>
      </section>

      {error && <p style={{ color: "#c00" }}>{error}</p>}

      {quiz && (
        <section style={{ marginTop: 24 }}>
          <h2 style={{ fontSize: 15 }}>② 状況：どんな事故が起こりうる？</h2>
          <p style={{ background: "#f4f4f5", padding: 12, borderRadius: 8 }}>{quiz.situation}</p>

          <div style={{ display: "grid", gap: 8 }}>
            {quiz.choices.map((c) => {
              const isAnswer = c === correct;
              const isPicked = c === picked;
              let bg = "#fff";
              if (picked) {
                if (isAnswer) bg = "#dcfce7";
                else if (isPicked) bg = "#fee2e2";
              }
              return (
                <button
                  key={c}
                  disabled={!!picked}
                  onClick={() => setPicked(c)}
                  style={{
                    padding: "10px 12px",
                    textAlign: "left",
                    border: "1px solid #ccc",
                    borderRadius: 6,
                    background: bg,
                    cursor: picked ? "default" : "pointer",
                  }}
                >
                  {c}
                  {picked && isAnswer && " ✓"}
                </button>
              );
            })}
          </div>

          {picked && (
            <div style={{ marginTop: 16 }}>
              <p style={{ fontWeight: 600 }}>
                {picked === correct ? "正解！" : "不正解"} — 公式の事故の型は「{correct}」
              </p>
              {quiz.answer.agent && (
                <p style={{ fontSize: 14, color: "#555" }}>起因物（大分類）：{quiz.answer.agent}</p>
              )}
              <button
                onClick={() => loadQuiz(quiz.keyword)}
                style={{ marginTop: 8, padding: "8px 14px", borderRadius: 6, cursor: "pointer" }}
              >
                同じ作業でもう1問
              </button>
            </div>
          )}
        </section>
      )}
    </main>
  );
}
