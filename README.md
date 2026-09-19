# Nichome - Watson's Blog

个人博客，2026 年起由 Hexo 迁移至 [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题。

- 线上地址：<https://ulsonhu.cn>
- 部署：`master` 分支存放 Hugo 源码，push 后由 GitHub Actions 自动构建并发布到 `gh-pages` 分支（GitHub Pages 源）。

## 日常写作

```bash
# 本地预览（需要 Hugo extended 版，https://gohugo.io/installation/）
hugo server

# 新建文章（编辑生成的 md 文件，把 draft 改为 false）
hugo new content posts/my-new-post.md
```

文章 front matter 参考：

```yaml
---
title: "文章标题"
date: 2026-09-19
categories: ["分类"]
tags: ["标签"]
math: true   # 需要 LaTeX 公式（$...$ / $$...$$）时开启
---
```

不写 `url` 字段时，文章地址为 `/posts/<文件名>/`。2018 年及以前的旧文章保留了原始 URL（根级 `/<中文标题>.html`）。

## 目录说明

- `content/posts/` — 全部文章（旧文由 Hexo 静态产物恢复，恢复脚本见 `scripts/restore.py`，清单见 `manifest.md`）
- `static/` — CNAME、图片、favicon
- `themes/PaperMod/` — 主题（已 vendor，无子模块依赖）
- `layouts/partials/extend_head.html` — MathJax 3 注入（仅 `math: true` 页面加载）
- `.github/workflows/deploy.yml` — 自动部署

## 网络提示

本机访问 GitHub 需走代理，仓库已配置 `http.proxy=http://127.0.0.1:7897`（`git config --local` 查看）。
