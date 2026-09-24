"""Check story wiki links and source citation coordinates."""

from pathlib import Path
from urllib.parse import unquote
import re

from story_view import scenes


ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "wiki"
PAGES = sorted(WIKI.glob("主線/*.md")) + sorted(WIKI.glob("番外篇/*.md"))
issues = []
citations = 0

for page in sorted(WIKI.rglob("*.md")):
    text = page.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", text):
        if target.startswith(("https:", "http:", "#")):
            continue
        resolved = (page.parent / unquote(target)).resolve()
        if not resolved.is_file():
            issues.append(f"{page}: broken link {target}")

for page in PAGES:
    text = page.read_text(encoding="utf-8")
    match = re.search(r"原文：\[[^]]+\]\(([^)]+\.txt)\)", text)
    if not match:
        issues.append(f"{page}: missing source link")
        continue
    source = (page.parent / unquote(match.group(1))).resolve()
    chapter_list = list(scenes(source))
    source_lines = source.read_text(encoding="utf-8").splitlines()
    for citation in re.findall(r"〔原文：([^〕]+)〕", text):
        for start_id, end_id, start, end in re.findall(
            r"(\d+)(?:–(\d+))?，(\d+)–(\d+)行", citation
        ):
            citations += 1
            start, end = int(start), int(end)
            if not 1 <= start <= end <= len(source_lines):
                issues.append(f"{page}: invalid lines {start}–{end}")
                continue
            first = next((item for item in chapter_list if item[1] <= start <= item[2]), None)
            last = next((item for item in chapter_list if item[1] <= end <= item[2]), None)
            if first and first[3] != start_id:
                issues.append(
                    f"{page}: start ID {start_id} differs from {first[3]} at line {start}"
                )
            if last and last[3] != (end_id or start_id):
                issues.append(
                    f"{page}: end ID {end_id or start_id} differs from {last[3]} at line {end}"
                )

for page in (WIKI / "主要角色.md", WIKI / "次要角色.md", WIKI / "次要角色詳述.md", WIKI / "世界設定.md", WIKI / "組織與勢力.md"):
    if not page.exists():
        continue
    page_text = page.read_text(encoding="utf-8")
    for filename, first_id, last_id, start, end in re.findall(
        r"([^：；]+?\.txt)：章(\d+)(?:–(\d+))?，(\d+)–(\d+)行", page_text
    ):
        filename = filename.removeprefix("原文：")
        source = ROOT / filename
        if not source.exists():
            issues.append(f"{page}: missing source {filename}")
            continue
        chapter_list = list(scenes(source))
        start, end = int(start), int(end)
        citations += 1
        first = next((x for x in chapter_list if x[1] <= start <= x[2]), None)
        last = next((x for x in chapter_list if x[1] <= end <= x[2]), None)
        if first is None or last is None:
            issues.append(f"{page}: invalid lines {start}–{end}")
        else:
            if first[3] != first_id:
                issues.append(f"{page}: start ID {first_id} differs from {first[3]} at line {start}")
            if last[3] != (last_id or first_id):
                issues.append(f"{page}: end ID {last_id or first_id} differs from {last[3]} at line {end}")

print(f"{len(PAGES)} story pages, {citations} source coordinates, {len(issues)} issues")
for issue in issues:
    print(issue)
if issues:
    raise SystemExit(1)
