"""Build a terminology index from the supplied Otogi Frontier story texts."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re


ROOT = Path(__file__).parent
DICTIONARY = json.loads((ROOT / "童前字典.json").read_text(encoding="utf-8"))
USER_OVERRIDES = {"トレローニー": "託雷羅尼"}
FILES = sorted(ROOT.rglob("*.txt"), key=lambda p: ("番外篇" in p.parts, p.name))
LINES = {path: path.read_text(encoding="utf-8").splitlines() for path in FILES}
SPEAKERS = Counter()
SPEAKER_SOURCE: dict[str, tuple[Path, int]] = {}
for path, lines in LINES.items():
    for line_no, line in enumerate(lines, 1):
        match = re.match(r"^([^：\n]{1,40})：", line)
        if match:
            name = match.group(1)
            SPEAKERS[name] += 1
            SPEAKER_SOURCE.setdefault(name, (path, line_no))

# Short terms can occur inside sound effects or longer names. Point to a clear use.
SOURCE_OVERRIDES = {
    "ガア": (ROOT / "第二部 6 天譜を焦がす星戦編.txt", 3084),
    "カナ": (ROOT / "番外篇/禁忌精霊伝承―ルインズナイト―.txt", 389),
}


def source_for(term: str, speaker_only: bool = False) -> str:
    if term in SOURCE_OVERRIDES:
        path, line_no = SOURCE_OVERRIDES[term]
        if term not in LINES[path][line_no - 1]:
            raise ValueError(f"Source override is stale: {term}")
        return f"{path.relative_to(ROOT).as_posix()}:{line_no}"
    if speaker_only and term in SPEAKER_SOURCE:
        path, line_no = SPEAKER_SOURCE[term]
        return f"{path.relative_to(ROOT).as_posix()}:{line_no}"
    for path, lines in LINES.items():
        for line_no, line in enumerate(lines, 1):
            if term in line:
                return f"{path.relative_to(ROOT).as_posix()}:{line_no}"
    raise ValueError(f"Term missing from corpus: {term}")


def translation(term: str, fallback: str = "") -> tuple[str, str]:
    if term in USER_OVERRIDES:
        return USER_OVERRIDES[term], "使用者指定"
    if term in DICTIONARY:
        return DICTIONARY[term], "字典"
    if not fallback:
        raise ValueError(f"No translation: {term}")
    return fallback, "暫譯"


# Category, Japanese term, fallback translation, concise identification note.
# A dictionary entry always overrides a fallback translation.
CORE = [
    ("世界與地點", "オトギノクニ", "", "故事世界"),
    ("世界與地點", "人間界", "人間界", "人類所在的世界"),
    ("世界與地點", "μ世界", "μ世界", "世界名稱；保留希臘字母 μ"),
    ("世界與地點", "ネバーランド", "", "地名"),
    ("世界與地點", "ワンダーランド", "", "地名"),
    ("世界與地點", "雪の国", "雪之國", "地名"),
    ("世界與地點", "アディス", "", "冥界地名"),
    ("世界與地點", "バビロン", "", "地名"),
    ("世界與地點", "ポルタ島", "波爾塔島", "地名"),
    ("世界與地點", "ハブタウン", "", "地名"),
    ("世界與地點", "ニヴルヘイム", "", "地名"),
    ("世界與地點", "ヘルヘイム", "", "地名"),
    ("世界與地點", "アースガルズ", "", "地名"),
    ("世界與地點", "ムスペルヘイム", "", "地名"),
    ("世界與地點", "十二迷宮", "十二迷宮", "地點"),
    ("世界與地點", "マオリン", "茂林", "五獸共同生活過的地方；暫譯"),
    ("世界與地點", "天空神殿", "天空神殿", "地點"),
    ("世界與地點", "ロゼッタ・ゲート", "", "設施名稱"),
    ("世界與地點", "フローレ・アカデミー", "", "學院名稱"),
    ("世界與地點", "ユグドラシル", "", "世界樹"),
    ("世界與地點", "忘却の丘", "忘卻之丘", "盧恩茲奈特事件開頭的地點"),
    ("世界與地點", "エイヴォン研究所", "艾文研究所", "杜布利追查時前往的研究所；暫譯"),
    ("組織與群體", "コミッティ", "", "組織名稱"),
    ("組織與群體", "インペリウム・コミッティ", "", "組織名稱"),
    ("組織與群體", "グリム家", "格林家", "家族與契約網"),
    ("組織與群體", "特務機関", "特務機關", "組織名稱"),
    ("組織與群體", "十二神官", "十二神官", "群體稱號"),
    ("組織與群體", "五獣", "五獸", "白虎、青龍、玄武、朱雀、黃龍的合稱"),
    ("組織與群體", "八武神", "八武神", "遠古封印星之魔獸的八名戰士；文本亦稱八武衆"),
    ("組織與群體", "星の革命軍", "星之革命軍", "組織名稱"),
    ("組織與群體", "星の革命戦線", "星之革命戰線", "組織名稱；與革命軍分列"),
    ("組織與群體", "白の夜明け団", "", "組織名稱"),
    ("組織與群體", "ナインスアルバ", "", "組織／篇章名稱"),
    ("組織與群體", "信民", "信民", "群體稱呼"),
    ("組織與群體", "コートクラーク", "", "職稱／群體稱呼"),
    ("組織與群體", "ルインズナイト", "", "六名獲得較大行動自由的武器精靈組織"),
    ("力量與機制", "エルマイト", "", "正面想像力所形成的能量"),
    ("力量與機制", "ディマイト", "", "負面想像力所形成的能量"),
    ("力量與機制", "イマジュマイト", "", "人間界供應的想像力能量"),
    ("力量與機制", "グランド・リヴィジョン", "", "能量管理與分配機制；字典譯名含書名號"),
    ("力量與機制", "GR2", "GR2", "第二次大變革計畫的簡稱"),
    ("力量與機制", "作品理解", "作品理解", "改寫人物設定時涉及的概念"),
    ("力量與機制", "リメイク", "", "改寫作品的手段"),
    ("力量與機制", "創造期", "創造期", "時期名稱"),
    ("力量與機制", "第二の理想郷", "第二理想鄉", "篇末提及的計畫；暫譯"),
    ("力量與機制", "消えゆく物語", "逐漸消逝的故事", "現象名稱"),
    ("力量與機制", "失われゆく物語", "逐漸失落的故事", "原文不同，暫不合併"),
    ("力量與機制", "逆位置の魔法", "逆位魔法", "魔法名稱"),
    ("力量與機制", "エルマイト・トレード", "聖之力交易", "術語；沿用字典對エルマイト的譯名"),
    ("力量與機制", "ヴェルト・レダクツィオン", "", "術式名稱"),
    ("力量與機制", "正しさの杖", "正確之杖", "改寫對正確的認知；作用範圍仍待核對"),
    ("力量與機制", "獣聖騎兵", "獸聖騎兵", "古代兵器的稱呼"),
    ("力量與機制", "イマジュマイト・アディション", "想像之力增幅", "兩種力量共鳴而產生的變化；暫譯"),
    ("力量與機制", "ファンタズマ・イン・ザ・ミラー", "鏡中幻想", "卡蘿爾的幻術名稱；暫譯"),
    ("力量與機制", "ルンペル", "", "KHM55 機體的簡稱"),
    ("力量與機制", "ラグナロク", "", "事件／概念名稱"),
    ("力量與機制", "深淵の闇", "深淵之闇", "概念名稱"),
    ("力量與機制", "深淵の闇計画", "深淵之闇計畫", "計畫名稱"),
    ("力量與機制", "星の魔獣", "星之魔獸", "生物類別"),
    ("力量與機制", "ゴエティア", "蓋提亞", "專有名稱；待後續語境核定類別"),
    ("力量與機制", "セレスティアル", "賽勒斯提亞爾", "專有名稱；待後續語境核定類別"),
    ("力量與機制", "アルカナム", "阿爾卡納姆", "專有名稱；待後續語境核定類別"),
    ("力量與機制", "武器精霊", "武器精靈", "武器本體產生的精靈"),
    ("力量與機制", "再刃", "再刃", "卡娜重新鍛造六人武器本體的工序"),
    ("人物名稱", "カナ", "卡娜", "鍛冶師；字典未收錄"),
    ("稱謂與別名", "人間さん", "", "對主角的稱呼"),
    ("稱謂與別名", "創造の聖母", "", "稱號；字典譯作「創造的聖母」"),
    ("稱謂與別名", "ティンカ", "", "ティンカー・ベル的簡稱"),
    ("稱謂與別名", "デュプリ", "", "デュプリ・ライブラ的簡稱"),
    ("稱謂與別名", "ヴィジュ―", "", "ヴィジュー的原文異體，末尾為長音符"),
    ("稱謂與別名", "ジューチャオ", "", "中文名「朱雀」的片假名讀法"),
    ("稱謂與別名", "パイフー", "", "中文名「白虎」的片假名讀法"),
    ("稱謂與別名", "チンロン", "", "中文名「青龍」的片假名讀法"),
    ("稱謂與別名", "ファンロン", "", "中文名「黃龍」的片假名讀法"),
    ("稱謂與別名", "シェンウー", "", "中文名「玄武」的片假名讀法"),
]

ARC_TITLES = [
    ("第一部 星々の失楽園編", "第一部 群星的失樂園篇"),
    ("第二部 1 黄昏の少女編", "第二部 1 黃昏少女篇"),
    ("第二部 1.5 探求の御伽乙女編", "第二部 1.5 探求童話少女篇"),
    ("第二部 2 交錯する天地編", "第二部 2 交錯天地篇"),
    ("第二部 3 柱石を照らす曙光編", "第二部 3 照亮柱石的曙光篇"),
    ("第二部 4 暗影に溶ける華夏編", "第二部 4 融於暗影的華夏篇"),
    ("第二部 5 御伽に咲く蓮花の闇焉編", "第二部 5 綻放於童話的蓮花暗焉篇"),
    ("第二部 5.5 星謐の獅子編", "第二部 5.5 星謐之獅篇"),
    ("第二部 6 天譜を焦がす星戦編", "第二部 6 灼燒天譜的星戰篇"),
    ("番外篇/魔宮流星譚", "番外篇／魔宮流星譚"),
    ("番外篇/禁忌精霊伝承―ルインズナイト―", "番外篇／禁忌精靈傳承—盧恩茲奈特—"),
    ("番外篇/白璧微瑕のアルカーナ", "番外篇／白璧微瑕的阿爾卡娜"),
    ("番外篇/十二迷宮", "番外篇／十二迷宮"),
    ("番外篇/ナインスアルバ", "番外篇／第九黎明"),
    ("番外篇/コミッティ創設秘話", "番外篇／評議會創設秘話"),
]

MENTIONED_NAMES = [
    "ビブリオ", "ポチ", "オルディン", "ヴェルザーム", "グリム",
    "ギャベル", "キャンディス", "リーシス", "アリシア", "カプレーゼ",
    "ラームス", "サーベイ", "ヨル", "スフィア", "ディ・マキナ",
    "ジャヴェール", "ティターニア", "ライメント", "ウィンキー",
    "エリーネア", "フォルクス・ゲヘナ", "ガア",
]

ADDITIONAL_PEOPLE = [
    ("雨依", "雨依", "漢字原名；字典未收錄"),
    ("服部あおい", "服部葵", "使用者指定"),
    ("三蔵法師", "三藏法師", "漢字繁化"),
    ("変帝", "變帝", "漢字繁化"),
    ("珠絵", "珠繪", "漢字繁化"),
    ("諸葛亮", "諸葛亮", "漢字原名"),
    ("朱雀", "朱雀", "與ジューチャオ同名"),
    ("白虎", "白虎", "與パイフー同名"),
    ("青龍", "青龍", "與チンロン同名"),
    ("玄武", "玄武", "與シェンウー同名"),
    ("猪八戒", "豬八戒", "漢字繁化"),
    ("怪人二十面相", "怪人二十面相", "漢字原名"),
    ("ジャヴェール警部", "賈維爾警部", "依字典「ジャヴェール→賈維爾」延伸"),
    ("浦島みずえ", "浦島水繪", "使用者指定"),
    ("紫式部", "紫式部", "漢字原名"),
    ("黄帝", "黃帝", "漢字繁化"),
    ("神農", "神農", "漢字原名"),
    ("乙姫", "乙姬", "漢字繁化"),
    ("金角", "金角", "漢字原名"),
    ("信長", "信長", "漢字原名"),
    ("光秀", "光秀", "漢字原名"),
]

EXCLUDE_SPEAKERS = {
    "人間さん", "創造の聖母", "ティンカ", "デュプリ", "ヴィジュ―",
    "ジューチャオ", "パイフー", "チンロン", "ファンロン", "シェンウー",
    "コートクラーク", "エインヘリヤル", "マスター", "スタッフ",
    "ナイトゴーント", "ショゴス",
}


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


out = [
    "# オトギフロンティア劇情術語表（繁體中文）",
    "",
    "本表只統一術語與人名，不整理故事事件。依據為本資料夾的 15 份日文劇情文本；有相符鍵值時優先採用《童前字典.json》，使用者指定的修正優先於字典。",
    "「字典」表示逐字沿用字典值；「暫譯」表示字典未收錄，目前供 WIKI 草稿使用。出處以檔名和原文行號標示。",
    "日文相近但可能不同的人物或概念，先分列，不擅自合併。人物索引取自文本中的說話者標籤；配角與稱號不代表人物關係已核實。",
    "",
]

out.extend([
    "## 篇章名稱",
    "",
    "篇章譯名為工作用暫譯；詞組中已有字典對照者沿用該用語。",
    "",
    "| 原文檔名（不含副檔名） | 繁體中文篇章名 |",
    "| --- | --- |",
])
for stem, value in ARC_TITLES:
    if not (ROOT / f"{stem}.txt").exists():
        raise ValueError(f"Story file missing: {stem}")
    out.append(f"| {md(stem)} | {md(value)} |")
out.append("")

for category in dict.fromkeys(row[0] for row in CORE):
    out.extend([
        f"## {category}",
        "",
        "| 日文原詞 | 繁體中文統一譯名 | 依據 | 備註 | 原文出處 |",
        "| --- | --- | --- | --- | --- |",
    ])
    for group, term, fallback, note in CORE:
        if group != category:
            continue
        value, basis = translation(term, fallback)
        out.append(f"| {md(term)} | {md(value)} | {basis} | {md(note)} | {md(source_for(term, category == '稱謂與別名'))} |")
    out.append("")

out.extend([
    "## 字典已對照的其他專名",
    "",
    "這些名稱見於正文，但沒有以完全相同字串作為說話者標籤；人物身分或與其他名稱的關係尚未在本步判定。",
    "",
    "| 日文原詞 | 繁體中文統一譯名 | 原文出處 |",
    "| --- | --- | --- |",
])
for name in MENTIONED_NAMES:
    if name not in DICTIONARY:
        raise ValueError(f"Name missing from dictionary: {name}")
    if name in SPEAKERS:
        raise ValueError(f"Name has speaker label: {name}")
    out.append(f"| {md(name)} | {md(DICTIONARY[name])} | {md(source_for(name))} |")
out.append("")

character_rows = [
    (name, translation(name)[0], count)
    for name, count in SPEAKERS.items()
    if name in DICTIONARY and name not in EXCLUDE_SPEAKERS
]
character_rows.sort(key=lambda row: (-row[2], row[0]))
out.extend([
    f"## 字典對照與使用者修訂的人物索引（{len(character_rows)} 筆）",
    "",
    "下表收錄有說話者標籤、且字典提供完全相同原文鍵值的人名。トレローニー依使用者指定譯作「託雷羅尼」。出場台詞數僅供查找使用，不能用來判斷角色重要性。",
    "",
    "| 日文原名 | 繁體中文統一譯名 | 台詞數 | 首次說話出處 |",
    "| --- | --- | ---: | --- |",
])
for name, value, count in character_rows:
    out.append(f"| {md(name)} | {md(value)} | {count} | {md(source_for(name, True))} |")

out.extend([
    "",
    "## 字典未收錄、需保留的具名說話者",
    "",
    "以下只列可從字面確定或能保守處理的名稱。保留假名的項目仍待後續查證正式譯名。一般群眾、衛兵、編號角色等泛稱不列入。",
    "",
    "| 日文原名 | 建議顯示名 | 備註 | 台詞數 | 首次說話出處 |",
    "| --- | --- | --- | ---: | --- |",
])
for name, value, note in ADDITIONAL_PEOPLE:
    if name not in SPEAKERS:
        raise ValueError(f"Additional speaker missing: {name}")
    out.append(f"| {md(name)} | {md(value)} | {md(note)} | {SPEAKERS[name]} | {md(source_for(name, True))} |")

out.extend([
    "",
    "## 待核對的字典條目",
    "",
    "| 日文原詞 | 字典原值 | 核對原因 |",
    "| --- | --- | --- |",
    f"| グランド・リヴィジョン | {md(DICTIONARY['グランド・リヴィジョン'])} | 字典值帶『』；用作一般敘述時，排版可另行決定。 |",
    "| ジャッジメント／リーブラ／ライブラ | 天秤座／利布拉／萊布拉 | 原文及字典分列；不可只因名稱相近就合併角色。 |",
    "| 消えゆく物語／失われゆく物語 | 逐漸消逝的故事／逐漸失落的故事 | 兩種原文是否指同一現象，需在整理劇情時再核對。 |",
    "",
])

target = ROOT / "術語表.md"
target.write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {target.name}: {len(CORE)} core terms, {len(character_rows)} dictionary speakers, {len(ADDITIONAL_PEOPLE)} additional speakers")
