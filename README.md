# Python Quiz PWA v1.1

Androidタブレット等で利用できる、オフライン対応の学習問題PWAです。

## v1.1 のポイント

アプリ本体 (`index.html`) と教材データ (`questions.json`) を分離しました。
**別ジャンルに変更するときは、基本的に `questions.json` だけを差し替えます。**

`questions.json` の主な項目:

- `course_id`: 教材を識別するID（教材ごとの学習履歴を分けるため、一意にする）
- `title`: 教材タイトル
- `subtitle`: サブタイトル
- `section_label`: 区分名（例: Day、章、分野）
- `clear_count`: 何回正解でクリアとするか
- `questions`: 問題一覧

各問題は従来どおり `day`, `number`, `type`, `question`, `options`, `answer`, `explanation` を持ちます。`day` は名称上は互換性維持のため残していますが、画面表示は `section_label` で変更できます。

## オフライン

Service Workerがアプリ本体と教材をキャッシュします。`questions.json` はオンライン時に最新版を取得し、失敗した場合はキャッシュ版を利用します。

## 学習履歴

教材の `course_id` ごとにブラウザの localStorage に保存します。Python v1.0 の既存履歴は `python-basic-v1` へ自動移行します。
