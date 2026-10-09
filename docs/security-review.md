# セキュリティレビュー

- 実施日: 2026-10-09
- 対象: リポジトリ全体(コミット`f1ac358`時点の追跡ファイル、全ブランチのgit履歴、ローカルの`.git/hooks/`)
- 重要度の基準: 高はRCE・情報漏洩・認証回避に直結するもの、中は特定条件下で大きな影響があるもの、低は多層防御上の改善点や影響の小さいもの

## 結果概要

| 重要度 | 件数 |
| --- | --- |
| 高 | 0 |
| 中 | 0 |
| 低 | 4(うち3件は対応済みのため削除。内容はコミット`5416470`時点の本ファイルを参照) |

本サイトはサーバー側処理やユーザー入力を持たない静的サイトで、描画される内容はすべてリポジトリ所有者が書いたものです。このため、XSSやインジェクションにつながる攻撃者制御の入力経路は存在しません。

## 指摘事項

### 1. [低] セキュリティ関連のレスポンスヘッダーが未設定

- 該当箇所: `public/`(`_headers`ファイルが存在しない)
- 分類: 多層防御
- 内容: Content-Security-Policy、`frame-ancestors`(またはX-Frame-Options)、Strict-Transport-Securityが送出されていません。2026-10-09に公開サイトの応答を確認したところ、X-Content-Type-Options: nosniffとReferrer-Policyは、Cloudflare Pagesが既定で付与していました(初版ではX-Content-Type-Optionsも未送出と記載していたため訂正)。
- 想定シナリオ: 現状は入力フォームやログインがないため実害は小さいものの、将来ページに生HTMLや外部スクリプトを追加した際の被害を抑える手段がありません。また、第三者サイトにiframeで埋め込まれます。
- 推奨対応: Cloudflare Pagesの`public/_headers`で、少なくとも`Content-Security-Policy: frame-ancestors 'none'`を設定する。KaTeXを使うページがあるため、`script-src`を絞る場合は`cdn.jsdelivr.net`と`onload`属性のインラインハンドラへの配慮が必要。
