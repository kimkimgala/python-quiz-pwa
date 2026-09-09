# Python Quiz PWA v1.5

Androidタブレット等で利用できる、オフライン対応の学習問題PWAです。

## v1.5 のポイント

v1.5では、v1.4の「マイ教材方式」に、教材カタログの自動登録機能を追加しました。

- 新しい教材JSONを `courses/` に追加すると GitHub Actions が自動起動
- `tools/build_catalog.py` が全教材を検証
- 検証に成功すると `catalog.json` を自動生成・更新
- 新教材は利用者の「マイ教材」へ勝手に追加されず、「教材を追加」に候補として表示
- 既存のPython教材と動作確認教材はv1.4以前との互換性を維持
- `catalog.json` は自動生成ファイルとし、原則として人が直接編集しない

## 新しい教材を追加する流れ

通常の新教材は `courses/` にJSONファイルを1つ追加するだけです。

例:

```text
courses/project-finance-v1.json
```

教材JSONの例:

```json
{
  "course_id": "project-finance-v1",
  "title": "プロジェクトファイナンス基礎",
  "description": "プロジェクトファイナンスの基本事項を学習する教材",
  "subtitle": "基礎編",
  "section_label": "章",
  "clear_count": 3,
  "questions": []
}
```

実際の教材では `questions` に1問以上の有効な問題を入れてください。GitHubへ追加・pushすると、自動処理が教材を検証し、問題がなければ `catalog.json` に登録します。

新教材には `default_subscribed` を設定する必要はありません。v1.5では新教材は自動的に各利用者のマイ教材へ入りません。利用者自身が「教材を追加」から選択します。

## 自動検証

`tools/build_catalog.py` は主に次を確認します。

- JSONとして正しく読み込めること
- `course_id` と `title` が存在すること
- `course_id` が全教材で重複していないこと
- 問題が1問以上あること
- 問題番号が教材内で重複していないこと
- 選択肢が2個以上あること
- 選択肢キーが重複していないこと
- `answer` が実際の選択肢キーのいずれかであること
- `clear_count` が正の整数であること

検証に失敗した場合はGitHub Actionsがエラーとなり、壊れた内容で `catalog.json` は更新されません。

## 自動化ファイル

- `tools/build_catalog.py`: 教材検証・`catalog.json` 生成
- `.github/workflows/build-catalog.yml`: GitHub Actionsの実行定義
- `catalog.json`: 自動生成される配信教材カタログ

GitHub Actionsは `questions.json`、`courses/**/*.json`、自動生成スクリプト、ワークフロー定義の変更時に動作します。Pull Requestでは生成結果が一致しているか検証し、`main` へのpushでは必要な場合だけ `catalog.json` を自動コミットします。

## 既存Python教材について

既存のPython教材は互換性のため、当面 `questions.json` のまま自動生成対象に含めます。`course_id` は `python-basic-v1` のままなので、既存の学習履歴は維持されます。

既存の次の2教材だけはv1.3からv1.4への移行互換性のため、生成されたカタログで `default_subscribed: true` になります。

- `python-basic-v1`
- `cassette-demo-v1`

今後 `courses/` に追加する新教材は、自動登録されても各端末のマイ教材には自動追加されません。

## マイ教材

各端末の `localStorage` に、利用中の教材IDを保存します。

- 保存キー: `subscribed_courses_v1`

配信カタログに新教材が追加されると、各利用者がオンライン時に最新の `catalog.json` を取得します。新教材は「教材を追加」に表示され、本人が「マイ教材に追加」を押した教材だけが学習画面に表示されます。

マイ教材から外すときは、「成績を残す」「成績も削除する」を選択できます。

## カセット方式

- `index.html`: 共通の学習アプリ本体
- `catalog.json`: 自動生成される配信教材カタログ
- `questions.json`: 既存Python基礎教材
- `courses/*.json`: 追加教材カセット

教材JSON内の `course_id` は一意にしてください。

## 学習履歴

学習履歴は教材の `course_id` ごとに各端末のブラウザ `localStorage` に保存します。GitHubには送信しません。教材を切り替えても成績は混在しません。

Python v1.0 の既存履歴は `python-basic-v1` へ一度だけ自動移行します。

## オフライン

Service Workerがアプリ本体、教材カタログ、取得済み教材をキャッシュします。JSONはオンライン時には最新版を取得し、取得できない場合はキャッシュを利用します。

「マイ教材に追加」を押す際にも教材JSONを取得するため、オンラインで追加に成功した教材はその時点でキャッシュ対象になります。
