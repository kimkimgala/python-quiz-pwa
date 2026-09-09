# Python Quiz PWA v1.2

Androidタブレット等で利用できる、オフライン対応の学習問題PWAです。

## v1.2 のポイント

v1.2では、1つの共通アプリから複数教材を選べる「カセット方式」に対応しました。

- `index.html`: 共通の学習アプリ本体
- `catalog.json`: 教材一覧（教材カタログ）
- `questions.json`: Python基礎教材
- `courses/cassette-demo.json`: カセット切替の動作確認用教材

起動時に `catalog.json` を読み込み、教材選択画面を表示します。教材を選ぶと、登録されたJSON教材を読み込みます。

## 新しい教材の追加方法

1. 新しい教材JSONを追加します。例: `courses/project-finance.json`
2. 教材内の `course_id` は他教材と重複しないIDにします。
3. `catalog.json` の `courses` に `id`, `title`, `description`, `file` を追加します。

原則として、新教材を追加するだけなら `index.html` の変更は不要です。

## 教材JSONの主な項目

- `course_id`: 教材を識別する一意ID。教材ごとの学習履歴分離にも使用します。
- `title`: 教材タイトル
- `subtitle`: サブタイトル
- `section_label`: 区分名（例: Day、章、分野）
- `clear_count`: 何回正解でクリアとするか
- `questions`: 問題一覧

各問題は `day`, `number`, `type`, `question`, `options`, `answer`, `explanation` を持ちます。

## 学習履歴

学習履歴は教材の `course_id` ごとに各端末のブラウザ `localStorage` に保存します。GitHubには送信しません。教材を切り替えても成績は混在しません。

Python v1.0 の既存履歴は `python-basic-v1` へ一度だけ自動移行します。

## オフライン

Service Workerがアプリ本体、教材カタログ、取得済み教材をキャッシュします。JSONはオンライン時には最新版を取得し、取得できない場合はキャッシュを利用します。
