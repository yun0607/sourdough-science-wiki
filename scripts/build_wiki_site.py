#!/usr/bin/env python3
"""Render the approved Wiki as one static HTML page."""
from dataclasses import dataclass
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from lint_wiki import CATEGORIES, ROOT, check


TITLE = '酸種麵包科學 Wiki'
INLINE = re.compile(
    r'\[(?P<source>SRC-\d{3})\]'
    r'|\[(?P<label>[^\]\n]+)\]\((?P<url>[^)\s]+)\)'
    r'|\*\*(?P<strong>[^*\n]+)\*\*'
)
LIST_ITEM = re.compile(r'^(?P<marker>\d+\.|-) (?P<text>.+)$')


@dataclass
class Article:
    article_id: str
    filename: str
    category: str
    title: str
    body: str
    references: dict


def load_articles():
    articles = []
    for path in sorted((ROOT / 'wiki/articles').glob('W*.md')):
        metadata, markdown = path.read_text(encoding='utf-8').split('\n---\n', 1)
        fields = dict(line.split(': ', 1) for line in metadata.splitlines()[1:])
        if fields['status'] != 'approved':
            continue
        title_line, body = markdown.lstrip().split('\n', 1)
        if not title_line.startswith('# '):
            raise ValueError(f'{path.name}: expected article title first')
        bibliography = body.split('\n## 來源\n', 1)[1]
        references = dict(re.findall(r'^- \[(SRC-\d{3})\] (.+)$', bibliography, re.M))
        expected = {sid.strip() for sid in fields['source_ids'].strip('[]').split(',')}
        if set(references) != expected:
            raise ValueError(f'{path.name}: source list does not match article metadata')
        articles.append(Article(fields['article_id'], path.name, fields['category'],
                                title_line[2:], body, references))
    return articles


def external_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.netloc:
        raise ValueError(f'Unsupported reference URL: {url}')
    return escape(url, quote=True)


def render_inline(text, article_ids):
    """Render the Wiki's citation, link, and emphasis syntax as safe HTML."""
    chunks = []
    offset = 0
    for match in INLINE.finditer(text):
        chunks.append(escape(text[offset:match.start()]))
        if match['source']:
            source = match['source']
            chunks.append(f'<a class="citation" href="#ref-{source}">[{source}]</a>')
        elif match['url']:
            url = match['url']
            href = f'#{article_ids[url]}' if url in article_ids else external_url(url)
            chunks.append(f'<a href="{href}">{escape(match["label"])}</a>')
        else:
            chunks.append(f'<strong>{escape(match["strong"])}</strong>')
        offset = match.end()
    chunks.append(escape(text[offset:]))
    return ''.join(chunks)


def render_body(markdown, article_ids):
    for block in re.split(r'\n\s*\n', markdown.strip()):
        lines = block.splitlines()
        if len(lines) == 1:
            heading = re.fullmatch(r'(#{2,3}) (.+)', block)
            if heading:
                level = len(heading[1]) + 2
                name = heading[2]
                css_class = ' class="body-heading"' if name == '正文' else ''
                yield f'<h{level}{css_class}>{render_inline(name, article_ids)}</h{level}>'
                continue

        items = [LIST_ITEM.fullmatch(line) for line in lines]
        if all(items):
            start_marker = items[0]['marker']
            tag = 'ul' if start_marker == '-' else 'ol'
            start = '' if start_marker in {'-', '1.'} else f' start="{int(start_marker[:-1])}"'
            yield f'<{tag}{start}>'
            for item in items:
                yield f'<li>{render_inline(item["text"], article_ids)}</li>'
            yield f'</{tag}>'
            continue

        css_class = ''
        if block.startswith('**摘要：**'):
            css_class = ' class="summary"'
        elif block.startswith('**關鍵字：**'):
            css_class = ' class="keywords"'
        yield f'<p{css_class}>{render_inline(block, article_ids)}</p>'


def render_topic(number, category, articles, article_ids):
    yield f'<section class="topic" id="topic-{number}" tabindex="-1">'
    yield f'<h2>{escape(category)}</h2>'
    for article in articles:
        aid = article.article_id
        yield f'<article id="{aid}" aria-labelledby="title-{aid}" tabindex="-1">'
        yield f'<div class="article-id">{aid}</div>'
        yield f'<h3 id="title-{aid}">{escape(article.title)}</h3>'
        yield from render_body(article.body, article_ids)
        yield '</article>'
    yield '</section>'


def render_reference(source, articles, article_ids):
    sid = source['source_id']
    citing = [article for article in articles if sid in article.references]
    # The approved citation line preserves publication details and date qualifiers.
    bibliography = render_inline(citing[0].references[sid], article_ids)
    primary_url = external_url(source['url'])
    original = source.get('candidate_url')
    original_link = (
        f' <a href="{external_url(original)}">原始候選網址</a>'
        if original and original != source['url'] else ''
    )
    backlinks = '、'.join(f'<a href="#{article.article_id}">{article.article_id}</a>'
                         for article in citing)
    return (
        f'<li id="ref-{sid}" tabindex="-1"><strong class="source-id">{sid}</strong>'
        f'<p class="bibliography">{bibliography}</p>'
        f'<p class="source-links"><a class="primary-source" href="{primary_url}">查閱原文</a>'
        f'{original_link} <span>引用文章 {backlinks}</span></p></li>'
    )


def render_page(articles, sources):
    article_ids = {article.filename: article.article_id for article in articles}
    groups = {category: [article for article in articles if article.category == category]
              for category in CATEGORIES}
    topic_links = []
    contents = []
    sections = []
    for number, (category, entries) in enumerate(groups.items(), 1):
        title = escape(category)
        topic_links.append(
            f'<li><a href="#topic-{number}"><span aria-hidden="true">{number:02}</span>'
            f'{title}</a></li>'
        )
        contents.extend(
            f'<li><a href="#{article.article_id}"><span>{article.article_id}</span>'
            f'{escape(article.title)}</a></li>' for article in entries
        )
        sections.extend(render_topic(number, category, entries, article_ids))
    references = [render_reference(source, articles, article_ids) for source in sources]

    return f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="從微生物科學到居家烘焙的酸種麵包入門 Wiki。">
  <title>{TITLE}</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="./wiki.css">
  <script src="./wiki.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">跳至主要內容</a>
  <div id="top" tabindex="-1"></div>
  <header class="site-header">
    <div class="frame">
      <a class="wordmark" href="#top">{TITLE}</a>
      <nav aria-label="全站導覽">
        <a href="#topics">主題</a>
        <a href="#contents">文章</a>
        <a href="#references">文獻</a>
      </nav>
    </div>
  </header>
  <main id="main" tabindex="-1">
    <div class="hero">
      <div class="frame hero-inner">
        <div>
          <h1>酸種麵包<span>科學 Wiki</span></h1>
          <p>從微生物科學到居家烘焙</p>
        </div>
        <div class="hero-art" aria-hidden="true">
          <div class="loaf"><i></i><i></i><i></i></div>
        </div>
      </div>
    </div>
    <div class="frame reading-layout">
      <aside class="navigator" aria-label="閱讀導覽">
        <nav id="topics" aria-labelledby="topics-title" tabindex="-1">
          <h2 id="topics-title">六大主題</h2>
          <ul class="topic-links">{''.join(topic_links)}</ul>
        </nav>
        <nav id="contents" aria-labelledby="contents-title" tabindex="-1">
          <h2 id="contents-title">文章目錄</h2>
          <ul class="contents-links">{''.join(contents)}</ul>
        </nav>
      </aside>
      <div class="reading">
        {chr(10).join(sections)}
        <section class="references" id="references" tabindex="-1">
          <h2>文獻書目</h2>
          <ul>{chr(10).join(references)}</ul>
        </section>
      </div>
    </div>
  </main>
  <footer class="site-footer">
    <div class="frame">
      <span>{TITLE}</span>
      <a href="#top">回到頂端</a>
    </div>
  </footer>
</body>
</html>
'''


def main():
    if check(7, True):
        print('Cannot build: strict Wiki validation failed.')
        return 1
    sources = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
    articles = load_articles()
    path = ROOT / 'docs/index.html'
    path.parent.mkdir(exist_ok=True)
    path.write_text(render_page(articles, sources), encoding='utf-8')
    print(f'Built {path} from {len(articles)} approved articles.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
