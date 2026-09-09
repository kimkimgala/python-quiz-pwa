# スタディカード 共有教材登録手順書

> 用途: 開発者・教材登録管理者向け運用手順
> 基準: 2026-09-09 完成版
> 関連: `DEVELOPMENT_CONCEPT.md`、`UIUX_V2_IMPLEMENTATION_SPEC.md`、`../README.md`

## 1. 目的と基本方針

新しい共有教材を、アプリ本体や既存の学習履歴を変更せずに配信カタログへ登録する。基本手順は「教材作成 → 共有用JSON書き出し → courses/へ追加 → 検証 → mainへ反映 → 利用者が追加」である。教材本体と学習エンジンを分離する開発コンセプトを維持する。

通常の「自分の教材として保存」は端末内の個人教材保存であり、GitHubへの公開ではない。共有用JSONを書き出しても自動公開されない。共有登録は開発者がGitHubで行う。公開前に、教材内容の正確性、著作権・利用許諾、個人情報・社内機密の混入がないことを確認する。

## 2. 登録対象とファイル配置

リポジトリ: `kimkimgala/python-quiz-pwa`

- `courses/*.json`: 新しい共有教材。`courses/`直下に配置する。
- `questions.json`: 既存Python教材。互換性維持のため既存のまま扱う。
- `catalog.json`: 自動生成される配信教材一覧。手動編集しない。
- `tools/build_catalog.py`: 教材検証・カタログ生成。
- `.github/workflows/build-catalog.yml`: GitHub Actionsの自動処理。

例: `courses/electrical-safety-v1.json`。ファイル名は教材IDと揃えると管理しやすい。教材IDは英数字で始まり、英数字・ハイフン・アンダースコアのみを使用する。既存教材と重複させない。

## 3. 教材の作成

1. アプリの「教材を作成」を開く。
2. Step 1「基本情報」で教材ID、教材名、説明、クリア回数等を入力する。
3. Step 2「問題入力」で問題を個別入力するか、CSVひな型を利用して一括読込する。読み込んだ問題は画面で確認・修正する。
4. Step 3「保存・書き出し」で内容チェックとJSONプレビューを確認する。
5. 「共有用JSONを書き出す」でJSONファイルを保存する。

Excel等を使う場合は、アプリからCSVひな型を保存し、CSV UTF-8（コンマ区切り）で保存して読み込む。基本列は `章,問題番号,問題形式,問題文,選択肢A,選択肢B,選択肢C,選択肢D,正解,解説`。必須列は章、問題番号、問題文、選択肢A、選択肢B、正解、解説。問題形式と選択肢C・Dは省略可能である。

## 4. JSON形式と検証条件

現行形式の例（内容は説明用）:

```json
{
  "course_id": "electrical-safety-v1",
  "title": "電気安全 基礎",
  "description": "電気設備の安全管理を学ぶ教材",
  "section_label": "章",
  "clear_count": 3,
  "category": "電気",
  "difficulty": "初級",
  "audience": "新人技術者",
  "author": "開発者",
  "version": "1.0",
  "updated_at": "2026-09-09",
  "study_time": "約30分",
  "tags": ["電気", "安全"],
  "questions": [
    {
      "day": 1,
      "number": 1,
      "type": "四者択一",
      "question": "ここに問題文",
      "options": [["A", "選択肢A"], ["B", "選択肢B"], ["C", "選択肢C"], ["D", "選択肢D"]],
      "answer": "A",
      "explanation": "ここに解説"
    }
  ]
}
```

`tools/build_catalog.py` の主な検証条件は次のとおり。

- トップレベルはJSONオブジェクト。`course_id`と`title`は空でない文字列。
- `clear_count`は1以上の整数。省略時は3。
- `questions`は1問以上の配列。
- 各問題に`day`、`number`、`question`、`options`、`answer`、`explanation`が存在する。
- 問題番号は教材内で重複しない。問題文は空でない文字列、解説は文字列。
- 選択肢は2個以上で、各要素は`[キー, 表示文]`。キーは重複せず、正解は存在する選択肢キーと一致する。
- `section_label`は省略可能（既定値「区分」）。指定時は空でない文字列。
- `description`は省略可能。`subtitle`も説明の代替に利用される。
- `category`、`difficulty`、`audience`、`author`、`version`、`updated_at`、`study_time`は任意の文字列。`tags`は任意の文字列配列。
- 全教材間で`course_id`が重複しない。

ブラウザ側の入力チェックとGitHub側の検証は別である。GitHub側の検証成功は教材内容の事実確認・著作権確認まで保証するものではない。

## 5. 推奨登録手順（作業ブランチ・PR方式）

### 5.1 GitHub Web画面で追加

1. GitHubのリポジトリを開き、`main`の最新状態を確認する。
2. ブランチ選択から新しい作業ブランチを作る。例: `course/electrical-safety-v1`。
3. 作業ブランチの`courses`フォルダを開く。
4. 「Add file」→「Upload files」で共有用JSONを選択する。既存教材を上書きしないようファイル名を確認する。
5. 変更内容を確認してcommitする。
6. Pull requestを作成し、`main`を取り込み先にする。
7. Actionsの「Build course catalog」を確認する。PRでは生成結果と`catalog.json`の差分がないことも検査されるため、新教材を追加しただけのPRはこのチェックが失敗する場合がある。その場合は、次の5.2の方法で作業ブランチ上の`catalog.json`を生成してcommitする。検証を無効化して通さない。
8. PRの差分を確認し、問題なければmainへmergeする。
9. main側の「Build course catalog」が成功したことを確認する。必要な場合はActionsが`catalog.json`を自動commitする。

### 5.2 PCで検証・カタログ生成する方法

Pythonが利用できるPCでは、リポジトリのルートで次を実行する。`catalog.json`は手で編集せず、生成スクリプトを使う。

```powershell
python tools/build_catalog.py
```

成功時は`OK: generated catalog.json with ... courses`と表示される。エラー時は表示されたファイル名・項目を修正して再実行する。PR方式では生成された`catalog.json`も教材JSONとともにcommitする。

Git操作の例（作業ブランチを作成済みの場合）:

```powershell
git status
git add courses/electrical-safety-v1.json catalog.json
git commit -m "content: add electrical safety course"
git push
```

`git status`で意図しない変更がないことを確認してからcommitする。新しいブランチを初めてpushする際に上流ブランチの指定を求められた場合は、表示された案内に従う。

### 5.3 mainへ直接追加する場合

現在のworkflowはmainへの教材JSON追加でも自動起動し、検証後に`catalog.json`を更新する。ただし、検証前の教材がmainへ入るため、通常はPR方式を推奨する。直接追加する場合も、事前にローカル検証と内容確認を行う。

## 6. 自動登録の仕組み

`Build course catalog`は、mainへのpush、main向けPR、手動実行に対応する。教材JSON等の変更時に`python tools/build_catalog.py`を実行する。対象はルートの`questions.json`と`courses/`直下のJSONである。生成される`catalog.json`には教材ID、タイトル、説明、ファイルパスおよび任意メタデータが入る。

PRでは`catalog.json`が生成結果と一致するか確認する。mainへのpushまたは手動実行では、差分があればActionsが生成ファイルをcommit/pushする。Actionsの成功と必要なカタログ更新を確認してから登録完了とする。

## 7. 利用者側での確認

1. アプリをオンラインで開き、必要に応じて再読み込みする。
2. 「教材を追加」を開き、新しい教材名を検索する。
3. 「マイ教材に追加」を選び、マイ教材に表示されることを確認する。
4. 「この教材を学ぶ」から問題・選択肢・正解・解説が正常に表示されることを確認する。
5. PC・スマートフォンで表示を確認する。既存教材や学習履歴が維持されていることも確認する。

新教材は利用者のマイ教材へ自動追加されない。既存の2教材`python-basic-v1`と`cassette-demo-v1`だけは移行互換性のため既定登録の扱いがある。学習履歴は教材IDごとに端末のlocalStorageへ保存され、GitHubへ送信されない。

## 8. 既存教材の更新と注意事項

既存教材を更新する場合は、同じ教材IDのまま内容を変更するか、新しい教材IDで別教材として配信するかを先に決める。現行の学習履歴は教材IDと問題番号に紐づくため、既存IDで問題番号の意味を変更すると過去の成績が別問題に引き継がれるおそれがある。既存の問題番号と意味を維持するか、互換性を保てない変更では新しい教材IDを採用する。

共有教材と同じIDの個人教材は保存時に拒否される。公開後のID衝突を避けるため、登録前に既存の共有教材IDを確認する。個人教材のバックアップ・復元は共有教材の公開操作ではない。

## 9. エラー時の確認

| 症状 | 確認すること |
| --- | --- |
| Actionsが失敗 | エラーログのファイル名・項目を確認し、JSON形式、必須項目、ID・問題番号重複、正解キーを修正する。 |
| PRでカタログ差分エラー | 作業ブランチで`python tools/build_catalog.py`を実行し、生成された`catalog.json`をcommitする。 |
| 教材が候補に出ない | mainへの反映、Actions成功、catalog.jsonへの登録、オンラインでの再読み込みを確認する。 |
| 教材を開けない | catalog.jsonの`file`が実際の教材JSONを指しているか、JSONが取得できるか確認する。 |
| 古い表示が残る | オンラインで再読み込みする。オフライン時は取得済みキャッシュが利用される場合がある。 |
| 学習履歴が想定と異なる | 教材IDと問題番号の変更有無を確認する。既存履歴を安易に削除しない。 |

## 10. 登録完了チェック

- [ ] 教材内容・公開権限・機密情報を確認した。
- [ ] 教材IDが既存教材と重複せず、JSONを`courses/`直下に配置した。
- [ ] 教材の内容チェックとGitHub側の検証が成功した。
- [ ] PRの差分を確認し、mainへ反映した。
- [ ] main側のActions成功とcatalog.jsonへの登録を確認した。
- [ ] 利用者の「教材を追加」から追加・学習できることを確認した。
- [ ] 既存教材・学習履歴への意図しない影響がないことを確認した。

## 11. 関連ファイル

- `DEVELOPMENT_CONCEPT.md`: 開発の基本方針。
- `UIUX_V2_IMPLEMENTATION_SPEC.md`: UI/UX v2.0の確定仕様。
- `../README.md`: 既存機能・教材形式の説明。
- `../tools/build_catalog.py`: 検証・生成の実装。
- `workflows/build-catalog.yml`: 自動登録workflow。

本書は2026-09-09時点の実装を基準とする。将来、登録方式・教材形式・保存方式を変更する場合は、開発コンセプトとの整合性と後方互換性を確認し、必要に応じて本書も更新する。
