"""建設業の労働災害データ取得モジュール（demoのデータ層）。

JNIOSH公開の死傷災害DB CSVを実行時にダウンロードし、建設業に絞った
スナップショットを作る。データ自体はリポジトリに含めない（.gitignore）。
私的使用の範囲で利用し、実レコードは配布・公開しない。

出典: 労働安全衛生総合研究所 労働災害（死傷）データベース
"""
from pathlib import Path
import urllib.request

import pandas as pd

BASE_URL = "https://www.jniosh.johas.go.jp/publication/houkoku/ROUSAIDB/SHISYO_{year}.csv"
DATA_DIR = Path(__file__).parent / "data"
INDUSTRY = "建設業"  # 業種（大分類）分類名 で絞る

# 元CSVの列名 → スナップショットの列名（名称列が元から入っており code.xlsx は不要）
COLUMNS = {
    "ID": "id",
    "災害状況": "situation",        # クイズの問題文
    "事故の型分類名": "accident_type",  # 正解ラベル
    "起因物（大分類）分類名": "agent",
    "業種（中分類）分類名": "work",
    "年齢": "age",
    "月": "month",
}


def _csv_path(year: int) -> Path:
    return DATA_DIR / f"SHISYO_{year}.csv"


def _snapshot_path(year: int) -> Path:
    return DATA_DIR / f"construction_{year}.parquet"


def fetch(year: int = 2017) -> Path:
    """年指定でCSVを実行時ダウンロード（既存ならスキップ）。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = _csv_path(year)
    if not path.exists():
        urllib.request.urlretrieve(BASE_URL.format(year=year), path)
    return path


def build_snapshot(year: int = 2017) -> Path:
    """建設業に絞り、必要列だけの parquet スナップショットを作る。"""
    df = pd.read_csv(fetch(year), dtype=str, encoding="utf-8")
    df = df[df["業種（大分類）分類名"].str.contains(INDUSTRY, na=False)]
    df = df[list(COLUMNS)].rename(columns=COLUMNS)
    df = df.dropna(subset=["situation", "accident_type"]).reset_index(drop=True)
    out = _snapshot_path(year)
    df.to_parquet(out, index=False)
    return out


def load(year: int = 2017) -> pd.DataFrame:
    """スナップショットを読む（なければ取得して生成）。アプリはこれを呼ぶ。"""
    if not _snapshot_path(year).exists():
        build_snapshot(year)
    return pd.read_parquet(_snapshot_path(year))


if __name__ == "__main__":
    df = load()
    print(f"建設業レコード: {len(df)}件")
    print(df[["situation", "accident_type", "agent", "age"]].head(3).to_string())