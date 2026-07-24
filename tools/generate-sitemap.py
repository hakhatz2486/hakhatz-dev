import os
import subprocess
from datetime import datetime, timezone

# 基本設定
site_url = "https://hakhatz.dev/"

# スクリプトのベース位置からの相対パスを設定
base_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(base_dir, ".."))
html_dir = os.path.join(repo_root, "dist")
sitemap_path = os.path.join(repo_root, "public", "sitemap.xml")

xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

# public フォルダ内を走査
for root, dirs, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            # ファイルのフルパスを取得
            file_full_path = os.path.join(root, file)

            # dist/ からの相対パスを取得(URL用にパス区切りを`/`へ統一)
            rel_path = os.path.relpath(file_full_path, html_dir).replace(os.sep, "/")

            # 1. Gitの履歴から「最終更新日」を取得
            # dist/はgit管理外(.gitignore)のため、対応するsrc/pages/内の
            # 元ファイルのパスでgit logを引く
            src_rel = rel_path[: -len("index.html")] + "index.md"
            src_full_path = os.path.join(repo_root, "src", "pages", src_rel)
            try:
                result_mod = subprocess.run(
                    [
                        "git",
                        "log",
                        "-1",
                        "--format=%cd",
                        "--date=format:%Y-%m-%d",
                        src_full_path,
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                    encoding="utf-8",
                )
                lastmod_date = result_mod.stdout.strip()
                if not lastmod_date:
                    lastmod_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            except (subprocess.CalledProcessError, FileNotFoundError):
                mtime = os.path.getmtime(file_full_path)
                lastmod_date = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime(
                    "%Y-%m-%d"
                )

            # # 2. Gitの履歴から「最初のコミット日（作成日）」を取得
            # try:
            #     result_created = subprocess.run(
            #         [
            #             "git",
            #             "log",
            #             "--reverse",
            #             "-1",
            #             "--format=%cd",
            #             "--date=format:%Y-%m-%d",
            #             file_full_path,
            #         ],
            #         capture_output=True,
            #         text=True,
            #         check=True,
            #         encoding="utf-8",
            #     )
            #     created_date = result_created.stdout.strip()
            #     if not created_date:
            #         created_date = datetime.now().strftime("%Y-%m-%d")
            # except (subprocess.CalledProcessError, FileNotFoundError):
            #     created_date = lastmod_date  # エラー時は最終更新日を流用

            # URLの構築ルール
            if rel_path == "index.html":
                url_path = ""
            elif rel_path.endswith("index.html"):
                url_path = rel_path[:-10]  # 末尾の index.html を削除
            else:
                url_path = rel_path

            # XMLへの書き出し（カスタムタグ <created> を追加）
            xml_content += "  <url>\n"
            xml_content += f"    <loc>{site_url}{url_path}</loc>\n"
            xml_content += f"    <lastmod>{lastmod_date}</lastmod>\n"
            # xml_content += f"    <created>{created_date}</created>\n" # createdは無効化
            xml_content += "  </url>\n"

xml_content += "</urlset>\n"

# public/sitemap.xml として書き出し
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"Generated {sitemap_path}")
