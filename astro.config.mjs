// @ts-check
import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkToc from "remark-toc";

// https://astro.build/config
export default defineConfig({
  site: "https://hakhatz.dev",
  markdown: {
    // Markdown中に`## 目次`見出しを書くと、その直下に見出し一覧へのリンクを自動生成する
    processor: unified({
      remarkPlugins: [[remarkToc, { heading: "目次", tight: true }]],
    }),
    shikiConfig: {
      themes: {
        light: "github-light",
        dark: "github-dark",
      },
    },
  },
  vite: {
    resolve: {
      alias: {
        src: "/src",
      },
    },
  },
});
