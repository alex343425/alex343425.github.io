"""Check the generated Pages artifact and its local links."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_site import OUTPUT, PAGES, SOURCES, output_path


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"] or "")
        for attribute in ("href", "src"):
            if data.get(attribute):
                self.urls.append((attribute, data[attribute] or ""))


def main() -> None:
    failures: list[str] = []
    html_files = sorted(OUTPUT.rglob("*.html"))
    if len(html_files) != len(PAGES):
        failures.append(f"Expected {len(PAGES)} HTML pages, found {len(html_files)}")
    for source in PAGES:
        if not output_path(source, OUTPUT).is_file():
            failures.append(f"Missing page: {source}")
    for source in SOURCES:
        if not (OUTPUT / "原文" / source.relative_to(OUTPUT.parent)).is_file():
            failures.append(f"Missing source text: {source}")
    for asset in ("assets/style.css", "assets/app.js", "data/search.json", ".nojekyll"):
        if not (OUTPUT / asset).is_file():
            failures.append(f"Missing site asset: {asset}")

    checked = 0
    for page in html_files:
        page_html = page.read_text(encoding="utf-8")
        if '<meta name="viewport" content="width=device-width, initial-scale=1">' not in page_html:
            failures.append(f"Missing mobile viewport: {page.relative_to(OUTPUT)}")
        if "<style>" not in page_html or "@media (max-width: 760px)" not in page_html:
            failures.append(f"Missing standalone mobile styles: {page.relative_to(OUTPUT)}")
        if "<script>" not in page_html or "function setMenu(open)" not in page_html:
            failures.append(f"Missing standalone navigation script: {page.relative_to(OUTPUT)}")
        parser = References()
        parser.feed(page_html)
        for _, raw_url in parser.urls:
            parsed = urlsplit(raw_url)
            if parsed.scheme or raw_url.startswith("//"):
                continue
            destination = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
            if not destination.is_relative_to(OUTPUT.resolve()) or not destination.is_file():
                failures.append(f"Broken local link: {page.relative_to(OUTPUT)} → {raw_url}")
            elif parsed.fragment and destination.suffix == ".html":
                if destination == page and unquote(parsed.fragment) not in parser.ids:
                    failures.append(f"Missing anchor: {page.relative_to(OUTPUT)} → {raw_url}")
            checked += 1

    search = json.loads((OUTPUT / "data/search.json").read_text(encoding="utf-8"))
    if len(search) != len(PAGES):
        failures.append(f"Expected {len(PAGES)} search entries, found {len(search)}")
    for entry in search:
        if not (OUTPUT / unquote(entry["url"])).is_file():
            failures.append(f"Broken search result: {entry['title']}")
        if not entry.get("text"):
            failures.append(f"Empty search text: {entry['title']}")

    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"{len(html_files)} pages, {len(SOURCES)} source texts, {checked} local references, 0 issues")


if __name__ == "__main__":
    main()
