# セキュリティレビュー

- 実施日: 2026-10-09
- 対象: リポジトリ全体(コミット`f1ac358`時点の追跡ファイル、全ブランチのgit履歴、ローカルの`.git/hooks/`)
- 重要度の基準: 高はRCE・情報漏洩・認証回避に直結するもの、中は特定条件下で大きな影響があるもの、低は多層防御上の改善点や影響の小さいもの

## 結果概要

| 重要度 | 件数 |
| --- | --- |
| 高 | 0 |
| 中 | 0 |
| 低 | 4 |

本サイトはサーバー側処理やユーザー入力を持たない静的サイトで、描画される内容はすべてリポジトリ所有者が書いたものです。このため、XSSやインジェクションにつながる攻撃者制御の入力経路は存在しません。

## 指摘事項

### 1. [低] `astro`の依存バージョンが`latest`指定になっている

- 該当箇所: `package.json:16`
- 分類: サプライチェーン
- 内容: `"astro": "latest"`はバージョン範囲を一切制限しません。`package-lock.json`があるため、Cloudflare Pagesのビルド(`npm clean-install`)ではロックされたバージョンが使われますが、ローカルで`npm install astro`や`npm update`を実行するとその時点の最新版(メジャー更新を含む)がロックファイルに取り込まれます。
- 想定シナリオ: astroパッケージやその依存が乗っ取られ悪意ある版が公開された時期に更新操作を行うと、その版がロックされ、ローカルのビルド環境およびCloudflare Pagesのビルドで実行されます。
- 推奨対応: 他の依存と同様にインストール済みのバージョンに合わせて`"astro": "^7.0.6"`のような範囲指定にする。

### 2. [低] セキュリティ関連のレスポンスヘッダーが未設定

- 該当箇所: `public/`(`_headers`ファイルが存在しない)
- 分類: 多層防御
- 内容: Content-Security-Policy、`frame-ancestors`(またはX-Frame-Options)、X-Content-Type-Optionsが送出されていません。
- 想定シナリオ: 現状は入力フォームやログインがないため実害は小さいものの、将来ページに生HTMLや外部スクリプトを追加した際の被害を抑える手段がありません。また、第三者サイトにiframeで埋め込まれます。
- 推奨対応: Cloudflare Pagesの`public/_headers`で、少なくとも`X-Content-Type-Options: nosniff`と`Content-Security-Policy: frame-ancestors 'none'`を設定する。KaTeXを使うページがあるため、`script-src`を絞る場合は`cdn.jsdelivr.net`と`onload`属性のインラインハンドラへの配慮が必要。

### 3. [低] post-commitフックが存在しないパスのスクリプトを実行しようとしている

- 該当箇所: `.git/hooks/post-commit.ps1:6`(未追跡のローカルファイル)、`.git/hooks/post-commit:10`
- 分類: ローカル実行環境
- 内容: フックは`python ./tools/generate-sitemap.py`を呼び出しますが、スクリプトは`.bin/`へ移動済みで、`tools/`は空のディレクトリとして残っています。`AGENTS.md`には「修正済み」とありますが、実際のフックは旧パスのままです。フック自体も`-ExecutionPolicy Bypass`で起動されます。
- 想定シナリオ: 別ブランチのチェックアウトや外部から取り込んだ変更で`tools/generate-sitemap.py`が置かれると、コミットのたびにそのスクリプトが無確認で実行されます。ただし`tools/`は`.gitignore`対象外のため`git status`で検知でき、悪用には書き込み権限が必要です。機能面では、現状サイトマップが自動再生成されていません。
- 推奨対応: `post-commit.ps1`のパスを`./.bin/generate-sitemap.py`に直し、空の`tools/`ディレクトリを削除する。

### 4. [低] 外部リンクにhttpが使われている

- 該当箇所: `src/pages/404.md:7`、`src/pages/sandbox.md:29`、`src/pages/sandbox.md:41`
- 分類: 通信の暗号化
- 内容: `http://scp-jp.wikidot.com/...`への平文リンクがあります。リンク先はhttpsに対応しています。
- 想定シナリオ: 公衆無線LANなどの中間者が、閲覧者がリンクを開いた際の遷移先を改ざんできます。
- 推奨対応: `https://`に置き換える。
- 対応状況: 2026-10-09に3か所とも`https://`へ変更済み。

## 問題なしと判断した項目

- `src/layouts/Layout.astro`の`set:html={bodyHtml}`: 入力はビルド時に描画された自前のMarkdown本文のみで、外部入力は含まれない。
- KaTeXのCDN読み込み: バージョン固定、`integrity`(SRI)と`crossorigin`が付与されている。
- `src/content.config.ts`: Zodスキーマで検証され、テンプレート側で自動エスケープされる。
- `.bin/generate-sitemap.py`: `subprocess.run`はリスト形式の引数でシェルを経由しない。走査対象は自前のビルド出力のみ。
- `.bin/escape-code.py`、`.bin/tree.py`: ローカル実行専用で、`yaml.dump`のみ使用し読み込み(デシリアライズ)は行わない。
- 秘密情報: 全ブランチの履歴(`package-lock.json`を除く)を検索し、APIキー・トークン・パスワード・秘密鍵は見つからなかった。削除済みファイル(`diff.txt`、`tools/serve.ps1`など)にも含まれていない。
- `.gitignore`: `dist/`、`.astro/`、`node_modules/`、`.zed/`が除外されている。
