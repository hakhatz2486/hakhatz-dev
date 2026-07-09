# hakhatz.dev

個人サイト

## 方針

- 静的ファイルで構築
- 装飾は最小限に留め、シンプルさによる資格負荷の低減の面から読みやすさを追求する
- HTMLとブラウザのデフォルトに主軸を置き、補助としてCSS/JSを使用する
- Google Lighthouseを活用してパフォーマンスの改善に努める
- [motherfuckingwebsite](https://motherfuckingwebsite.com/)や[派生サイト](https://github.com/lyoshenka/awesome-motherfucking-website)を参考にする

## 技術スタック

- Astro: 静的サイトジェネレーター(SSG)として使用
- Cloudflare Pages: ホスティングプラットフォームとして使用、GitHubと連携して自動デプロイを構築

## ディレクトリ構成

- `.git/hooks/`
    - `post-commit`: PowerShellから`post-commit`を実行するためのスクリプト
    - `post-commit.ps1`: `hakhatz-dev/scripts/generate-sitemap.py`を実行しサイトマップを生成する
- `public/`: 公開される静的ファイルのルート
    - `css/`: スタイルシート
    - `images/`: アイコンや画像
    - `js/`: JavaScript(現在(2026-06-06)は未使用)
- `scripts/`: 開発・保守用スクリプトを格納する
    - `escape-code.py`: テキストを実体参照に変換するスクリプト
    - `generate-sitemap.py`: サイトマップ(`public/sitemap.xml`)を自動生成するスクリプト
    - `serve.ps1`: Pythonの標準機能を利用して、ローカル環境で簡易的なWebサーバーを起動するスクリプト
    - `tree.py`: ディレクトリ構造をYAML形式で出力するスクリプト

## ローカル開発環境

本プロジェクトはWindowsで開発されています。動作確認をする場合はWindows PowerShellの使用を推奨します。

### 実行例

```PowerShell
npm run dev
```

ブラウザで`localhost:4321`に接続する。

## [ライセンス](LICENSE)

### ソースコード

HTML, CSS, JavaScript, その他ソースコード
[MIT License](https://opensource.org/license/mit)

### コンテンツ

テキスト、画像、その他メディアのライセンス
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### サードパーティ

- [Prism.js](https://prismjs.com/) (MIT License)
