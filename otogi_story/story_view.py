"""Read-only scene browser for the supplied Otogi Frontier story files.

Usage: python story_view.py <source filename> [first scene] [last scene] [headings|cards|full]
Scene numbers are one-based positions in a file, not story IDs.
"""

from pathlib import Path
import re
import sys


def scenes(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = []
    for line_no, line in enumerate(lines, 1):
        match = re.match(r"^(\d+)\s*-\s*(.+)$", line)
        if match:
            heads.append((line_no, match.group(1), match.group(2)))
    for index, (line_no, story_id, title) in enumerate(heads, 1):
        stop = heads[index][0] - 1 if index < len(heads) else len(lines)
        body = [x.strip() for x in lines[line_no:stop] if x.strip()]
        yield index, line_no, stop, story_id, title, body


if __name__ == "__main__":
    path = Path(sys.argv[1])
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    last = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    mode = sys.argv[4] if len(sys.argv) > 4 else "cards"
    for index, start, stop, story_id, title, body in scenes(path):
        if index < first or index > last:
            continue
        print(f"[{index}] {story_id} {title} ({start}-{stop})")
        if mode == "headings":
            continue
        if mode == "full":
            for line in body:
                print("  " + line)
        else:
            excerpts = body if len(body) <= 6 else body[:3] + ["…"] + body[-3:]
            for line in excerpts:
                print("  " + line)
