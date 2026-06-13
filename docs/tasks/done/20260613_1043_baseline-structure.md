# ベースライン構造の整備

## 目的・前提・方針案
- 目的: 1day Solution Sprintを反復するワークスペースのベースライン構造を整備する
- 前提: 構想md（mind/00_inbox/20260612_SolutionSprint構想.md）準拠。共通基盤の先行整備はしない（重複2回まで抽出禁止）
- 方針: 最小構成（README + docs + templates）。monorepoツール（Turborepo/Nx）は捨てる前提の規律と逆方向のため導入しない

## 計画
### Phase 1: 計画・意思決定
- [x] 構想md読み込み・現状把握・ベストプラクティス調査（monorepoツール不採用と判断）
- [x] 意思決定4点をユーザー確認：雛形=見出しのみ／git initのみ（GitHub化は後でユーザー）／demo起動手順はREADMEに記載／Sprintはルート直下（リポジトリ名は後でユーザーがsprintsに改名）

### Phase 2: ベースライン構築
- [x] git init（main、コミット対象は新規作成ファイルのみ。.claude/は独自gitを持つため対象外）
- [x] README.md作成：目的・規律・1日の流れ・構成図・demo起動手順（構想mdの要約）
- [x] docs/tasks/done/ と docs/themes.md（テーマ候補ストック）を作成
- [x] templates/sprint/ に brief/research/decision/retro の見出しのみ雛形を作成（demo/含む、cp -rでSprint開始）
- [x] .gitignore作成（node_modules, .venv, .next, .env 等）

## 実行ログ
（計画想定外の事象なし。.claude/が独自gitリポジトリのためroot追跡から除外、扱いはユーザー判断待ち）

## 結果
- ベースライン構造（README / docs / templates / .gitignore）を構築しmainに初回commit
- GitHub化・リポジトリ改名（solution-sprints）はユーザーが後で実施
- 次アクション: Sprint 01テーマ選定（docs/themes.mdに候補1件あり）
