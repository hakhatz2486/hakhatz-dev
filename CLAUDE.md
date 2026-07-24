# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際にClaude Code (claude.ai/code) に向けたガイダンスを提供します。

## 概要

hakhatz.dev — Astroで構築された個人サイト(日本語コンテンツ)。GitHub連携によりCloudflare Pagesへ自動デプロイされる(pushするだけでよく、このリポジトリ内で個別のデプロイコマンドを実行する必要はない)。

設計方針(README記載): 装飾は最小限に留め、スタイリングよりも読みやすさ・シンプルさを優先する。HTMLとブラウザのデフォルトを主軸に、CSS/JSは補助として使用する。Google Lighthouseでパフォーマンスを確認する。motherfuckingwebsite.com系のミニマリズムを参考にしている。

## コマンド

- `npm run dev` — 開発サーバーを起動(`localhost:4321`)
- `npm run build` — 本番ビルド(`dist/`に出力)
- `npm run preview` — 本番ビルドをプレビュー
- `tools/serve.ps1` — 代替手段。すでにビルド済みの`public/`ディレクトリをPythonの`http.server`でポート8000から直接配信する(Astroのビルド工程を経ない)

テストスイートおよびlintスクリプトは設定されていない。フォーマットは`prettier-plugin-astro`を使ったPrettier(`.prettierrc`)を使用するが、npmスクリプトとしては配線されていないため、必要なら`npx prettier --write .`を直接実行する。

## アーキテクチャ

- `src/pages/` — ファイルベースルーティング。各フォルダ下の`index.md`がそのルートに対応する(例: `src/pages/profile/index.md` → `/profile`)。全ページがMarkdownで書かれており、frontmatterの`layout`で`src/layouts/Layout.astro`への相対パスを指定し、`title`/`description`/`useKatex`もfrontmatterで渡す。本文はCommonMarkで記述し、素のMarkdownで表現できない部分(画像タグなど)は生HTMLをそのまま埋め込める。Astro標準のShikiによりフェンスコードブロックが自動でハイライトされる(`astro.config.mjs`の`markdown.shikiConfig`参照)。
- `src/layouts/Layout.astro` — 唯一の共通ページシェル(header/footer/`<head>`)。Props: `title`, `description`, `useKatex`(CDN経由でKaTeXを読み込み数式レンダリングを有効化)。Markdownページの`layout` frontmatterから呼ばれた場合、propsは`Astro.props.frontmatter`に入るため、Layout.astro側で両対応している。
- `src/layouts/templates/index.md` — 新規ページ追加時にコピーするための空ページテンプレート(title/descriptionは空、useKatexはoff)。`src/pages/<name>/index.md`と同じく`src`から2階層下にあるため、`layout`の相対パスはそのままコピー先でも通用する。
- importパスの癖: Viteのエイリアスによりベアな`src`が`/src`にマッピングされる(`astro.config.mjs`と`tsconfig.json`の`paths`参照)。現状ページは全てMarkdown化されておりこのエイリアスを使うページはないが、今後`.astro`コンポーネントを追加する場合に備えて設定は残している。
- `public/` — サイトルートにそのまま配信される静的アセット: `css/`(スタイルシート), `images/`(アイコン・写真)。テーマはGruvboxのライト/ダークパレットを`public/css/style.css`内のCSSカスタムプロパティで実装し、`prefers-color-scheme`で切り替える。リポジトリルートの`color.table`はこれらの値の元になっているGruvboxパレットの参照表。
- `tools/` — Astroのビルドには含まれない、独立した開発・保守用スクリプト群:
  - `generate-sitemap.py` — `astro build`の出力先である`dist/`内の`*.html`を走査し(`public/`ではない。実行前に`npm run build`が必要)、`public/sitemap.xml`を生成する。`public/`に書き出すのは、次回ビルド時に静的アセットとして`dist/`へそのままコピーされるようにするため。ファイルごとの`<lastmod>`は`git log`から取得。
  - `escape-code.py` — argvまたは標準入力からのテキストをHTMLエスケープする(コードサンプルを`.astro`のマークアップに貼り付ける際に便利)。
  - `tree.py` — リポジトリのディレクトリ構造をYAML形式でダンプする(`.git`, `node_modules`, `.astro`などは除外)。
  - `serve.ps1` — 上記コマンド参照。
- `.git/hooks/post-commit` + `post-commit.ps1` — ローカル(未追跡)のフックで、コミット後に`tools/generate-sitemap.py`を実行してサイトマップを再生成し、差分があればコミットにamendする。以前は呼び出しパスが`tools/`へのディレクトリ名変更に追従できておらず壊れていたが、現在は修正済み。ただし`generate-sitemap.py`は`dist/`を走査するため、事前に`npm run build`でビルドしていないとサイトマップが空になる点に注意。

## ライセンス

ソースコード(HTML/CSS/JS)はMIT License、コンテンツ(テキスト・画像・その他メディア)はCC BY 4.0。ファイルを追加・流用する際はこの区別に留意する。
