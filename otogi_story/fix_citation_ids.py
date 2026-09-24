"""Align wiki citation chapter IDs to the already recorded source lines."""

from pathlib import Path
from urllib.parse import unquote
import re

from story_view import scenes


WIKI = Path(__file__).resolve().parent / "wiki"
pages = sorted(WIKI.glob("主線/*.md")) + sorted(WIKI.glob("番外篇/*.md"))
changed = 0
for page in pages:
    text = page.read_text(encoding="utf-8")
    source_link = re.search(r"原文：\[[^]]+\]\(([^)]+\.txt)\)", text)
    source = (page.parent / unquote(source_link.group(1))).resolve()
    chapter_list = list(scenes(source))

    def fix_coordinate(match):
        global changed
        first_line, last_line = int(match.group(3)), int(match.group(4))
        first = next(x for x in chapter_list if x[1] <= first_line <= x[2])[3]
        last = next(x for x in chapter_list if x[1] <= last_line <= x[2])[3]
        corrected = f"{first}{'–' + last if first != last else ''}，{first_line}–{last_line}行"
        if corrected != match.group(0):
            changed += 1
        return corrected

    def fix_citation(match):
        return "〔原文：" + re.sub(
            r"(\d+)(?:–(\d+))?，(\d+)–(\d+)行", fix_coordinate, match.group(1)
        ) + "〕"

    fixed = re.sub(r"〔原文：([^〕]+)〕", fix_citation, text)
    if fixed != text:
        page.write_text(fixed, encoding="utf-8")

print(f"Corrected {changed} citation coordinates")
