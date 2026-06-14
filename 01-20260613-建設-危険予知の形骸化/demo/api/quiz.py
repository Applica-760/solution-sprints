"""出題ロジック（キーワード→situationフィルタ→1問生成）。

データのみ・自己採点のdemo本体。LLM/RAGなし。`fetch_data.load()` が返す
建設業レコードから、作業キーワードに該当する災害状況を1件抽選し、
事故の型を当てる4択クイズを組み立てる。
"""
import random
import re

import pandas as pd

from fetch_data import load

# 作業キーワード（ラベル → situation部分一致の一致語リスト）。
# 一致語は実データ（2017建設業3,900件）でヒット件数を確認済み。
KEYWORDS: dict[str, list[str]] = {
    "高所・足場": ["足場", "高所", "はしご", "脚立", "屋根", "梁", "開口部", "親綱"],
    "掘削・土砂": ["掘削", "土砂", "法面", "溝", "埋設", "地山"],
    "重機・クレーン": ["クレーン", "重機", "ショベル", "バックホウ", "ユンボ", "フォークリフト", "玉掛"],
    "電動工具": ["電動", "グラインダ", "丸のこ", "サンダー", "切断機", "ドリル", "カッター"],
    "解体": ["解体", "取り壊", "撤去"],
    "運搬・荷役": ["運搬", "荷下ろし", "荷上げ", "積み込", "台車", "手押"],
}

# ダミー選択肢の母集団（建設業で件数の多い主要な事故の型）。
MAIN_TYPES: list[str] = [
    "墜落、転落",
    "はさまれ、巻き込まれ",
    "転倒",
    "飛来、落下",
    "切れ、こすれ",
    "激突され",
    "激突",
    "崩壊、倒壊",
]

N_CHOICES = 4  # 正解1 + ダミー3

# 結末を示しがちな語（簡易マスクの判定に使う）。
_OUTCOME_RE = re.compile(r"[^。]*(受傷|負傷|死亡|被災|骨折|裂傷|挫滅|切断|やけど|火傷|感電し)[^。]*。\s*$")


def list_keywords() -> list[str]:
    """UIのプリセット供給用。キーワードのラベル一覧を返す。"""
    return list(KEYWORDS)


def _filter(df, keyword: str):
    words = KEYWORDS.get(keyword)
    if not words:
        return df.iloc[0:0]
    mask = df["situation"].str.contains("|".join(map(re.escape, words)), na=False)
    return df[mask]


def mask_outcome(situation: str) -> str:
    """末尾の結末節（受傷/負傷/死亡 等を含む文末1節）を粗く除去する軽量マスク。

    1節しか落とさない保守的な実装。誤除去や効果が薄ければ呼び出し側で無効化する。
    """
    masked = _OUTCOME_RE.sub("", situation).strip()
    # 全消し・実質空になった場合は元文を返す（やり過ぎ防止）。
    return masked if len(masked) >= 10 else situation


def _build_choices(correct: str) -> list[str]:
    pool = [t for t in MAIN_TYPES if t != correct]
    distractors = random.sample(pool, k=min(N_CHOICES - 1, len(pool)))
    choices = distractors + [correct]
    random.shuffle(choices)
    return choices


def make_quiz(keyword: str, mask: bool = True) -> dict:
    """キーワードに該当する1件を抽選してクイズを組み立てる。

    返却物に正解・解説を同梱する（自己採点demoの最簡実装。フロントが回答後に開示）。
    """
    df = _filter(load(), keyword)
    if df.empty:
        raise ValueError(f"no records for keyword: {keyword}")

    row = df.sample(n=1).iloc[0]
    correct = row["accident_type"]
    situation = mask_outcome(row["situation"]) if mask else row["situation"]

    return {
        "keyword": keyword,
        "situation": situation,
        "choices": _build_choices(correct),
        "answer": {
            "accident_type": correct,
            "agent": None if pd.isna(row["agent"]) else row["agent"],
        },
    }
