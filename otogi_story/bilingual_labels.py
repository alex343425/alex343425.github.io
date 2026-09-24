"""Add verified Japanese originals to Wiki headings and named entry labels.

This is idempotent: existing full-width Japanese annotations are left alone.
It changes editorial labels, not narrative prose or source citations.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "wiki"
GLOSSARY = ROOT / "術語表.md"


def glossary_pairs() -> tuple[dict[str, str], list[tuple[str, str]]]:
    terms: dict[str, str] = {}
    chapters: list[tuple[str, str]] = []
    in_chapters = False
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        if line == "## 篇章名稱":
            in_chapters = True
            continue
        if line.startswith("## "):
            in_chapters = False
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip("| ").split("|")]
        if len(cells) < 2 or cells[0].startswith(("---", "原文", "日文")):
            continue
        ja, zh = cells[:2]
        if in_chapters:
            chapters.append((ja, zh))
        elif ja != zh and len(zh) >= 2 and "（" not in zh:
            # First attested spelling wins, including user-specified translations.
            terms.setdefault(zh, ja)
    terms.update({
        "格林家": "グリム家",  # 第二部 3 柱石を照らす曙光編.txt:1520
        "阿迪斯": "アディス",  # 第二部 3 柱石を照らす曙光編.txt:1138
        "毗濕奴": "ヴィジュー",  # Prefer the full speaker name to its variant.
        "阿爾卡娜": "アルカーナ",  # 番外篇/白璧微瑕のアルカーナ.txt
        "大變革": "グランド・リヴィジョン",
        "黃昏少女": "黄昏の少女",
        "探求童話少女": "探求の御伽乙女",
        "交錯天地": "交錯する天地",
        "照亮柱石的曙光": "柱石を照らす曙光",
        "融於暗影的華夏": "暗影に溶ける華夏",
        "綻放於童話的蓮花暗焉": "御伽に咲く蓮花の闇焉",
        "星謐之獅": "星謐の獅子",
        "灼燒天譜的星戰": "天譜を焦がす星戦",
    })
    return terms, chapters


TERMS, CHAPTERS = glossary_pairs()
PATTERN = re.compile("|".join(re.escape(term) for term in sorted(TERMS, key=len, reverse=True)))
CHAPTER_BY_ZH = {zh: ja.split("/", 1)[-1] for ja, zh in CHAPTERS}
CHAPTER_BY_JA = {ja.split("/", 1)[-1]: zh.split("／", 1)[-1] for ja, zh in CHAPTERS}


ANNOTATION_OR_TERM = re.compile(r"（[^（）]*）|" + PATTERN.pattern)


def annotate(text: str) -> str:
    # Preserve existing Japanese annotations and their Chinese base terms.
    def replace(match: re.Match[str]) -> str:
        term = match.group()
        if term.startswith("（"):
            return term
        annotation = f"（{TERMS[term]}）"
        return term if text.startswith("（", match.end()) else term + annotation

    return ANNOTATION_OR_TERM.sub(replace, text)


def update_line(path: Path, line: str) -> str:
    heading = re.match(r"^(#{1,6} )(.*?)(\r?\n)?$", line)
    if heading:
        prefix, label, newline = heading.groups()
        if path == WIKI / "章節索引.md" and prefix == "## ":
            zh = CHAPTER_BY_JA.get(label)
            if zh and zh != label:
                label = f"{zh}（{label}）"
        elif prefix == "# " and path.parent.name in {"主線", "番外篇"}:
            original = CHAPTER_BY_ZH.get(label.replace("：", " ").replace("番外篇 ", "番外篇／"))
            if original and original not in label:
                label = f"{label}（{original}）"
        else:
            label = annotate(label)
        return prefix + label + (newline or "")

    # Character dossiers and named item descriptions use bold lead labels.
    lead = re.match(r"^(- \*\*)([^*]+?)(：\*\*.*?)(\r?\n)?$", line)
    if lead:
        return lead.group(1) + annotate(lead.group(2)) + lead.group(3) + (lead.group(4) or "")

    if path == WIKI / "劇情總覽.md" and line.startswith("|"):
        # Only the page title link in each overview row is a named item.
        for zh, ja in CHAPTER_BY_ZH.items():
            short = zh.split(" ")[-1].replace("番外篇／", "").removesuffix("篇")
            line = re.sub(
                rf"\[([^\]]*{re.escape(short.removesuffix('篇'))}[^\]]*)\](\([^)]*\.md\))",
                lambda match: f"[{match.group(1)}（{ja}）]{match.group(2)}" if ja not in match.group(1) else match.group(),
                line,
            )
        return line

    if path in {WIKI / "次要角色.md", WIKI / "組織與勢力.md"} and line.startswith("|"):
        cells = line.split("|")
        if len(cells) >= 4 and cells[1].strip() not in {"類別", "文本／群體", "篇章／群體", "關係", "---"}:
            cells[1] = " " + annotate(cells[1].strip()) + " "
            return "|".join(cells)
    return line


def main() -> None:
    preview = "--preview" in sys.argv
    changed_files = 0
    changed_lines = 0
    for path in sorted(WIKI.rglob("*.md")):
        before = path.read_bytes().decode("utf-8")
        lines = before.splitlines(keepends=True)
        after_lines = []
        for line in lines:
            line = re.sub(r"（([^（）]+)）(?:（\1）)+", r"（\1）", line)
            line = line.replace("毗濕奴（ヴィジュ―）", "毗濕奴（ヴィジュー）")
            line = line.replace("阿爾卡娜（カナ）", "阿爾卡娜（アルカーナ）")
            after_lines.append(update_line(path, line))
        after = "".join(after_lines)
        if after != before:
            changed_files += 1
            changed_lines += sum(a != b for a, b in zip(lines, after_lines))
            if preview:
                for old, new in zip(lines, after_lines):
                    if old != new:
                        print(f"{path.relative_to(ROOT)}: {old.strip()} -> {new.strip()}")
            else:
                path.write_bytes(after.encode("utf-8"))
    print(f"Annotated {changed_lines} labels in {changed_files} files")


if __name__ == "__main__":
    main()
