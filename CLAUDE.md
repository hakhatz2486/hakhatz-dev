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

- `src/pages/` — ファイルベースルーティング。各フォルダ下の`index.astro`がそのルートに対応する(例: `src/pages/profile/index.astro` → `/profile`)
- `src/layouts/Layout.astro` — 唯一の共通ページシェル(header/footer/`<head>`)。Props: `title`, `description`, `usePrism`(ローカルの`/css/prism.css` + `/js/prism.js`を読み込みコードハイライトを有効化), `useKatex`(CDN経由でKaTeXを読み込み数式レンダリングを有効化)。全ページが`<Layout ...>`でコンテンツをラップする。
- `src/layouts/templates/index.astro` — 新規ページ追加時にコピーするための空ページテンプレート(title/descriptionは空、両レンダーフラグはoff)。
- importパスの癖: Viteのエイリアスによりベアな`src`が`/src`にマッピングされる(`astro.config.mjs`と`tsconfig.json`の`paths`参照)。そのため各ページはレイアウトを`import Layout from "src/layouts/Layout.astro"`という形でimportしており、相対パス(`../../layouts/...`)ではない。
- `public/` — サイトルートにそのまま配信される静的アセット: `css/`(スタイルシート), `js/`(Prismなどのベンダースクリプト), `images/`(アイコン・写真)。テーマはGruvboxのライト/ダークパレットを`public/css/style.css`内のCSSカスタムプロパティで実装し、`prefers-color-scheme`で切り替える。リポジトリルートの`color.table`はこれらの値の元になっているGruvboxパレットの参照表。
- `tools/` — Astroのビルドには含まれない、独立した開発・保守用スクリプト群:
  - `generate-sitemap.py` — `public/`内の`*.html`を走査(つまり`src/`ではなく`astro build`後に実行する必要がある)し、`public/sitemap.xml`を生成する。ファイルごとの`<lastmod>`は`git log`から取得。
  - `escape-code.py` — argvまたは標準入力からのテキストをHTMLエスケープする(コードサンプルを`.astro`のマークアップに貼り付ける際に便利)。
  - `tree.py` — リポジトリのディレクトリ構造をYAML形式でダンプする(`.git`, `node_modules`, `.astro`などは除外)。
  - `serve.ps1` — 上記コマンド参照。
- `.git/hooks/post-commit` + `post-commit.ps1` — ローカル(未追跡)のフックで、サイトマップを自動再生成しコミットにamendする意図のもの。ただし現状`.ps1`は`./scripts/generate-sitemap.py`を呼び出しており、実際のスクリプトは`tools/generate-sitemap.py`に存在する — このパスは古くなっている/壊れている可能性が高い。修正する場合は`tools/`を移動するのではなく、フックスクリプト側のパスを直す。

## ライセンス

ソースコード(HTML/CSS/JS)はMIT License、コンテンツ(テキスト・画像・その他メディア)はCC BY 4.0。ファイルを追加・流用する際はこの区別に留意する。
