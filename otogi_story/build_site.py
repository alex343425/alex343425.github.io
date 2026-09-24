"""Build the dependency-free static story wiki in docs/ for GitHub Pages."""

from __future__ import annotations

import html
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "wiki"
OUTPUT = ROOT / "docs"
ASSETS = ROOT / "site_assets"
MAIN = [
    "第一部-群星的失樂園.md",
    "第二部-1-黃昏少女.md",
    "第二部-1.5-探求童話少女.md",
    "第二部-2-交錯天地.md",
    "第二部-3-照亮柱石的曙光.md",
    "第二部-4-融於暗影的華夏.md",
    "第二部-5-綻放於童話的蓮花暗焉.md",
    "第二部-5.5-星謐之獅.md",
    "第二部-6-灼燒天譜的星戰.md",
]
EXTRA = [
    "十二迷宮.md",
    "評議會創設秘話.md",
    "禁忌精靈傳承-盧恩茲奈特.md",
    "白璧微瑕的阿爾卡娜.md",
    "第九黎明.md",
    "魔宮流星譚.md",
]
REFERENCE = [
    "主要角色.md",
    "次要角色.md",
    "次要角色詳述.md",
    "世界設定.md",
    "組織與勢力.md",
    "波爾塔島事件史.md",
    "章節索引.md",
]

PAGES = [WIKI / "劇情總覽.md"]
PAGES += [WIKI / "主線" / name for name in MAIN]
PAGES += [WIKI / "番外篇" / name for name in EXTRA]
PAGES += [WIKI / name for name in REFERENCE]
PAGES += [ROOT / "術語表.md"]
SOURCES = sorted(ROOT.glob("*.txt")) + sorted((ROOT / "番外篇").glob("*.txt"))


def output_path(source: Path, base: Path) -> Path:
    if source == WIKI / "劇情總覽.md":
        return base / "index.html"
    if source == ROOT / "術語表.md":
        return base / "術語表.html"
    return base / source.relative_to(WIKI).with_suffix(".html")


def relative_url(from_page: Path, to_page: Path) -> str:
    relative = to_page.relative_to(from_page.parent) if to_page.parent == from_page.parent else None
    if relative is None:
        import os

        relative = Path(os.path.relpath(to_page, from_page.parent))
    return "/".join(quote(part) for part in relative.parts)


def title_of(source: Path) -> str:
    if source == ROOT / "術語表.md":
        return "術語表"
    if source == WIKI / "章節索引.md":
        return "章節索引"
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("《オトギフロンティア》", "")
    raise ValueError(f"Missing page title: {source}")


TITLES = {source: title_of(source) for source in PAGES}
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*\|?$", re.ASCII)


def render_plain(text: str) -> str:
    result = html.escape(text, quote=True)
    result = re.sub(r"`([^`]+)`", r"<code>\1</code>", result)
    result = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", result)
    result = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", result)
    result = re.sub(r"〔原文：(.+?)〕", r'<span class="source-note">〔原文：\1〕</span>', result)
    return result


def link_target(raw: str, source: Path, page: Path, base: Path) -> str:
    if raw.startswith(("https://", "http://", "mailto:", "#")):
        return raw
    parsed = urlsplit(raw)
    target = (source.parent / unquote(parsed.path)).resolve()
    if not target.is_file() or not target.is_relative_to(ROOT):
        raise ValueError(f"Missing or external local link in {source}: {raw}")
    if target.suffix == ".md":
        if target not in TITLES:
            raise ValueError(f"Markdown page not included in site: {target}")
        destination = output_path(target, base)
    elif target.suffix == ".txt":
        destination = base / "原文" / target.relative_to(ROOT)
    else:
        raise ValueError(f"Unexpected linked file in {source}: {raw}")
    url = relative_url(page, destination)
    if parsed.fragment:
        url += "#" + quote(unquote(parsed.fragment))
    return url


def render_inline(text: str, source: Path, page: Path, base: Path) -> str:
    pieces: list[str] = []
    cursor = 0
    for match in LINK_RE.finditer(text):
        pieces.append(render_plain(text[cursor : match.start()]))
        label = render_plain(match.group(1))
        href = html.escape(link_target(match.group(2), source, page, base), quote=True)
        pieces.append(f'<a href="{href}">{label}</a>')
        cursor = match.end()
    pieces.append(render_plain(text[cursor:]))
    return "".join(pieces)


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_markdown(source: Path, page: Path, base: Path) -> tuple[str, list[tuple[int, str, str]]]:
    lines = source.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    headings: list[tuple[int, str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            label = heading.group(2).strip()
            anchor = f"section-{len(headings) + 1}"
            headings.append((level, label, anchor))
            output.append(f'<h{level} id="{anchor}">{render_inline(label, source, page, base)}</h{level}>')
            index += 1
            continue
        if stripped.startswith("> "):
            block: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                block.append(lines[index].strip()[2:])
                index += 1
            output.append(f'<aside class="note">{render_inline(" ".join(block), source, page, base)}</aside>')
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and TABLE_SEPARATOR.match(lines[index + 1].strip()):
            header = table_cells(stripped)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(table_cells(lines[index]))
                index += 1
            th = "".join(f"<th>{render_inline(cell, source, page, base)}</th>" for cell in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{render_inline(cell, source, page, base)}</td>" for cell in row) + "</tr>"
                for row in rows
            )
            output.append(f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if bullet or numbered:
            tag = "ul" if bullet else "ol"
            items: list[str] = []
            pattern = r"^\s*[-*]\s+(.+)$" if bullet else r"^\s*\d+\.\s+(.+)$"
            while index < len(lines):
                item = re.match(pattern, lines[index])
                if not item:
                    break
                items.append(f"<li>{render_inline(item.group(1), source, page, base)}</li>")
                index += 1
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        paragraph = [stripped]
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if not next_line or re.match(r"^(#{1,6})\s+", next_line) or next_line.startswith(("> ", "|", "- ", "* ")):
                break
            paragraph.append(next_line)
            index += 1
        output.append(f"<p>{render_inline(' '.join(paragraph), source, page, base)}</p>")
    return "\n".join(output), headings


def nav_link(label: str, target: Path, page: Path, base: Path, current: bool = False) -> str:
    href = html.escape(relative_url(page, output_path(target, base)), quote=True)
    active = ' class="active" aria-current="page"' if current else ""
    return f'<a href="{href}"{active}>{display_title(label, "nav-original")}</a>'


def display_title(label: str, original_class: str) -> str:
    match = re.fullmatch(r"(.+?)(（[^（）]+）)", label)
    if not match:
        return html.escape(label)
    return (
        f'<span>{html.escape(match.group(1))}</span>'
        f'<small class="{original_class}">{html.escape(match.group(2))}</small>'
    )


def render_nav(source: Path, page: Path, base: Path) -> str:
    groups = [
        ("閱讀", [WIKI / "劇情總覽.md"]),
        ("主線劇情", [WIKI / "主線" / name for name in MAIN]),
        ("番外篇", [WIKI / "番外篇" / name for name in EXTRA]),
        ("資料頁", [WIKI / name for name in REFERENCE] + [ROOT / "術語表.md"]),
    ]
    parts = []
    for label, paths in groups:
        links = "".join(nav_link(TITLES[path], path, page, base, path == source) for path in paths)
        parts.append(f'<div class="nav-group"><p class="nav-heading">{label}</p>{links}</div>')
    return "".join(parts)


def sequence_links(source: Path, page: Path, base: Path) -> str:
    sequence = [WIKI / "主線" / name for name in MAIN] + [WIKI / "番外篇" / name for name in EXTRA]
    if source not in sequence:
        return ""
    position = sequence.index(source)
    parts = []
    if position > 0:
        target = sequence[position - 1]
        parts.append(f'<div><small>上一篇</small>{nav_link(TITLES[target], target, page, base)}</div>')
    if position + 1 < len(sequence):
        target = sequence[position + 1]
        parts.append(f'<div><small>下一篇</small>{nav_link(TITLES[target], target, page, base)}</div>')
    return '<nav class="sequence" aria-label="相鄰篇章">' + "".join(parts) + "</nav>"


def home_cards(page: Path, base: Path) -> str:
    cards = [
        ("01", "開始主線", "從第一部到第二部，依文本順序閱讀九篇劇情。", WIKI / "主線" / MAIN[0]),
        ("02", "閱讀番外", "六篇獨立故事，各篇保留原文出處。", WIKI / "番外篇" / EXTRA[0]),
        ("03", "查找資料", "人物、組織、世界設定與術語集中查閱。", WIKI / "主要角色.md"),
    ]
    items = []
    for number, title, description, target in cards:
        href = relative_url(page, output_path(target, base))
        items.append(f'<a class="feature-card" href="{html.escape(href, quote=True)}"><span class="feature-number">{number}</span><strong>{title}</strong><span>{description}</span><span class="feature-arrow">閱讀 →</span></a>')
    return '<div class="feature-grid">' + "".join(items) + "</div>"


def render_page(source: Path, base: Path) -> str:
    page = output_path(source, base)
    title = TITLES[source]
    body, headings = render_markdown(source, page, base)
    if headings and headings[0][0] == 1:
        body = body.replace(f'<h1 id="{headings[0][2]}">{render_inline(headings[0][1], source, page, base)}</h1>', "", 1)
    toc = "".join(
        f'<a class="toc-level-{level}" href="#{anchor}">{html.escape(label)}</a>'
        for level, label, anchor in headings
        if level in (2, 3)
    )
    # A page opened alone from a phone's file viewer cannot load sibling assets.
    # Keep the published pages readable and navigable as standalone HTML files.
    inline_css = (ASSETS / "style.css").read_text(encoding="utf-8").replace("</style", "<\\/style")
    inline_js = (ASSETS / "app.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    search_url = relative_url(page, base / "data" / "search.json")
    home = source == WIKI / "劇情總覽.md"
    breadcrumb = "總覽" if home else "主線" if source.parent.name == "主線" else "番外篇" if source.parent.name == "番外篇" else "資料頁"
    hero = (
        '<div class="hero-mark" aria-hidden="true">✦</div><p class="eyebrow">オトギフロンティア · STORY ARCHIVE</p>'
        '<h1>童話之國<small class="home-original">オトギノクニ</small><br><em>劇情資料庫</em></h1>'
        '<p class="hero-intro">從失樂園到跨世界的星戰，依篇章閱讀故事，循原文行號回查每個轉折。</p>'
        if home else f'<p class="eyebrow">{breadcrumb} · 完整劇透</p><h1>{display_title(title, "title-original")}</h1>'
    )
    cards = home_cards(page, base) if home else ""
    html_title = "童話之國（オトギノクニ）劇情資料庫" if home else f"{title}｜童話之國劇情資料庫"
    description = "繁體中文整理《オトギフロンティア》主線、番外、角色、設定與組織劇情，附原文行號。"
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="color-scheme" content="light">
  <title>{html.escape(html_title)}</title>
  <style>{inline_css}</style>
</head>
<body data-search-url="{html.escape(search_url, quote=True)}">
  <a class="skip-link" href="#main">跳到內容</a>
  <div class="site-shell">
    <header class="topbar">
      <button class="menu-button" type="button" aria-label="開啟導覽" aria-expanded="false" aria-controls="sidebar">☰</button>
      <a class="brand" href="{relative_url(page, base / 'index.html')}"><span class="brand-symbol">✦</span><span>童話之國 <small>オトギノクニ · 劇情資料庫</small></span></a>
      <div class="topbar-actions"><button class="search-open" type="button" aria-label="搜尋劇情與角色" aria-haspopup="dialog">⌕ <span>搜尋劇情與角色</span><kbd>/</kbd></button></div>
    </header>
    <button class="nav-scrim" type="button" aria-label="關閉導覽" hidden></button>
    <div class="layout">
      <aside class="sidebar" id="sidebar" aria-label="網站導覽"><div class="sidebar-inner">{render_nav(source, page, base)}</div></aside>
      <main class="main" id="main">
        <div class="article-width"><div class="breadcrumb">{breadcrumb} <span>／</span> {html.escape(title)}</div>
          <header class="page-hero {'home-hero' if home else ''}">{hero}</header>
          {cards}
          <article class="prose">{body}</article>
          {sequence_links(source, page, base)}
          <footer class="page-footer"><span>依現有文本整理 · 內容含完整劇透</span><a href="{relative_url(page, base / 'index.html')}">返回總覽 ↑</a></footer>
        </div>
      </main>
      <aside class="toc" aria-label="本頁目錄"><p>本頁目錄</p>{toc or '<span>請使用左側導覽閱讀其他頁面。</span>'}</aside>
    </div>
  </div>
  <div class="search-backdrop" hidden><div class="search-dialog" role="dialog" aria-modal="true" aria-label="搜尋網站"><div class="search-field"><span>⌕</span><input id="search-input" type="search" autocomplete="off" placeholder="搜尋人物、篇章或事件…" aria-label="搜尋人物、篇章或事件"><button class="search-close" type="button" aria-label="關閉搜尋">Esc</button></div><div class="search-results" role="status"><p class="search-hint">輸入關鍵字，搜尋所有 WIKI 頁面。</p></div></div></div>
  <script>{inline_js}</script>
</body>
</html>'''


def build(base: Path) -> None:
    for source in PAGES:
        if not source.is_file():
            raise FileNotFoundError(source)
        page = output_path(source, base)
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(render_page(source, base), encoding="utf-8")
    assets = base / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name in ("style.css", "app.js"):
        shutil.copy2(ASSETS / name, assets / name)
    search = []
    for source in PAGES:
        text = source.read_text(encoding="utf-8")
        category = "主線" if source.parent.name == "主線" else "番外" if source.parent.name == "番外篇" else "資料"
        readable = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        search.append({
            "title": TITLES[source],
            "category": category,
            "url": relative_url(base / "index.html", output_path(source, base)),
            "headings": [line.lstrip("# ").strip() for line in text.splitlines() if re.match(r"^#{2,4}\s", line)],
            "text": re.sub(r"[#*`|\[\]()]", " ", readable),
        })
    data = base / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for source in SOURCES:
        target = base / "原文" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (base / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    if OUTPUT.resolve() != (ROOT / "docs").resolve() or not OUTPUT.resolve().is_relative_to(ROOT):
        raise RuntimeError("Unsafe output path")
    with tempfile.TemporaryDirectory(prefix=".site-build-", dir=ROOT) as temp:
        staged = Path(temp) / "docs"
        staged.mkdir()
        build(staged)
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        shutil.move(str(staged), str(OUTPUT))
    print(f"Built {len(PAGES)} pages and {len(SOURCES)} source texts in {OUTPUT}")


if __name__ == "__main__":
    main()
