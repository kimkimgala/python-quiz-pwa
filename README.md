# Python基礎集中講座 PWA版 v1.0

## 機能
- Androidホーム画面へインストール
- オフライン利用
- Day別／全問／シャッフル
- 間違えた問題だけ再出題
- 未クリア問題だけ再出題
- 正解・不正解回数を端末保存
- 3回正解でクリア
- Day別学習状況
- 学習履歴リセット

## GitHub Pagesで公開する手順
1. GitHubで新しいリポジトリを作成。
2. ZIP内のファイルをリポジトリ直下へアップロード。
3. GitHubの Settings → Pages。
4. Sourceを「Deploy from a branch」。
5. Branchを `main`、Folderを `/ (root)` にしてSave。
6. 発行されたGitHub Pages URLをAndroid Chromeで開く。
7. Chromeの「アプリをインストール」または「ホーム画面に追加」を選ぶ。

## 注意
PWAのService Workerは通常HTTPS配信が必要です。端末内のindex.htmlを直接開く方式では、
PWAインストールやオフラインキャッシュが正しく動かないことがあります。

## 収録問題
49問。元原稿では問146が欠けているためDay 10のみ4問です。

## 学習履歴
localStorageに保存されます。ブラウザデータを削除すると履歴も消えます。
