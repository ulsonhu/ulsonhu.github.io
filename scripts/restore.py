#!/usr/bin/env python3
"""Restore 46 Hexo posts from generated static output to Hugo markdown.

Sources:
  - search.xml          : full post bodies (CDATA HTML)
  - <post>.html         : date / category / tags / description metadata
Output:
  - ../content/posts/<slug>.md
  - ../manifest.md      : restore checklist
"""
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from markdownify import markdownify as md

SITE_DIR = "/Users/peter/Downloads/ulsonhu.github.io"
OUT_DIR = "/Users/peter/Downloads/blog-staging/content/posts"
MANIFEST = "/Users/peter/Downloads/blog-staging/manifest.md"

# filename (from search.xml link) -> repo-friendly slug
SLUGS = {
    "2018就飘着.html": "floating-2018",
    "Excel知识点备忘.html": "excel-notes",
    "HMM-隐马尔可夫模型.html": "hmm",
    "JQuery源码解读 01.html": "jquery-source-1",
    "JQuery源码解读 02-对象构建.html": "jquery-source-2",
    "JUMP少年周刊-最全漫画排行榜.html": "jump-manga-ranking",
    "LASSO回归算法.html": "lasso",
    "Lunar_Year.html": "2017-lunar-year",
    "MCMC与Gibbs采样.html": "mcmc-gibbs",
    "MacOS下使用python的多版本方案.html": "macos-python-versions",
    "MySQL语句学习及总结.html": "sql-notes",
    "Note-关于事件的运算.html": "note-events-operation",
    "Python字符串处理拾掇.html": "python-string",
    "SAS基础学习篇(一).html": "sas-basics-1",
    "SVM支持向量机.html": "svm",
    "Schwarz不等式知识归纳.html": "schwarz-inequality",
    "VC维理论-统计学习理论基础.html": "vc-dimension",
    "new_year_2018.html": "books-movies-2018",
    "优化算法篇之梯度法.html": "gradient-methods",
    "优化算法篇之牛顿法.html": "newton-method",
    "全局优化算法之模拟退火算法.html": "simulated-annealing",
    "全局优化算法之遗传算法.html": "genetic-algorithm",
    "全局搜索算法之粒子群算法.html": "pso",
    "共轭先验.html": "conjugate-prior",
    "写在大三下学期.html": "junior-year-thoughts",
    "唐璜节选.html": "don-juan-excerpt",
    "因果推断：工具变量（Instrumental Variable）.html": "instrumental-variable",
    "如何高效学习.html": "how-to-learn-notes",
    "广义矩估计(GMM)方法.html": "gmm",
    "广义线性模型(Generalized Linear Model).html": "glm",
    "指数分布族.html": "exponential-family",
    "接触向量自回归模型.html": "var-model",
    "数理统计学：世纪末的回顾与展望.html": "mathematical-statistics-review",
    "本科计量经济学之回炉重造篇.html": "econometrics-review",
    "概率论杂谈篇一.html": "probability-discrete-space",
    "概率论的两个问题-球盒模型、匹配问题.html": "probability-two-problems",
    "理解回调函数.html": "understanding-callback",
    "理解异步.html": "understanding-async",
    "理解拓扑空间的紧性.html": "topological-compactness",
    "用AngularJS写框架.html": "angularjs-framework",
    "用Tensorflow写简单的神经网络.html": "tensorflow-nn",
    "用python做数据分析与科学计算(篇一).html": "python-data-analysis-1",
    "矩阵分解相关知识回顾.html": "matrix-factorization",
    "等式约束与不等式约束问题.html": "constrained-optimization",
    "红楼梦-Dream of the Chamber.html": "dream-of-red-chamber",
    "网站迁移-hexo.html": "site-migration-hexo",
}


def extract_meta(filename):
    path = os.path.join(SITE_DIR, filename)
    if not os.path.exists(path):
        return {}
    s = open(path, encoding="utf-8").read()
    meta = {}
    m = re.search(r'datetime="([^"]+)"', s)
    if m:
        meta["date"] = m.group(1)[:10]
    m = re.search(r'<span class="post-category".*?href="/categories/([^/"]+)/"', s, re.S)
    if m:
        meta["categories"] = [urllib.parse.unquote(m.group(1))]
    tags = re.findall(r'href="/tags/([^/"]+)/"\s+rel="tag"', s)
    if not tags:
        tags = re.findall(r'href="/tags/([^/"]+)/" rel="tag"', s)
    meta["tags"] = [urllib.parse.unquote(t) for t in tags]
    m = re.search(r'<div class="post-description">(.*?)</div>', s, re.S)
    if m:
        desc = BeautifulSoup(m.group(1), "html.parser").get_text().strip()
        meta["description"] = re.sub(r"\s+", " ", desc)
    return meta


def convert_figures(soup):
    """Turn Hexo highlight figures into plain <pre><code class="language-x">."""
    for fig in soup.find_all("figure", class_="highlight"):
        classes = fig.get("class", [])
        lang = classes[1] if len(classes) > 1 else ""
        code_td = fig.find("td", class_="code")
        if code_td is None:
            continue
        for br in code_td.find_all("br"):
            br.replace_with("\n")
        text = code_td.get_text().strip("\n")
        pre = soup.new_tag("pre")
        code = soup.new_tag("code")
        if lang:
            code["class"] = f"language-{lang}"
        code.string = text
        pre.append(code)
        fig.replace_with(pre)


def _code_lang(el):
    code = el.find("code")
    if code:
        for c in code.get("class", []):
            if c.startswith("language-"):
                return c[len("language-"):]
    return ""


def clean_body(html):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", id="more"):
        a.decompose()
    convert_figures(soup)
    body_md = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        escape_asterisks=False,
        escape_underscores=False,
        wrap=False,
        code_language_callback=_code_lang,
    )
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()
    return body_md


def detect_math(body_md):
    stripped = re.sub(r"```.*?```", "", body_md, flags=re.S)
    stripped = re.sub(r"`[^`]*`", "", stripped)
    return bool(re.search(r"\$\$|\$[^$\n]+\$", stripped))


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tree = ET.parse(os.path.join(SITE_DIR, "search.xml"))
    entries = tree.getroot().findall("entry")
    manifest = [
        "# 恢复清单",
        "",
        "| # | 标题 | 日期 | 旧 URL | 分类 | 标签 | 外链图 | 公式 | 正文字数 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    problems = []
    for i, e in enumerate(entries, 1):
        title = e.findtext("title").strip()
        link = e.find("link").get("href")
        filename = urllib.parse.unquote(link.lstrip("/"))
        html = e.findtext("content") or ""
        meta = extract_meta(filename)
        if not meta.get("date"):
            problems.append(f"{filename}: 缺日期")
        slug = SLUGS.get(filename)
        if slug is None:
            slug = re.sub(r"\.html$", "", filename)
            problems.append(f"{filename}: 无 slug 映射，用原名")
        body = clean_body(html)
        has_math = detect_math(body)
        ext_imgs = re.findall(r"!\[[^\]]*\]\((https?://[^)]+)\)", body)
        fm = [
            "---",
            f"title: {yaml_str(title)}",
            f"date: {meta.get('date', '2016-01-01')}",
        ]
        if meta.get("categories"):
            fm.append("categories: [" + ", ".join(yaml_str(c) for c in meta["categories"]) + "]")
        if meta.get("tags"):
            fm.append("tags: [" + ", ".join(yaml_str(t) for t in meta["tags"]) + "]")
        if meta.get("description"):
            fm.append(f"description: {yaml_str(meta['description'])}")
        fm.append(f"url: {yaml_str('/' + filename)}")
        if has_math:
            fm.append("math: true")
        fm.append("---")
        out = "\n".join(fm) + "\n\n" + body + "\n"
        with open(os.path.join(OUT_DIR, slug + ".md"), "w", encoding="utf-8") as f:
            f.write(out)
        manifest.append(
            f"| {i} | {title} | {meta.get('date','-')} | {link} | "
            f"{'/'.join(meta.get('categories',[]))} | {'/'.join(meta.get('tags',[]))} | "
            f"{len(ext_imgs)} | {'Y' if has_math else ''} | {len(body)} |"
        )
    manifest += ["", "## 问题", ""] + [f"- {p}" for p in problems] if problems else []
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")
    print(f"restored {len(entries)} posts -> {OUT_DIR}")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" ", p)


if __name__ == "__main__":
    sys.exit(main())
