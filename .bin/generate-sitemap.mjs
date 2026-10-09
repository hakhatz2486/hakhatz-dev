// dist/内のHTMLを走査し、各ページの元ファイルのgit履歴から最終更新日を引いてpublic/sitemap.xmlを生成する。
// public/に書き出すのは、次回ビルド時に静的アセットとしてdist/へそのままコピーされるようにするため。
// dist/を材料にするため、実行前にnpm run buildでdist/を最新にしておく必要がある。
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteUrl = "https://hakhatz.dev/";

const repoRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const htmlDir = path.join(repoRoot, "dist");
const sitemapPath = path.join(repoRoot, "public", "sitemap.xml");

// 直下のファイルを先に、サブディレクトリを後に、それぞれ名前順で返す。
// 出力順を固定し、実行環境によってサイトマップに無意味な差分が出ないようにするため。
function listHtmlFiles(dir) {
  const entries = readdirSync(dir, { withFileTypes: true }).sort((a, b) =>
    a.name < b.name ? -1 : a.name > b.name ? 1 : 0,
  );
  const files = entries
    .filter((e) => e.isFile() && e.name.endsWith(".html"))
    .map((e) => path.join(dir, e.name));
  const nested = entries
    .filter((e) => e.isDirectory())
    .flatMap((e) => listHtmlFiles(path.join(dir, e.name)));
  return [...files, ...nested];
}

// dist/はgit管理外のため、対応する元ファイルのパスでgit logを引く。
// 元ファイルはsrc/pages/直下のフラットな<name>.md、フォルダ+index.mdまたはindex.astro(blog一覧)、src/content/配下の.md(blog記事)が混在するため、候補を順に存在確認する。
function sourcePathFor(relPath) {
  if (relPath.endsWith("index.html")) {
    const dirPart = relPath.slice(0, -"index.html".length);
    const name = dirPart.replace(/\/+$/, "");
    const candidates = [
      path.join(repoRoot, "src", "pages", `${name}.md`),
      path.join(repoRoot, "src", "pages", dirPart, "index.md"),
      path.join(repoRoot, "src", "pages", dirPart, "index.astro"),
      path.join(repoRoot, "src", "content", `${name}.md`),
    ];
    return candidates.find((c) => existsSync(c)) ?? candidates[0];
  }
  return path.join(
    repoRoot,
    "src",
    "pages",
    `${relPath.slice(0, -".html".length)}.md`,
  );
}

function lastmodFor(srcPath, htmlPath) {
  try {
    const date = execFileSync(
      "git",
      ["log", "-1", "--format=%cd", "--date=format:%Y-%m-%d", srcPath],
      { cwd: repoRoot, encoding: "utf8", stdio: "pipe" },
    ).trim();
    // 未コミットの新規ページは履歴がないため、今日の日付を使う
    return date || new Date().toISOString().slice(0, 10);
  } catch {
    // gitが使えない環境では、ビルド出力の更新日時で代用する
    return statSync(htmlPath).mtime.toISOString().slice(0, 10);
  }
}

let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

for (const htmlPath of listHtmlFiles(htmlDir)) {
  const relPath = path.relative(htmlDir, htmlPath).split(path.sep).join("/");
  const lastmod = lastmodFor(sourcePathFor(relPath), htmlPath);
  const urlPath = relPath.endsWith("index.html")
    ? relPath.slice(0, -"index.html".length)
    : relPath;

  xml += "  <url>\n";
  xml += `    <loc>${siteUrl}${urlPath}</loc>\n`;
  xml += `    <lastmod>${lastmod}</lastmod>\n`;
  xml += "  </url>\n";
}

xml += "</urlset>\n";

writeFileSync(sitemapPath, xml, "utf8");
console.log(`Generated ${sitemapPath}`);
