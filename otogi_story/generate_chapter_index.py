"""Generate a source-line chapter index for the Otogi story wiki."""

from pathlib import Path
from urllib.parse import quote

from bilingual_labels import CHAPTER_BY_JA
from story_view import scenes


ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "wiki"
SOURCES = [
    "第一部 星々の失楽園編.txt",
    "第二部 1 黄昏の少女編.txt",
    "第二部 1.5 探求の御伽乙女編.txt",
    "第二部 2 交錯する天地編.txt",
    "第二部 3 柱石を照らす曙光編.txt",
    "第二部 4 暗影に溶ける華夏編.txt",
    "第二部 5 御伽に咲く蓮花の闇焉編.txt",
    "第二部 5.5 星謐の獅子編.txt",
    "第二部 6 天譜を焦がす星戦編.txt",
    "番外篇/十二迷宮.txt",
    "番外篇/コミッティ創設秘話.txt",
    "番外篇/禁忌精霊伝承―ルインズナイト―.txt",
    "番外篇/白璧微瑕のアルカーナ.txt",
    "番外篇/ナインスアルバ.txt",
    "番外篇/魔宮流星譚.txt",
]


def main():
    output = [
        "# 劇情文本章節索引",
        "",
        "以下依原始檔案順序列出章節編號、原文標題及起迄行號。行號從檔案第一行起算，含空白行；同檔內的章節編號可能重複，查找時請合用檔名與行號。此表只供回查原文，不代表番外篇的故事時間順序。",
        "",
        "[返回劇情總覽](劇情總覽.md)",
        "",
    ]
    for name in SOURCES:
        path = ROOT / name
        chapters = list(scenes(path))
        link = "../" + quote(name.replace("\\", "/"), safe="/.-_")
        japanese = path.stem
        chinese = CHAPTER_BY_JA.get(japanese)
        heading = f"{chinese}（{japanese}）" if chinese and chinese != japanese else japanese
        output += [
            f"## {heading}",
            "",
            f"原文：[來源檔案]({link})；共 {len(chapters)} 個章節標題。",
            "",
            "| 檔內順序 | 章節編號 | 原文標題 | 起迄行號 |",
            "|---:|---:|---|---:|",
        ]
        for position, start, end, chapter_id, title, _ in chapters:
            title = title.replace("|", "\\|").replace("`", "\\`")
            output.append(f"| {position} | {chapter_id} | {title} | {start}–{end} |")
        output.append("")
    output += [
        "## 文本更新",
        "",
        "更新後的 `番外篇/禁忌精霊伝承―ルインズナイト―.txt` 有獨立內容，已單獨列章。`番外篇/ナインスアルバ.txt` 已刪除 `630201–630215` 的重複段落；本索引依現有檔案位置列出一次。",
        "",
    ]
    (WIKI / "章節索引.md").write_text("\n".join(output), encoding="utf-8")
    print(f"Wrote {sum(len(list(scenes(ROOT / name))) for name in SOURCES)} chapter entries")


if __name__ == "__main__":
    main()
