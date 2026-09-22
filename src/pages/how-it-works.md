---
layout: /src/layouts/Layout.astro
title: "このサイトの仕組み"
description: "hakhatz.devの技術的な構成、公開の仕組み、ライセンスをまとめたページです。"
---

# このサイトの仕組み

hakhatz.devの技術的な構成、公開の仕組み、ライセンスをまとめたページです。

## 目次

## 技術スタック

- [Astro](https://astro.build/): 静的サイトジェネレーター(SSG)。各ページはMarkdownで書かれ、ビルド時に静的なHTMLへ変換される
- [remark-toc](https://github.com/remarkjs/remark-toc): Markdownページ内の`## 目次`見出し直下に見出し一覧へのリンクを自動生成する
- [KaTeX](https://katex.org/): 本文に`$$`や`\(...\)`などの数式区切り文字が含まれる場合に自動で有効化される
- Astro Content Collections: ブログ記事の一覧化・日付順の並び替えに使用(他のページとは異なる管理方式)
- [Cloudflare Pages](https://pages.cloudflare.com/): ホスティングプラットフォーム

## 公開の流れ

コードは[GitHub](https://github.com/hakhatz2486/hakhatz-dev)で管理しています。
`main`ブランチにpushすると、Cloudflare Pagesが自動的にビルドとデプロイを行い、このサイトに反映されます。

## 設計方針

- 装飾は最小限に留め、スタイリングよりも読みやすさとシンプルさを優先する
- HTMLとブラウザのデフォルトを主軸に、CSSとJavaScriptは補助として使う
- [WCAG](https://waic.jp/translations/WCAG22/)レベルAAを目標に、コントラスト比やフォントサイズなどのアクセシビリティに配慮する
- [motherfuckingwebsite](https://motherfuckingwebsite.com/)系のミニマリズムを参考にする

## ライセンス

ソースコード(HTML/CSS/JS)は[MIT License](https://opensource.org/license/mit)、コンテンツ(テキスト・画像・その他メディア)は[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)です。

## ソースコード

[GitHubリポジトリ](https://github.com/hakhatz2486/hakhatz-dev)で全文を公開しています。
ディレクトリ構成や開発コマンドなどの詳細は、リポジトリの[README](https://github.com/hakhatz2486/hakhatz-dev/blob/main/README.md)を参照してください。
