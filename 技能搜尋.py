import string
import requests
import json
import time
import sys
import pyperclip
import re
from idparse import check_sc, check_sa, isinforward, isinor, isinbackward, isindamage, isininterval, isinand, setskilltype, skillclass, weaponclass, skillrank, attribute
import skill_change
import copy
from cfg_skill import set_wiki_name
import os,sys
from PIL import Image
from io import BytesIO


l_search=['サマの緋玉', 'ノームの地玉', 'ウンディーネの水玉', 'サラマンダーの焔玉', 'シルフィードの風玉', 'ペガサスの駿玉', 'ケルピーの潮玉', 'バイコーンの愛玉', 'ユニコーンの純玉', 'オーフェンの堪玉', 'BBの仁玉', 'ハンプの膳玉', '五神の冥護', '甘美なモチベ', '3周年前夜祭', '3周年の喜び', '3周年の感謝', '今夜はスシﾊﾟ', '2021年の感謝', 'ご無沙汰', 'Wゴールドの喜び6', 'Wゴールドの喜び7', 'Wゴールドの喜び8', '4周年の喜び', 'Version.500の喜び', 'Version.600の喜び', '今夜は串ﾊﾟ', '4周年の感謝', '6周年の感謝', '全力疾走3', '4周年のドキドキ', '5周年のドキドキ', '6周年のドキドキ', '学習装置', 'ジズの紅玉', '人間の宝玉', 'レヴィアの蒼玉', 'アズの黄玉', 'マハの紺玉', 'シェイクスピアの狂玉', 'アザの桃玉', '2周年の感謝', 'そわそわ・・・', '2020年の感謝', '2周年のドキドキ', '2周年の喜び', '今夜はたこﾊﾟ', 'SPブラウザの喜び', 'Wゴールドの喜び3', 'SSランクの恩寵', 'Version.400の喜び', '今夜はピザﾊﾟ', 'Wゴールドの喜び4', '規格外の喜び', '10日目の感謝', '超経験値だよ…虹', 'リリース1000日の喜び', 'リリース1000日の感謝', 'Wゴールドの喜び5', '3周年の感謝(仮)', 'ピカキャの狂信者', '全力疾走2', '4周年の感謝(仮)', '熱血指導', 'スピードドライブ', 'Sランクの恩寵', '火事場改', '祝福のビギナー', 'ホワイトデーのお返し', 'ウルトラゾウル', 'ウナギの極意', 'ゴールドの喜び特大', '平成への感謝', 'リミテーション', '瓜姫流嘘吐道断術', 'コミュ力', '司書の優しさ', 'Version.300の喜び', 'うぇいうぇいふーっ！', '100万人の喜び', 'シュバババッ', '2周年の感謝(仮)', 'ガタガタ・・・', 'Wシルバーの喜び2', 'Wブロンズの喜び3', 'Wブロンズの幸せ', 'スケット・コゼット', 'Wブロンズの喜び2', 'ゴールドの喜び', '超ゴールドの喜び', '意識高い系ビギナー', '1周年の喜び', '1周年の感謝', 'Wゴールドの喜び', '超経験値だよ…金', '超経験値だよ…W金', 'ふんばり戦士', 'ふんばりナイト', 'ふんばり僧侶', 'ふんばりシーフ', 'ふんばり魔道士', 'おつむぺいん', '火事場', '霊峰', '脱兎', '酔っ払いセンサー', '21位の意地', 'ラジオマニア', 'Wゴールドの喜び2', '全力疾走', 'シルバーの喜び', 'ゴールドの喜び(仮)', 'Wシルバーの喜び', 'シルバーの喜び特大', 'ブロンズの喜び', '熱中症対策', 'Wブロンズの喜び', 'ブロンズの喜び特大', '神狩りのヴォーパルブレードZ', '二天飾斬りν', 'パワーバンプδ', 'ラピラドゥイス', '薔薇４の字固め', '愛慕のリリカルパルスX', 'パラライアップフェルα', 'ポイズンアップフェルβ', 'スリプアップフェルγ', 'メロメロメルトπ', 'ハロウィンズアークζ', 'ティディオレクション', 'あばら砕き', '超あばら砕き', 'バンカーバイト', 'ピュルテバウンド', 'キッズフェスビッグバンW', 'レイジングメディスンη', 'イノセントラブθ', 'パルデペンターノ', '五色結界', '高度な軍略', '天性の才能', '原初の鼓動', '博愛の炎羽', '大海の雫', '悪魔の豹変', '悪魔の折檻', '狂演出家のシナリオ', '悪魔の禁欲', '悪魔の嫉妬', '開闢の大地', '水清ければ月宿る', '紅蓮の浄火', '静寂の神風', '優駿の順風', '溟海の耽溺', '不貞な接吻', '傲慢な純潔', '多感な真火', '侠気と義気', '治癒の新生', 'バレンタインウォールH', 'エンゼルリンクω', 'アネーロ・リフレイン', 'エスフィカーティオ', 'チェリーブロッサムウォール', 'サツキバレウォール', 'ウェディングウォール', '誠実のアメジスト', '清浄のクリスタル', 'トレジャーハンターⅤ', '希望のジェイド', '仁愛のカーネリアン', '慈愛のアイオライト', '円満のパール', '忠実の徳', '節制の徳', 'カオティックディーパーティー', '慎重の徳', '正義の徳', '智慧の徳', '博愛の徳', '希望の徳', 'トレジャーハンターⅥ', '覇戒の陣', '妨禦の陣', '魔崩の陣', '豪傑のメンタル', '堅牢のメンタル', '勇猛のメンタル', '徳義の誓い', 'ドゥエロ・レント', 'アヴァン・レント', 'マギア・レント', 'ペルフェ・レント', 'ルブス・オルブ', 'アーラ・オルブ', 'マーレ・オルブ', 'ドルテ・オルブ', 'サルス・オルブ', 'ペトゥス・オルブ', 'ゼクスティアン', 'トレジャーハンターⅣ', '永遠のラピスラズリ', '情熱のガーネット', '創造のオパール', '沈着のアクアマリン', '幸福のペリドット', '純白のトパーズ', '信仰の戒', '真実の戒', '純潔の戒', '忍耐の戒', '慈愛の戒', '敬神の戒', '無欲の戒', '五大輪の借', 'ルビーの神秘', 'エメラルドの風雅', 'サファイアの崇高', 'トレジャーハンターⅢ', 'ダイヤモンドの威厳', 'マカロンボーイ', 'HPアップ特大', '攻撃力アップ特大', '防御力アップ特大', '攻撃魔力アップ特大', '回復魔力アップ特大', 'すばやさアップ特大', 'クリティカル率アップ特大', 'CTアップ特大', '憤怒之罪', '嫉妬之罪', '怠惰之罪', '傲慢之罪', '強欲之罪', '暴食之罪', '色欲之罪', 'コミニティ', '王の叫び', '妃の祈り', '公爵の憂い', '侍女の仕え', '王子の甘え', '民衆の嘆き', '不死鳥の冥護', '攻撃力アップ大', '防御力アップ大', '攻撃魔力アップ大', '回復魔力アップ大', 'すばやさアップ大', 'クリティカル率アップ大', 'CTアップ大', 'トレジャーハンター', 'HPアップ中', '攻撃力アップ中', '防御力アップ中', '攻撃魔力アップ中', '回復魔力アップ中', 'すばやさアップ中', 'クリティカル率アップ中', 'CTアップ中', 'HPアップ小', '攻撃力アップ小', '防御力アップ小', '攻撃魔力アップ小', '回復魔力アップ小', 'すばやさアップ小', 'クリティカル率アップ小', 'CTアップ小',
          '剛力王','サイン・オブ・ソード','サイン・オブ・アクス','サイン・オブ・スピア','サイン・オブ・ブック','エルダーの真玉','サイン・オブ・ロッド','黄昏より愛をこめて','サイン・オブ・ダガー','バルムンクの剣玉','サイン・オブ・アザーズ','ワールドリーフブレード','ワールドリーフアックス','ワールドリーフランス','Wゴールドの喜び9','ワールドリーフブック','タバアトの淡玉','ワールドリーフワンド','7周年のドキドキ','驢馬の迅輪','7周年の感謝','Wゴールドの喜び10','ワールドリーフダガー','ワールドリーフアロー','真っ当な支配','竜気解放','絶えず続く召喚',
          'サイン・オブ・アロー','ワールドリーフアザーズ','スズネの煩玉','スケピトゥソード','スケピトゥアックス','水の導き','教育の力','スケピトゥランス','スケピトゥブック','甘くて優しい想いをあなたに','バインバイン','潜在能力トリガー(攻)','覇王の膂力','スケピトゥワンド','明晰夢の世界','スケピトゥダガー','スケピトゥアロー','スケピトゥアザーズ','御伽乃覇気','祝福の悪夢','マリッジの祝玉','8周年のドキドキ','花嫁の誓い','騎士の在り方','タフティール・ソード','ヒヨリの鏡玉', '陰陽師の責務', 'ワンド', 'ペンタクル', 'ソード', 'カップ', '縁起物！！', 'タフティール・アックス', 'タフティール・ランス', 'タフティール・ブック', 'タフティール・ワンド', 'タフティール・ダガー', 'タフティール・アロー','タフティール・アザーズ','超学習装置','トリック・アンド・ゴッデス・ラブ','アサルテンス・ソード','魔法の箱庭','作家の箱庭','聖者の箱庭','アサルテンス・ランス','Version.700の喜び',
          'ノワゼッタの魔玉','シュティフトの体玉','プレイントの法玉']
l_search_trash=['ピュルテガンガンッ','ピュルテコスモ','アンパラリス','アンポイズ','ラジクイック','ラジクイック','ラジシルド','ラジテンション','ダウスロー','ダウプロト','ダウパワー','ピュルテタックル','バレンタインウォール','バレンタインベール','トランプコマンダー','超ゴールドラッシュ','超ゴールドラッシュ','エターナルブリザード？？','モワモワ☆エンヴィーウィンド','ビリビリ☆アングリーサンダー','ぬすむ','イノセントラブ','ゴールドラッシュ',
                'レイジングメディスン','フォレストアロー','インフェルノアロー','ダークホール','包帯男タックル','ピュルテフォール','ピュルテスライディング','ピュルテローリング','ピュルテドンッ','ゴッドスラップ','ポイズンアップフェル','パラライアップフェル','愛慕のリリカルパルス','リリカルギフト','キッズフェスビッグバン','キッズフェスマジック','カードコマンダー','カオスクラッシュ','カオスブレイク','エンゼルリンク','美流炎之舞','美流水之舞',
                '限界突破(攻撃)', '限界突破(魔法)', '闇属性ダメージ防御壁', '限界突破(特殊)', '天衣無縫の力', 'サマーバケーション', 'ワッショーイ！', '自動回復', '攻撃＆防御アップ小', '攻撃＆防御アップ中', '攻撃＆防御アップ中', '攻魔＆回魔アップ小', '攻魔＆回魔アップ中', '攻魔＆回魔アップ中', '攻撃＆攻魔アップ小', '女子力', '嫁力', '突込力', '飲兵衛力', '村人力', '二天飾斬り', '二天飾斬り', '強打', '剣士の一撃', 'パワーバンプ', 'シルバーラッシュ', '特大☆グレートジャーマン', 'ローゼ・ザ・グレートボム', 'ハロウィンズアーク', 'ロストメモリー', 'エルマイトカノン', 'スリプアップフェル', '変帝の偽攻', 'メロメロメルト', '御伽陸鰻斬', 'メロメロメルト', 'ヴォーパルソード', 'ヴォーパルソード', '神狩りのヴォーパルブレード', 'ジャバウォック突き', '鎧砕き', '鎧砕き', '精霊の審判', 'ウィンドヒール', 'ウィンドヒール', '包帯男ラッシュ', 'イカサマダイス', 'イカサマダイス', 'ブラックエッジ', '潜在能力トリガー(攻)', '潜在能力トリガー(攻)', 'アクアバスター', 'ライトニングバスター', 'ハーデスバスター', 'ブロンズラッシュ',]
path = r'C:\Users\user\Documents\GitHub\alex343425.github.io'

d_hpdebuff={
    '一輪花':10,
    '歌舞蓮矢':20,
    '艶麗の乱舞':30,
    'ダウシックスα':5,
    'ダウシックスβ':10,
    'ダウセブンズΩ':10,
    'ムーサへの祈り':30,
    'カリュプソーからの船出':30,
    'セイレーンの幻惑':50,
    'オデュッセウスの帰郷':70,
    'エヴァキュエイト・キャリプソ':30,
    '聖天の寵愛':10,
    '優明の導き':10,
    '神悲の憂患':30,
    '聖母の懐抱':50,
    '優明の導き＋':10,
    '往日-グリムメモリー-':20,
    '劣記-ミスイリュージョン-':30,
    '無追-アンリターンパスト-':40,
    '醒々-デイブレイクワールド-':50,
    '劣記-ミスイリュージョン-＋':30,
    '一枚だって逃さない！':10,
    '十枚ぽっちじゃ足りない！':20,
    '百枚あるなら千枚ある！':30,
    '大吸引・一吸万枚日！':40,
    '十枚ぽっちじゃ足りない！＋':20,
    '崩れ破する普遍の往日':50,
    '儚き夜の予告状':50
    }

def match(s):
    match = re.search(r'\{(.*?)\}', s)
    if match:
        result = match.group(1)
        #print(result)  # 輸出：ホーリーレイン
    else:
        print("找不到匹配的字串",s)
    return result

def match2(s):
    match = re.search(r'\[\[(.*?)\]\]', s)
    if match:
        result = match.group(1)
        #print(result)  # 輸出：★3/シンデレラ
    else:
        print("找不到匹配的字串",s)
        
    return result

def buff_cancel_search(y, skill_name=''):
    # 回傳 (機率分類, 最低消除數量)；全部消除為 99，未符合為 (0, 0)。
    if skill_name == 'Stand by Michiru':
        return 2, 1

    y = y.translate(str.maketrans('０１２３４５６７８９％', '0123456789%'))
    y = re.sub(r'<br\s*/?>', '。', y, flags=re.IGNORECASE)
    chance_pattern = (r'(?:確率\s*)?(?P<percent>\d+(?:\.\d+)?)\s*%(?:の確率)?|'
                      r'ごく稀|低確率|高確率|稀|確率|確実|必ず|必定')
    chance_tags = {'ごく稀': 1, '稀': 1, '低確率': 1, '確率': 2,
                   '高確率': 3, '確実': 4, '必ず': 4, '必定': 4}

    for clause in re.split(r'[。・、：:\r\n]+', y):
        effect = re.search(r'(?P<name>全?有利効果)(?P<details>.*?)'
                           r'(?:打ち消(?:す|し)|消去(?:する)?)', clause)
        if effect is None:
            continue

        # 僅搜尋有利効果的消除；ステータス上昇効果消去不會符合。
        details = effect.group('details').translate(
            str.maketrans('一二三四五六七八九', '123456789'))
        if effect.group('name').startswith('全') or '全' in details:
            count = 99
        else:
            quantity = re.search(r'(\d+)(?:\s*[~〜～－-]\s*(\d+))?\s*(?:つ|個)', details)
            if quantity is None:
                raise ValueError(f'未能判定有利効果消除數量：{clause}')
            count = min(int(n) for n in quantity.groups() if n is not None)

        # 限定在同一效果且截止於消除動詞，避免取到其他效果的機率。
        chances = list(re.finditer(chance_pattern, clause[:effect.end()]))
        if not chances:
            rate = 4
        elif chances[-1].group('percent') is None:
            rate = chance_tags[chances[-1].group()]
        else:
            percent = float(chances[-1].group('percent'))
            if percent in (5, 10):
                rate = 1
            elif percent in (25, 30):
                rate = 2
            elif 40 <= percent <= 80:
                rate = 3
            elif percent == 100:
                rate = 4
            else:
                raise ValueError(f'未定義的有利効果消除機率：{percent}%（{clause}）')
        return rate, count

    return 0, 0

def stat_down_search(y):
    #回傳格式：list
    #回傳格式：1=攻擊 2=防禦 3=攻魔 4=回魔 5=速度 6=無視耐性降防
    y=y.replace('・', '。')
    y=y.replace('、', '。')
    z=y.split('。')
    for z2 in z:        
        result = z2.find('関わらず')
        if result >= 0:
            break
        result = z2.find('耐性を無視')
        if result >= 0:
            break

    if '防御力を0' in z2:
        return [6]
    l_result=[]
    if isinforward(z2,['攻撃力','ダウン']) or isinforward(z2,['攻撃力','半減']):
        l_result.append(1)
    if isinforward(z2,['防御力','ダウン']) or isinforward(z2,['防御力','半減']):
        l_result.append(2)
    if isinforward(z2,['攻撃魔力','ダウン']) or isinforward(z2,['攻撃魔力','半減']):
        l_result.append(3)
    if isinforward(z2,['回復魔力','ダウン']) or isinforward(z2,['回復魔力','半減']):
        l_result.append(4)
    if isinforward(z2,['すばやさ','ダウン']) or isinforward(z2,['すばやさ','半減']):
        l_result.append(5)
    if isinforward(z2,['全パラメータ','ダウン','HPを除く']):        
        l_result.extend([1,2,3,4,5])    
    if len(l_result)==0:
        #print('降能力未匹配:',z2)
        pass
    return l_result

def mark_search(y):
    #回傳格式：數字
    #回傳格式：刻印倍率
    y=y.replace('・', '。')
    y=y.replace('、', '。')
    z=y.split('。')
    for z2 in z:        
        result = z2.find('刻印')
        if result >= 0:
            break
    
    def extract_numbers(s):
    # 使用正则表达式匹配括号中的两个数字
        match = re.search(r'\((\d+)倍/(\d+)回\)', s)
        if match:
            # 提取匹配到的数字并转换为整数
            return int(match.group(1)), int(match.group(2))
        else:
            # 如果没有匹配到，返回 None
            return None    
    
    i,j = extract_numbers(z2)    
    return i*j-j+1

def enemy_dmg_up_search(y):
    #回傳格式：list
    #回傳格式：1=一般被傷 2=武器被傷 3=技能種類被傷
    y=y.replace('・', '。')
    y=y.replace('、', '。')
    z=y.split('。')
    target_list=[]
    l_result=[]
    for z2 in z:
        result = z2.find('被ダメ')
        if result >= 0:
            target_list.append(z2)
    
    key_word_list=['軽減',
                   '被ダメージ半減',
                   '次回攻撃スキル威力が2倍になり次のターン終了まで被ダメージが1.5倍に上昇する',
                   '自身2ターン：文無しになり被ダメージ1.5倍',
                   '自身：次のターン終了まで被ダメージ1.5倍',
                   '被ダメージほんの少し減少',
                   '被ダメージ少し減少',
                   '被ダメージ減少',
                   '被ダメージ50％減少'
                   ]
    def contains_any_substring(s, substr_list):
        for substr in substr_list:
            if substr in s:
                return True
        return False

    for item in target_list:        
        if contains_any_substring(item,key_word_list):
            continue
        if 'スキルから' in item:
            l_result.append(3)
            continue
        if isinforward(item,['武器種','から','被ダメ']):
            l_result.append(2)
            #print(item)
            continue
        l_result.append(1)
    l_result = list(set(l_result))    
    return l_result

def status_condition_down(y):
    #回傳格式：int,str
    #回傳格式：數字=異常量 str=回合或備註
    key_word_list=['自身の全ての状態異常耐性が60％上昇し。攻撃対象の状態異常耐性をダウンさせて攻撃する',
                   '自身の全ての状態異常耐性が80％上昇し。攻撃対象の状態異常耐性をダウンさせて攻撃する',
                   '味方全員の攻撃力を上げて、攻撃対象の状態異常耐性を減少させて攻撃可能',
                   '味方全員の攻撃力を少し上げて、攻撃対象の状態異常耐性をほんの少し減少させて攻撃可能',
                   '敵の弱点を分析することで、攻撃対象の状態異常耐性を大幅に減少させて攻撃する',
                   '敵と味方の性質を完璧に分析することで味方全員の攻撃力を14％上げて、攻撃対象の状態異常耐性を大幅に減少させて攻撃する',
                   '「悪役令嬢のお仕置きリゾート」を読み陵辱の仕方を覚え、自身の攻撃力と攻撃魔力が14％上昇し、攻撃対象の状態異常耐性を減少させて攻撃する',
                   '「悪役令嬢のお仕置きリゾート」を読み陵辱の仕方を覚え、自身の攻撃力と攻撃魔力が24％上昇し、攻撃対象の状態異常耐性を減少させて攻撃する'
                   ]
    if y in key_word_list:
        return 0,''
    if '状態異常耐性100低下(重複なし)' in y:
        return 100,'3回合(不可疊加/機率觸發)'
    if '悲劇[状態異常耐性100低下]' in y:
        return 100,'3回合(機率觸發)'
    
    y_original = y
    y=y.replace('・', '。')
    y=y.replace('、', '。')
    y=y.replace('：', '。')
    y=y.replace('減少', 'ダウン')
    z=y.split('。')
    target_list=[]
    for z2 in z:
        i= z2.find('状態異常耐性')
        j= z2.find('ダウン')
        #result = z2.find('状態異常耐性')
        if i >= 0 and j>=0:
            target_list.append(z2)
    if len(target_list) == 0:
        return 0,''
    if target_list[0] =='攻撃対象の状態異常耐性をダウンさせて攻撃する':
        return 0,''
    d_check={        
        '状態異常耐性4回ダウン':40,
 '状態異常耐性3回ダウン':30,
 '状態異常耐性1～2回少しダウン':7,
 '状態異常耐性1〜2回ほんの少しダウン':5,
 '状態異常耐性12回ダウン':120,
 '状態異常耐性5～7回ダウン':60,
 '状態異常耐性大幅ダウン':15,
 '状態異常耐性3～7回ダウン':60,
 '攻撃力＆攻撃魔力＆すばやさ＆状態異常耐性ダウン':10,
 '状態異常耐性をほんの少しダウン':5,
 '状態異常耐性2回超大幅ダウン':40,
 '状態異常耐性1～3回ダウン':20,
 '状態異常耐性1～3回ほんの少しダウン':10,
 '状態異常耐性3～5回ダウン':40,
 '状態異常耐性1〜2回ダウン':10,
 '状態異常耐性3回超大幅ダウン':60,
 '状態異常耐性少しダウン':7,
 '状態異常耐性超大幅ダウン':20,
 '状態異常耐性2回ダウン':20,
 '状態異常耐性15回ダウン':150,
 '状態異常耐性ほんの少しダウン':5,
 '状態異常耐性8回ダウン':80,
 '状態異常耐性5～10回ダウン':75,
 '状態異常耐性2回大幅ダウン':30,
 '状態異常耐性ダウン(スキル変化＆超スキル変化有)':10,
 '1ターンの間状態異常耐性50回ダウン':500,
 '状態異常耐性7回ダウン':70,
 '状態異常耐性3回ほんの少しダウン':15,
 '状態異常耐性50回ダウン':500,
 '状態異常耐性2～3回ダウン':20,
 '状態異常耐性2回ほんの少しダウン':10,
 '状態異常耐性1～2回ダウン':10,
 '状態異常耐性20回ダウン':200,
 '状態異常耐性10回ダウン':100,
 '状態異常耐性少しダウン(CT独立)':7,
 '状態異常耐性7～10回ダウン':85,
 '状態異常耐性1～2回ほんの少しダウン':5,
 '状態異常耐性ダウン':10,
 '状態異常耐性2回少しダウン':14,
 '状態異常耐性5回少しダウン':35,
 '状態異常耐性6回ダウン':60,
 '状態異常耐性を少しダウン':7,
 '状態異常耐性1〜2回少しダウン':7,
 '状態異常耐性1～3回少しダウン':14,
 '状態異常耐性4回超大幅ダウン':80,
 '状態異常耐性3回少しダウン':21,
 '状態異常耐性がほんの少しダウン':5,
 '状態異常耐性5回ダウン':50,
 '状態異常耐性3回大幅ダウン':45,
 '状態異常耐性5回大幅ダウン':75,
 '状態異常耐性25回ダウン':250,
 '状態異常耐性13回ダウン':130
        }
    result =0
    for x,y in d_check.items():
        if target_list[0] == x:
            result =y
            break
    if result == 0:
        print(f"未匹配: {target_list[0]}")
    
    turn = '3回合'
    l_2trun =[
        '味方全員のHPを回復する。味方全員：ステータス減少効果一つリフレッシュ・低確率で全スキルリフレクト（1回限り100％発動）、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさ少しダウン・状態異常耐性少し減少・確率で悩殺＆昏睡の追加効果',
        '味方全員のHPを回復する。味方全員：ステータス減少効果一つリフレッシュ・全状態異常回復・確率で全スキルリフレクト（1回限り100％発動）、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさダウン・状態異常耐性減少・悩殺＆昏睡の追加効果',
        '味方全員のHPを大回復する。味方全員：魔女ノ宴(連続攻撃・全スキルリフレクト・全状態異常＆不利効果リフレッシュ)が発動、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさ大幅ダウン・状態異常耐性大幅減少・悩殺＆昏睡の追加効果',
        '味方全員のHPを大回復する。味方全員：魔女ノ宴(連続攻撃・全スキルリフレクト・全状態異常＆不利効果リフレッシュ)が発動、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさ超大幅ダウン・状態異常耐性超大幅減少・悩殺＆昏睡の追加効果',
        '味方全員のHPを回復する。味方全員：ステータス減少効果一つリフレッシュ・全状態異常回復・確率で全スキルリフレクト（1回限り100％発動）・状態異常耐性少しアップ、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさダウン・状態異常耐性減少・悩殺＆昏睡の追加効果(スキル変化＆超スキル変化有)',
        '味方全員のHPを大回復する。味方全員：魔女ノ宴(連続攻撃・全スキルリフレクト・全状態異常＆不利効果リフレッシュ)が発動・状態異常耐性アップ、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさ大幅ダウン・状態異常耐性大幅減少・悩殺＆昏睡の追加効果',
        '味方全員のHPを大回復する。味方全員：魔女ノ宴(連続攻撃・全スキルリフレクト・全状態異常＆不利効果リフレッシュ)が発動・状態異常耐性大幅アップ、敵全体：攻撃力＆防御力＆攻撃魔力＆回復魔力＆すばやさ超大幅ダウン・状態異常耐性超大幅減少・悩殺＆昏睡の追加効果',
        '味方全員のHPを回復する。味方全体：攻撃力＆防御力＆攻撃魔力＆すばやさ1〜3回少しアップ・ステータス減少効果一つリフレッシュ・低確率で全スキルリフレクト（1回限り100％発動）、敵全体：状態異常耐性少し減少',
        '味方全員のHPを回復する。。味方全体：攻撃力＆防御力＆攻撃魔力＆すばやさ3〜5回少しアップ・ステータス減少効果一つリフレッシュ・確率で全スキルリフレクト（1回限り100％発動）、敵全体：状態異常耐性減少',
        '味方全員のHPを大回復する。味方全員：次のターン終了まで元気歌(連続攻撃・全スキルリフレクト・不利効果3つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ5〜7回少しアップ、敵全体：状態異常耐性大幅減少、特殊効果：スキルコンティニュー(スキル使用後確実に超変化してCT100％増加)',
        '味方全員のHPを大回復する。味方全員：次のターン終了まで元気歌(連続攻撃・全スキルリフレクト・不利効果3つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ7〜10回少しアップ、敵全体：状態異常耐性超大幅減少',
        '味方全員のHPを回復する。味方全体：攻撃力＆防御力＆攻撃魔力＆すばやさ3〜5回少しアップ・ステータス減少効果二つリフレッシュ・確率で全スキルリフレクト（1回限り100％発動）、敵全体：状態異常耐性減少(スキル変化＆超スキル変化有)',
        '味方全員のHPを大回復する。味方全員：次のターン終了まで超元気歌(連続攻撃・全スキルリフレクト・不利効果4つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ5〜7回少しアップ、敵全体：状態異常耐性大幅減少、特殊効果：スキルコンティニュー(スキル使用後確実に超変化してCT100％増加)',
        '味方全員のHPを大回復する。味方全員：次のターン終了まで超元気歌(連続攻撃・全スキルリフレクト・不利効果4つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ7〜10回少しアップ、敵全体：状態異常耐性超大幅減少'
        ]
    if y_original in l_2trun:
        turn = '2回合'
    if y_original == '威力7000％の火属性5回全体攻撃。敵全体：1ターンの間状態異常耐性50回ダウン・悩殺＆封印の追加効果・火属性耐性半減(固有/サブスキルを発動する度にULTゲージ上昇)':
        turn = '1回合'
    if y_original == '味方全員のHPを回復する。。味方全体：攻撃力＆防御力＆攻撃魔力＆すばやさ3〜5回少しアップ・ステータス減少効果一つリフレッシュ・確率で全スキルリフレクト（1回限り100％発動）、敵全体：状態異常耐性減少' or y_original == '味方全員のHPを回復する。味方全体：攻撃力＆防御力＆攻撃魔力＆すばやさ3〜5回少しアップ・ステータス減少効果二つリフレッシュ・確率で全スキルリフレクト（1回限り100％発動）、敵全体：状態異常耐性減少(スキル変化＆超スキル変化有)' :
        result = 15
    if y_original == '味方全員のHPを大回復する。味方全員：次のターン終了まで元気歌(連続攻撃・全スキルリフレクト・不利効果3つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ5〜7回少しアップ、敵全体：状態異常耐性大幅減少、特殊効果：スキルコンティニュー(スキル使用後確実に超変化してCT100％増加)' or y_original == '味方全員のHPを大回復する。味方全員：次のターン終了まで超元気歌(連続攻撃・全スキルリフレクト・不利効果4つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ5〜7回少しアップ、敵全体：状態異常耐性大幅減少、特殊効果：スキルコンティニュー(スキル使用後確実に超変化してCT100％増加)' :
        result = 30
    if y_original == '味方全員のHPを大回復する。味方全員：次のターン終了まで元気歌(連続攻撃・全スキルリフレクト・不利効果3つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ7〜10回少しアップ、敵全体：状態異常耐性超大幅減少' or y_original == '味方全員のHPを大回復する。味方全員：次のターン終了まで超元気歌(連続攻撃・全スキルリフレクト・不利効果4つリフレッシュ)が発動・攻撃力＆防御力＆攻撃魔力＆すばやさ7〜10回少しアップ、敵全体：状態異常耐性超大幅減少' :
        result = 50
    
 
    return result,turn

def extra_skill(token2=''):
    f=open('skill_new2.json',mode='r',encoding="utf-8")
    skill_new2=f.read()
    skill_new2=json.loads(skill_new2)
    f.close()
    l=[]

    for y in l_search:
        flag=False
        for x in skill_new2:
            if x['n'] == y and x['l'] == x['ml']:
                l.append(x)
                flag = True                
                break
        if flag == False:
            print('沒找到:',y)
    sorted_data = sorted(l, key=lambda x: x['id'])
    
    if token2 == '':
        return sorted_data
        
    return
    
def char_special_passskill():
    #找包含 に装備時 和 S3稀有度的
    f=open('skill_new2.json',mode='r',encoding="utf-8")
    skill_new2=f.read()
    skill_new2=json.loads(skill_new2)
    f.close()
    l=[]
    global MMonsters
    
    def get_first_bracket_text(text):
        match = re.search(r'「(.*?)」', text)
        return match.group(1) if match else None
    
    for x in skill_new2:
        if 'に装備時' in x['d'] and x['sr'] == 8:
            y=get_first_bracket_text(x['d'])
            for z in MMonsters:
                if z['n'] == y:                    
                    x['skill_name'] = x['n']
                    x['skill_type'] = '綠S3'
                    x['skill_state'] = '專綠技'
                    x['description'] = x['d']
                    x['skill_char'] = y
                    x['char_id'] = z['id']
                    l.append(x)
                    break
                             
    
    return l
    
def isinforward(sentence,kw):
    n = 0
    first = 0
    for k in kw:
        n = sentence.find(k,n)+1
        if n == 0:
            return False
        if first ==0:
            first = n
    return True
def find_segment_with_keyword(s, keyword):
    # 使用「。・、」將s分段
    segments = [seg for seg in re.split('[。・、]', s) if seg]

    # 以空格將keyword分段
    keywords = keyword.split()

    for segment in segments:
        start_search_idx = 0
        all_found = True

        # 按照順序查找每一個關鍵字
        for key in keywords:
            idx_current = segment.find(key, start_search_idx)
            if idx_current != -1:
                # 更新搜索的起始位置
                start_search_idx = idx_current + len(key)
            else:
                all_found = False
                break

        # 如果所有關鍵字都按照順序出現在這一段
        if all_found:
            return segment

    return False

def damage_dealt_search(y):
    # 回傳 (player_dmg_up, enemy_dmg_down)，0 表示沒有符合的效果。
    def target_kind(text):
        if '攻撃対象' in text or '敵' in text:
            return 'enemy'
        if any(word in text for word in ['味方', 'キャラ', '自身以外', '自分以外', '非自身']):
            return 'ally'
        if '自身' in text or '自分' in text:
            return 'self'
        return None

    count = r'(?:\d+(?:[〜～~－-]\d+)?回|\d+(?:\.\d+)?[％%])?'
    degree = r'(?:ほんの少し|少し|超大幅|大幅)?'
    damage = (r'与ダメージ(?:[がをは])?(?:'
              r'(?P<multiplier>\d+(?:\.\d+)?)倍|'
              + count + degree + r'(?P<change>上昇|アップ|増加|減少|ダウン))')
    tokens = (r'(?P<header>[^。・、()（）:：<>]+)[:：]'
              r'|(?P<open>[(（])|(?P<close>[)）])|' + damage)
    target = None
    target_stack = []
    player_dmg_up = 0
    enemy_dmg_down = 0
    for match in re.finditer(tokens, y):
        if match.group('header') is not None:
            target = target_kind(match.group('header'))
            continue
        if match.group('open') is not None:
            target_stack.append(target)
            continue
        if match.group('close') is not None:
            if target_stack:
                target = target_stack.pop()
            continue

        prefix = re.split(r'[。・、()（）]', y[:match.start()])[-1]
        # 「次回攻撃スキル与ダメージを2倍」是次回技能威力的舊描述，不是与傷上升。
        if (match.group('multiplier') is not None
                and re.search(r'次回(?:攻撃魔法|攻撃|特殊|魔法|全)?スキル(?:の)?$', prefix)):
            continue
        effect_target = target
        if effect_target is None:
            # 冒號省略時，從該效果前文確認對象。
            effect_target = target_kind(prefix)
        if match.group('change') in ['減少', 'ダウン']:
            if effect_target == 'enemy':
                enemy_dmg_down = 1
            continue
        if effect_target not in ['self', 'ally']:
            continue

        multiplier = match.group('multiplier')
        value = float(multiplier) if multiplier is not None else None
        if value is not None and value <= 1:
            continue
        # 2.0 倍仍歸一般上升；只有嚴格大於 2 倍才歸 3 / 4。
        tag = 1 if effect_target == 'self' else 2
        if value is not None and value > 2:
            tag += 2
        # 同技能有多種上升時：倍率 > 2 優先，同級則非自身優先。
        player_dmg_up = max(player_dmg_up, tag)
    return player_dmg_up, enemy_dmg_down


def damage_reduction_search(y):
    # 回傳兩個去重排序的 list：(player_dmg_down, em_dmg_down)。
    # 1/2：一般減傷；3/4：屬性減傷；5/6：軽減シールド。奇數僅自身，偶數包含其他角色。
    def target_kind(text):
        if re.search(r'味方|全員|PT全体|パーティ|キャラ|自身以外|自分以外|非自身', text):
            return 'ally'
        if '攻撃対象' in text or re.search(r'敵(?!対心)', text):
            return 'enemy'
        if '自身' in text or '自分' in text:
            return 'self'
        return None

    # 標題不得跨過「軽減」，避免漏逗號或多餘冒號吞掉減傷效果。
    tokens = (r'(?P<header>(?:(?!軽減)[^。・、()（）:：<>\r\n])+)[：:]'
              r'|(?P<open>[(（])|(?P<close>[)）])'
              r'|(?P<sentence>。|<br\s*/?>|[\r\n]+)'
              r'|(?P<subject>自身以外|自分以外|非自身|自身|自分|'
              r'味方|全員|PT全体|パーティ|キャラ|攻撃対象|敵(?!対心))'
              r'|(?P<reduction>軽減(?P<shield>シールド)?)')
    elements = {'火': 1, '水': 2, '樹': 3, '光': 4, '闇': 5}
    player_dmg_down = set()
    em_dmg_down = set()
    target = None
    explicit_target = False
    target_stack = []
    effect_start = 0
    for match in re.finditer(tokens, y):
        if match.group('header') is not None:
            header = match.group('header')
            kind = target_kind(header)
            # 純回合期限標題沿用前一對象，例如「味方全員：次のターン終了まで：」。
            if kind is not None or not re.fullmatch(r'(?:次の|この)?ターン終了まで|\d+ターン', header):
                target = kind
                explicit_target = kind is not None
            continue
        if match.group('open') is not None:
            target_stack.append((target, explicit_target))
            continue
        if match.group('close') is not None:
            if target_stack:
                target, explicit_target = target_stack.pop()
            continue
        if match.group('sentence') is not None:
            target = None
            explicit_target = False
            effect_start = match.end()
            continue
        if match.group('subject') is not None:
            # 無冒號的舊描述沿用主語；有標題時不讓其他效果中提到的角色改變對象。
            if not explicit_target:
                target = target_kind(match.group('subject'))
            continue

        prefix = re.split(r'[。・、:：()（）<>\r\n]', y[effect_start:match.start()])[-1]
        effect_start = match.end()
        # 排除攻擊的「被ダメージ軽減(系)効果を無視」，仍可辨識同技能的實際減傷。
        if re.match(r'(?:系)?(?:効果)?(?:を|も)無視', y[match.end():]):
            continue
        if target == 'enemy':
            continue
        # 沒寫對象的被動效果視為自身。
        tag = 2 if target == 'ally' else 1
        if match.group('shield') is not None:
            player_dmg_down.add(tag + 4)
            continue

        attribute_matches = re.findall(r'([火水樹光闇全各])属性(?:の)?(?:被)?ダメージ', prefix)
        if attribute_matches:
            player_dmg_down.add(tag + 2)
            for attribute_name in attribute_matches:
                if attribute_name in ['全', '各']:
                    em_dmg_down.update(elements.values())
                else:
                    em_dmg_down.add(elements[attribute_name])
        else:
            player_dmg_down.add(tag)
    return sorted(player_dmg_down), sorted(em_dmg_down)


def barrier_search(y):
    # 回傳 (drain_baria, dispel_baria)，0 表示沒有符合的屏障。
    # 1：僅自身；2/3：其他角色單回機率/必定；4/5：其他角色多回機率/必定。
    barriers = {'ドレインバリア': 0, 'ディスペルバリア': 0}
    if not any(name in y for name in barriers):
        return 0, 0

    def target_kind(text):
        if re.search(r'味方|キャラ|自身以外|自分以外|非自身|PT全体|パーティ', text):
            return 'ally'
        if '攻撃対象' in text or re.search(r'敵(?!対心)', text):
            return 'enemy'
        if re.search(r'全員|全体', text):
            return 'ally'
        if '自身' in text or '自分' in text:
            return 'self'
        return None

    def is_random(match):
        if match is None:
            return False
        rate = match.group('rate_before') or match.group('rate_after')
        if rate is not None:
            return float(rate) < 100
        return match.group('chance') not in ['確実', '必ず', '必定']

    # 統一全形數字與符號；「A＆B(2回)」的回數及機率由兩種屏障共用。
    y = y.translate(str.maketrans('０１２３４５６７８９（）％＆', '0123456789()%&'))
    barrier = r'(?:ドレインバリア|ディスペルバリア)'
    chance = (r'(?P<chance>確率\s*(?P<rate_before>\d+(?:\.\d+)?)\s*%|'
              r'(?P<rate_after>\d+(?:\.\d+)?)\s*%の確率|'
              r'(?:超高|超低|高|中|低)?確率|ごく稀|稀|まれ|確実|必ず|必定)')
    tokens = (r'(?P<header>(?:(?!ドレインバリア|ディスペルバリア)'
              r'[^。・、():：<>\r\n])+)[：:]'
              r'|(?P<open>\()|(?P<close>\))'
              r'|(?P<sentence>。|<br\s*/?>|[\r\n]+)'
              r'|(?P<separator>[・、])|'
              + chance +
              r'|(?P<subject>自身以外|自分以外|非自身|自身|自分|'
              r'味方|PT全体|パーティ|全員|全体|キャラ|攻撃対象|敵(?!対心))'
              r'|(?P<barriers>' + barrier + r'(?:\s*&\s*' + barrier + r')*)'
              r'(?:\s*(?:を付与)?\s*\((?P<count>\d+(?:[〜～~－-]\d+)?)回\))?')
    target = None
    explicit_target = False
    random = False
    context_stack = []
    for match in re.finditer(tokens, y):
        if match.group('header') is not None:
            header = match.group('header')
            target = target_kind(header)
            explicit_target = target is not None
            random = is_random(re.search(chance, header))
            continue
        if match.group('open') is not None:
            # 狀態名稱的括號內沿用對象及該狀態的發動機率。
            context_stack.append((target, explicit_target, random))
            continue
        if match.group('close') is not None:
            if context_stack:
                target, explicit_target, random = context_stack.pop()
            continue
        if match.group('sentence') is not None:
            # 「味方全員：HPを回復。...」仍屬同一對象的效果清單。
            if not explicit_target:
                target = None
            random = False
            continue
        if match.group('separator') is not None:
            # 其他效果的機率不能延用到屏障；括號內仍保留外層狀態機率。
            random = context_stack[-1][2] if context_stack else False
            continue
        if match.group('chance') is not None:
            random = is_random(match)
            continue
        if match.group('subject') is not None:
            if not explicit_target:
                target = target_kind(match.group('subject'))
            continue

        if target == 'enemy':
            continue
        if target != 'ally':
            tag = 1
        else:
            count = match.group('count')
            # 沒寫回數的持續回合／狀態內屏障視為多回。
            multiple = count is None or max(map(int, re.split(r'[〜～~－-]', count))) >= 2
            tag = (4 if multiple else 2) + (0 if random else 1)
        for name in barriers:
            if name in match.group('barriers'):
                # 同技能有多種屏障效果時，保留較高的分類。
                barriers[name] = max(barriers[name], tag)
    return barriers['ドレインバリア'], barriers['ディスペルバリア']


def buff_drain_search(y):
    # 回傳 (機率分類, 最低吸取數量)；依描述採第一個效果，未符合為 (0, 0)。
    y = y.translate(str.maketrans('０１２３４５６７８９％', '0123456789%'))
    y = re.sub(r'<br\s*/?>', '。', y, flags=re.IGNORECASE)
    chance_pattern = (r'(?:確率\s*)?(?P<percent>\d+(?:\.\d+)?)\s*%(?:の確率)?|'
                      r'ごく稀|低確率|高確率|稀|確率|確実|必ず|必定')
    chance_tags = {'ごく稀': 1, '稀': 1, '低確率': 1, '確率': 2,
                   '高確率': 3, '確実': 4, '必ず': 4, '必定': 4}
    quantity = r'\d+(?:\s*[~〜～－-]\s*\d+)?'
    effect_pattern = (r'(?:(?P<all>全)|(?P<before>' + quantity + r')\s*回)?'
                      r'\s*バフドレイン(?:\s*(?P<after>' + quantity + r')\s*回)?')

    for clause in re.split(r'[。・、：:\r\n]+', y):
        effect = re.search(effect_pattern, clause)
        if effect is None:
            continue

        if effect.group('all'):
            count = 99
        else:
            count_text = effect.group('before') or effect.group('after')
            count = min(map(int, re.findall(r'\d+', count_text))) if count_text else 1

        # 僅取吸取效果前方的同段機率；＆串接的共同機率也適用。
        chances = list(re.finditer(chance_pattern, clause[:effect.start()]))
        if not chances:
            rate = 4
        elif chances[-1].group('percent') is None:
            rate = chance_tags[chances[-1].group()]
        else:
            percent = float(chances[-1].group('percent'))
            if 0 <= percent <= 10:
                rate = 1
            elif 11 <= percent <= 35:
                rate = 2
            elif 36 <= percent <= 99:
                rate = 3
            elif percent == 100:
                rate = 4
            else:
                raise ValueError(f'未定義的バフドレイン機率：{percent}%（{clause}）')
        return rate, count

    return 0, 0

def skill_description_search(d):
    
    d.pop('drain_baria', None)
    d.pop('dispel_baria', None)
    drain_baria, dispel_baria = barrier_search(d['description'])
    if drain_baria:
        d['drain_baria'] = drain_baria
    if dispel_baria:
        d['dispel_baria'] = dispel_baria
    d.pop('buff_cancel_rate', None)
    d.pop('buff_cancel_count', None)
    buff_cancel_rate, buff_cancel_count = buff_cancel_search(d['description'], d['skill_name'])
    if buff_cancel_rate:
        d['buff_cancel_rate'] = buff_cancel_rate
        d['buff_cancel_count'] = buff_cancel_count
    d.pop('buff_drain_rate', None)
    d.pop('buff_drain_count', None)
    buff_drain_rate, buff_drain_count = buff_drain_search(d['description'])
    if buff_drain_rate:
        d['buff_drain_rate'] = buff_drain_rate
        d['buff_drain_count'] = buff_drain_count
    l_result=[]
    if d['description'].find('関わらず') >0 or d['description'].find('耐性を無視') >0:
        l_result = stat_down_search(d['description'])
        if len(l_result) > 0:
            d['stat_down'] = l_result.copy()                                    
  
    d['em_resist']=[0]
    result_key = find_segment_with_keyword(d['description'],'属性弱')
    if result_key != False:
        d['em_resist']= d_em_resist[result_key[result_key.find('属性弱')-1]]
    result_key = find_segment_with_keyword(d['description'],'属性耐')
    if result_key != False:
        d['em_resist']= d_em_resist[result_key[result_key.find('属性耐')-1]]
    
    # 精靈槽：只記錄回復效果；格數與機率依指定整數分類。
    d.pop('spirit_gauge', None)
    d.pop('spirit_chance', None)
    spirit_description = d['description'].translate(
        str.maketrans('０１２３４５６７８９％〜～－', '0123456789%~~~'))
    spirit_match = re.search(
        r'(?:^|[。・、：:（(\s])'
        r'(?P<chance>稀に|低確率で|確率で|高確率で|確率(?:30|50)%で)?'
        r'(?:発動時)?\s*精霊ゲージ\s*(?P<gauge>1(?:\s*[~-]\s*[23])?|2(?:\s*[~-]\s*3)?|3)\s*回復',
        spirit_description)
    if spirit_match:
        spirit_gauge_tags = {'1': 2, '2': 4, '3': 6, '1~2': 3, '1~3': 3, '2~3': 5}
        spirit_chance_tags = {
            '稀に': 1, '低確率で': 1, '確率で': 2,
            '高確率で': 3, '確率30%で': 3, '確率50%で': 4, '': 5}
        spirit_gauge = re.sub(r'\s+', '', spirit_match.group('gauge')).replace('-', '~')
        d['spirit_gauge'] = spirit_gauge_tags[spirit_gauge]
        d['spirit_chance'] = spirit_chance_tags[spirit_match.group('chance') or '']
        
    if d['description'].find('刻印') > 0:
        result = mark_search(d['description'])
        if result > 0:
            d['mark'] = result
    
    d.pop('limit',None)
    limit_match = re.search(r'属性(?:の)?臨界を付与[(（](\d+)回HITで効果発動[)）]', d['description'])
    if limit_match:
        d['limit'] = int(limit_match.group(1))
    
    # 与ダメージ上升 / 下降，依效果對象及倍率新增技能標籤。
    d.pop('player_dmg_up', None)
    d.pop('enemy_dmg_down', None)
    player_dmg_up, enemy_dmg_down = damage_dealt_search(d['description'])
    if player_dmg_up:
        d['player_dmg_up'] = player_dmg_up
    if enemy_dmg_down:
        d['enemy_dmg_down'] = enemy_dmg_down

    # 軽減依對象及種類保留多個標籤，屬性輕減另記錄屬性。
    d.pop('player_dmg_down', None)
    d.pop('em_dmg_down', None)
    player_dmg_down, em_dmg_down = damage_reduction_search(d['description'])
    if player_dmg_down:
        d['player_dmg_down'] = player_dmg_down
    if em_dmg_down:
        d['em_dmg_down'] = em_dmg_down

    if d['description'].find('被ダメ') >0:
        l_result = enemy_dmg_up_search(d['description'])
        if len(l_result) > 0:
            d['enemy_dmg_up'] = l_result.copy()
    #異常
    if d['description'].find('状態異常耐性') >0:
        i,j = status_condition_down(d['description'])
        if i > 0:
            d['status_condition_down'] = i
            d['description']+=f"<br>降抗搜尋：降{i}抗/{j}"
    #降血
    d.pop('hp_debuff',None)
    if d['skill_name'] in d_hpdebuff:
        d['hp_debuff'] = d_hpdebuff[d['skill_name']]
        d['description']+=f"<br>降血技能：降{d['hp_debuff']}%HP"
    
    return d
        
def check_all_em_char(MMonsters):
    result=[]
    a_set=set()
    s_temp=''
    for x in MMonsters:
        if x['n'] in result:
            continue
        if s_temp != x['n']:
            s_temp = x['n']
            a_set.clear()
        else:
            a_set.add(x['a'])
            if len(a_set) >= 5:
                result.append(x['n'])        
    return result


f=open('fileAll.txt',mode='r',encoding="utf-8")
r=f.read()
f.close()
r=r.split('\n')[3:]
#增加改版後變化技能



f=open('sp_sort.json',mode='r',encoding="utf-8")
sp_sort=f.read()
sp_sort=json.loads(sp_sort)
f.close()
d_sp_sort={}
d_em_resist={
    '火':1,
    '水':2,
    '樹':3,
    '光':4,
    '闇':5,
    '各':6,
    '全':6,
    '種':6}

for x in sp_sort:
    if x['classify'] == '':
        continue
    if x['name_jp'] in d_sp_sort:
        continue
    else:
        d_sp_sort[x['name_jp']] = x['classify']
    

l=[]
url = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MMonsters.json'
MMonsters = requests.get(url).json()
set_wiki_name(MMonsters)
all_em_char = check_all_em_char(MMonsters)
skill_type_name=['昇華變化','昇華超變化']

for x in r:
    d={}
    try:
        x=x.split('|')
        #d['skill_name'] = match(x[1])
        d['skill_name'],d['skill_id'] = x[1].split(',')
        d['skill_id'] = int(d['skill_id'])//10
        d['skill_type'] = x[2]
        d['skill_state'] = x[3]
        d['skill_char']= match2(x[4])
        s_search = match2(x[4]).split('/')[1]
        img_name='0.png'
        for y in MMonsters:
            if y['n'] == s_search:
                img_name = str(y['id'])+'.png'
                break
        d['img_name']=img_name
        d['sp_sort'] = '未分類'
        if s_search in d_sp_sort:
            d['sp_sort'] = d_sp_sort[s_search]
            
        d['sp_sort_for_search']=0
        if '+不入池' in d['sp_sort']:#菓角不入池
            d['sp_sort_for_search'] = 6
        elif 'SP' in d['sp_sort']:#普池
            d['sp_sort_for_search'] = 1
        elif '合作' in d['sp_sort']:#合作
            d['sp_sort_for_search'] = 2
        elif '活動' in d['sp_sort']:#活動
            d['sp_sort_for_search'] = 3
        elif '限定' in d['sp_sort']:#限定
            d['sp_sort_for_search'] = 4
        else:#未匹配/三星/四星
            d['sp_sort_for_search'] = 5
        d['char_em']=x[5]
        if s_search in all_em_char:
            d['char_em'] = '全'
        d['char_wep']=x[6]
        d['description'] = x[7]
        d['CT'] = x[8]
        
        
        d = skill_description_search(d)
        
        l.append(d)
        #檢測變化技能 昇華變化 昇華超變化
        # if d['skill_name'] in skill_change.skill_change:
        #     s = skill_change.skill_change[d['skill_name']].split(',')
        #     i=0
        #     while len(s) > i *2:
        #         y = copy.deepcopy(d)
        #         if y['skill_char'] == '★5/セリヌンティウス':
        #             print('已檢測BUG')
        #             break
        #         # s[0] 技能名
        #         # s[1] 敘述
        #         y['skill_name'] = s[i*2]                
        #         y['description'] = s[i*2+1]
        #         y['skill_state'] = skill_type_name[i]            
        #         y = skill_description_search(y)
        #         l.append(y)
        #         i+=1
        
    except:
        continue
r_test = r.copy()
extra_skill = extra_skill()


for x in extra_skill:
    d={}
    d['skill_name'] = x['n']
    d['skill_type'] = skillclass(x['sc']) + skillrank(x['sr'])
    d['skill_id'] = int(x['id'])//10
    d['skill_state'] = '非角色'
    d['skill_char']= '非角色'
    #d['img_name']=img_name
    
    #if s_search in d_sp_sort:
    #    d['sp_sort'] = d_sp_sort[s_search]

    temp = attribute(x['a'])
    if temp == '':
        temp = '--'
    d['char_em']=temp
    d['char_wep']='--'
    d['description'] = x['d']
    d['sp_sort_for_search']=7
    try:
        d['ct'] = x['ct']
    except:
        pass
    d = skill_description_search(d)
    
        
    l.append(d)

l_char_special_passskill = char_special_passskill()
for x in l_char_special_passskill:
    d={}
    d['skill_name'] = x['n']
    d['skill_type'] = skillclass(x['sc']) + skillrank(x['sr'])
    d['skill_id'] = int(x['id'])//10
    d['skill_state'] = '課金專用綠'
    d['skill_char']= x['skill_char']
    #d['img_name']=img_name
    
    #if s_search in d_sp_sort:
    #    d['sp_sort'] = d_sp_sort[s_search]

    temp = attribute(x['a'])
    if temp == '':
        temp = '--'
    d['char_em']=temp
    d['char_wep']='--'
    d['description'] = x['d']
    d['sp_sort_for_search']=7
    d = skill_description_search(d)

    l.append(d)

s2 = json.dumps(l,ensure_ascii=False)
f=open('data.json',mode='w',encoding="utf-8")
r=f.write(s2)
f.close()
f=open(f"{path}/data.json",mode='w',encoding="utf-8")    
r=f.write(s2)
f.close()



#輸入隊長技
f=open('file_leader.txt',mode='r',encoding="utf-8")
r=f.read().split('\n')
f.close()
l_leader_test = []
list_of_awake_1=[] #全覚醒
list_of_awake_2=[] #超覚醒
for x in r:
    d={}
    try:
        x=x.split('|')
        d['skill_char']= match2(x[1])        
        d['skill_name'] = x[2]
        d['char_em']=x[3]
        s_search = match2(x[1]).split('/')[1]
        if s_search in all_em_char:
            d['char_em'] = '全'
        d['char_wep']=x[4]
        d['description'] = x[5]
        d['description'] = d['description'].replace('&br;','<br>')
        d['type'] = '隊長技能'        
        img_name='0.png'
        for y in MMonsters:
            if y['n'] == s_search:
                img_name = str(y['id'])+'.png'
                break
        d['img_name']=img_name
        
        if s_search in d_sp_sort:
            d['sp_sort'] = d_sp_sort[s_search]
        else:
            d['sp_sort'] = '未分類'
        if '永続昇華' in d['description']:
            d['permanent_skill_up'] = 1
        else:
            d['permanent_skill_up'] = 0
        if 'デバフ効果' in d['description']:
            d['debuff'] = 1
        else:
            d['debuff'] = 0
        if 'エンチャント' in d['description']:
            d['enchant'] = 1
        else:
            d['enchant'] = 0
        d['sp_sort_for_search']=0
        if '+不入池' in d['sp_sort']:#菓角不入池
            d['sp_sort_for_search'] = 6
        elif 'SP' in d['sp_sort']:#普池
            d['sp_sort_for_search'] = 1
        elif '合作' in d['sp_sort']:#合作
            d['sp_sort_for_search'] = 2
        elif '活動' in d['sp_sort']:#活動
            d['sp_sort_for_search'] = 3
        elif '限定' in d['sp_sort']:#限定
            d['sp_sort_for_search'] = 4
        else:#未匹配/三星/四星
            d['sp_sort_for_search'] = 5
        if '全覚醒' in d['description']:
            list_of_awake_1.append(s_search)
        if '超覚醒' in d['description']:
            list_of_awake_2.append(s_search)    
        l_leader_test.append(d)            
    except Exception as e:
        print(e)
        continue
url = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MWeapons.json'
wep_list = requests.get(url).json()

f=open('weapon2.txt',mode='r',encoding="utf-8")
r=f.read().split('\n')
f.close()


f=open('data_acc.json',mode='r',encoding="utf-8")
data_acc=f.read()
data_acc=json.loads(data_acc)
f.close()
name_in_list=[]
list_of_permanent_skill_up=[]

for x in r:
    d={}
    try:
        x=x.split('|')
        d['skill_char']= match2(x[3])
        d['skill_name'] = match(x[11])
        d['description'] = x[12]
        d['char_wep']=x[2]
        d['char_em']='--'
        for y in wep_list:
            if y['n'] == x[1]:
                z=y['rmid']
                break
        for y in MMonsters:
            if y['id'] == z:
                d['char_em'] = attribute(y['a'])
                break                                
        d['type'] = '專武技能'
        s_search = match2(x[3]).split('/')[1]
        if s_search in all_em_char:
            d['char_em'] = '全'
        img_name='0.png'
        for y in MMonsters:
            if y['n'] == s_search:
                img_name = str(y['id'])+'.png'
                break
        d['img_name']=img_name        
        if s_search in d_sp_sort:
            d['sp_sort'] = d_sp_sort[s_search]
            
        if '永続昇華' in d['description']:
            d['permanent_skill_up'] = 1
            list_of_permanent_skill_up.append(s_search)
        else:
            d['permanent_skill_up'] = 0
        if 'デバフ効果' in d['description']:
            d['debuff'] = 1
        else:
            d['debuff'] = 0
        if 'エンチャント' in d['description']:
            d['enchant'] = 1
        else:
            d['enchant'] = 0        
        d['sp_sort_for_search']=0
        if '+不入池' in d['sp_sort']:#菓角不入池
            d['sp_sort_for_search'] = 6
        elif 'SP' in d['sp_sort']:#普池
            d['sp_sort_for_search'] = 1
        elif '合作' in d['sp_sort']:#合作
            d['sp_sort_for_search'] = 2
        elif '活動' in d['sp_sort']:#活動
            d['sp_sort_for_search'] = 3
        elif '限定' in d['sp_sort']:#限定
            d['sp_sort_for_search'] = 4
        else:#未匹配/三星/四星
            d['sp_sort_for_search'] = 5
        l_leader_test.append(d)
        #找飾品
        l_acc=[]
        for item in data_acc:
            if item['acc_source_id'] == z:
                l_acc.append(item)
        if len(l_acc) == 0:
            continue
        for item in l_acc:
            d2=d.copy()
            if item['n'] in name_in_list:
                continue
            d2['skill_name'] = item['n']
            d2['description'] = item['d']
            d2['img_name_acc'] = item['id']
            d2['type'] = '角色飾品'
            if '永続昇華' in d2['description']:
                d2['permanent_skill_up'] = 1
            else:
                d2['permanent_skill_up'] = 0
            if 'デバフ効果' in d2['description']:
                d2['debuff'] = 1
            else:
                d2['debuff'] = 0
            if 'エンチャント' in d2['description']:
                d2['enchant'] = 1
            else:
                d2['enchant'] = 0        
            name_in_list.append(item['n'])
            l_leader_test.append(d2)
    except:
        continue


s3 = json.dumps(l_leader_test,ensure_ascii=False)
f=open('data_leader_wep.json',mode='w',encoding="utf-8")
r=f.write(s3)
f.close()
f=open(f"{path}/data_leader_wep.json",mode='w',encoding="utf-8")    
r=f.write(s3)
f.close()



#檢測角色
#MMonsters
list_to_show=[]
l_check=[]
i=0
MMonsters.reverse()
#vsid
for x in MMonsters:
    if x['r'] <=2:
        continue
    if x['vsid'] in l_check:
        continue
    l_check.append(x['vsid'])
    list_to_show.append(x)
list_to_show.reverse()
MMonsters.reverse()
#寫入固有技id對應技能顏色
f=open('skill_new2.json',mode='r',encoding="utf-8")
skill_new2=f.read()
skill_new2=json.loads(skill_new2)
f.close()
list_skillclass={}
for x in skill_new2:
    list_skillclass[x['id']] = x['sc']

l_cheerleading=[]
for x in list_to_show:
    d={}
     
    d['skill_char']= x['n']              
    d['char_em']=attribute(x['a'])
    if x['n'] in all_em_char:
        d['char_em'] = '全'
    d['char_wep']=weaponclass(x['wc'])
    img_name='0.png'
    for y in MMonsters:
        if y['n'] == d['skill_char']:
            img_name = str((int(y['id'])//10)*10+1)+'.png'
            break
    d['img_name']=img_name
    s_search = d['skill_char']
    if s_search in d_sp_sort:
        d['sp_sort'] = d_sp_sort[s_search]
    else:
        d['sp_sort'] = '未分類'
    if s_search in list_of_permanent_skill_up:
        d['permanent_skill_up'] = 1
    else:
        d['permanent_skill_up'] = 0
        
    if s_search in list_of_awake_1:
        d['awake']=1
    if x['id'] == 14816:
        d['awake']=1
    if s_search in list_of_awake_2:
        d['awake']=2
        
    d['sp_sort_for_search']=0
    if '+不入池' in d['sp_sort']:#菓角不入池
        d['sp_sort_for_search'] = 6
    elif 'SP' in d['sp_sort']:#普池
        d['sp_sort_for_search'] = 1
    elif '合作' in d['sp_sort']:#合作
        d['sp_sort_for_search'] = 2
    elif '活動' in d['sp_sort']:#活動
        d['sp_sort_for_search'] = 3
    elif '限定' in d['sp_sort']:#限定
        d['sp_sort_for_search'] = 4
    else:#未匹配/三星/四星
        d['sp_sort_for_search'] = 5
    #針對角色本身
    d['hp'] = x['ls']['mahp']
    d['def'] = x['ls']['mad']
    d['source_skill'] = skillclass(list_skillclass[x['vsid']])
    d['r'] = x['r']
    #slot
    d['sr1'] = skillrank(x['sr1'])
    d['sr2'] = skillrank(x['sr2'])
    d['sr3'] = skillrank(x['sr3'])
    d['sc1'] = skillclass(x['sc1'])
    d['sc2'] = skillclass(x['sc2'])
    d['sc3'] = skillclass(x['sc3'])
    d['slot1'] = d['sc1'] + d['sr1']
    d['slot2'] = d['sc2'] + d['sr2']
    d['slot3'] = d['sc3'] + d['sr3']
    #綠格
    temp_s=d['slot1']+d['slot2']+d['slot3']
    d['green_ss_up'] = temp_s.count('綠S3') + temp_s.count('綠SS')
    d['green_s3'] = temp_s.count('綠S3')
    d['pink'] = temp_s.count('粉A')
    d['orange'] = temp_s.count('橘A')
    d['purple'] = temp_s.count('紫A')
    d['blue'] = temp_s.count('藍A')
    l_cheerleading.append(d)


s3 = json.dumps(l_cheerleading,ensure_ascii=False)
f=open('data_cheerleading.json',mode='w',encoding="utf-8")
r=f.write(s3)
f.close()
f=open(f"{path}/data_cheerleading.json",mode='w',encoding="utf-8")    
r=f.write(s3)
f.close()


f=open('data.json',mode='r',encoding="utf-8")
data=f.read()
data=json.loads(data)
f.close()

f=open('data_leader_wep.json',mode='r',encoding="utf-8")
data_lw=f.read()
data_lw=json.loads(data_lw)
f.close()

d={}
for x in data:
    if x.get('img_name') == None:
        continue        
    k=x['img_name'].split('.')[0]
    if d.get(k) == None:
        d[k]={'skill':[],'ls':[],'wep':[],'acc':[]}
    d[k]['skill'].append(x)
    
for x in data_lw:
    if x.get('img_name') == None:
        continue
    k=x['img_name'].split('.')[0]
    if d.get(k) == None:
        d[k]={'skill':[],'ls':[],'wep':[],'acc':[]}
    if x['type'] == '隊長技能':
        d[k]['ls'].append(x)
    elif x['type'] == '角色飾品':
        d[k]['acc'].append(x)
    elif x['type'] == '專武技能':
        d[k]['wep'].append(x)
    else:
        print('error',x)

for x in l_char_special_passskill:
    k = str(x['char_id'])
    d[k]['skill'].append(x)

print('正在檢查角色立繪')
for x, y in d.items():
    if x == '0':
        continue
        
    # 確保所有必要的資料夾都存在
    os.makedirs("./charjson", exist_ok=True)
    os.makedirs(f"{path}/charjson", exist_ok=True)
    os.makedirs(f"{path}/charimg", exist_ok=True)
    
    # 將當前的資料轉成 JSON 字串
    s3 = json.dumps(y, ensure_ascii=False)
    
    # 預計比對的本地 JSON 路徑
    target_json_path = f"{path}/charjson/{x}.json"
    
    # 判斷是否需要執行圖片下載的旗標
    is_updated_or_new = True
    
    # 檢查本地的 JSON 是否已存在
    if os.path.exists(target_json_path):
        try:
            with open(target_json_path, mode='r', encoding="utf-8") as f:
                old_content = f.read()
            
            # 如果內容完全相同，則將旗標設為 False，不下載圖片
            if old_content == s3:
                is_updated_or_new = False
                #print(f"[{x}] JSON 內容完全相同，跳過圖片下載檢查。")
        except Exception as e:
            # 如果讀取舊檔失敗（例如檔案損壞），安全起見還是當作有更新
            print(f"[{x}] 讀取舊 JSON 失敗: {e}，將重新覆蓋並檢查圖片。")

    # 寫入第一個 JSON 檔
    with open(f"./charjson/{x}.json", mode='w', encoding="utf-8") as f:
        f.write(s3)
        
    # 寫入第二個 JSON 檔
    with open(target_json_path, mode='w', encoding="utf-8") as f:
        f.write(s3)
        
    # 只有在 JSON 有新增或修改時，才走進圖片抓取邏輯
    if is_updated_or_new:
        url = f"https://sp-assets.otogi-frontier.com/prodassets/SPBrowser/CharaStand/Posing/{x}.webp"                
        x2 = f"{(int(x) // 10)}5"
        url2 = f"https://sp-assets.otogi-frontier.com/prodassets/SPBrowser/CharaStand/Posing/{x2}.webp"

        img1_path = f"{path}/charimg/{x}.png"
        img2_path = f"{path}/charimg/{x2}.png"

        def download_image(target_url, save_path, char_id):
            # 如果 JSON 變了，但本地其實已經有這張圖片，也可以選擇跳過
            if os.path.exists(save_path):
                print(f"[{char_id}] 圖片已存在，跳過下載。")
                return

            try:
                response = requests.get(target_url, timeout=10)
                if response.status_code == 200:
                    try:
                        # 將 WebP 轉成 PNG
                        image = Image.open(BytesIO(response.content))

                        # 若有透明通道則保留
                        if image.mode not in ("RGB", "RGBA"):
                            image = image.convert("RGBA")

                        image.save(save_path, format="PNG")
                        print(f"[{char_id}] WebP 下載並轉成 PNG 成功！儲存至 {save_path}")

                    except Exception as e:
                        print(f"[{char_id}] WebP 轉 PNG 失敗: {e}")

                elif response.status_code == 404:
                    print(f"[{char_id}] 網頁回傳 404 (圖片不存在)，跳過。")
                else:
                    print(f"[{char_id}] 連線異常，狀態碼: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"[{char_id}] 發生網路錯誤: {e}")

        # 執行下載
        download_image(url, img1_path, x)
        download_image(url2, img2_path, x2)
    
#道具+食物
# addressS = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MSkills.json'
# addressM = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MMonsters.json'
# addressR = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MSpirits.json'
# addressW = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MWeapons.json'
# addressA = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MAccessory.json'
# addressI = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MItems.json'
# addressF = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MFoods.json'
# my_headersjp = {'token': '8b00d233-168c-41fd-a4ac-500e3da7ef15'}
# url = 'https://otogi-rest.otogi-frontier.com/api/Events/19002/exchangeItems'
# r_ex = requests.get(url, headers=my_headersjp).json()['Items']
# l_name=[]
# for x in r_ex:
#     l_name.append(x['ItemName'].split('のレシピ')[0])

# r = requests.get(addressI).json()
# l=[]
# for x in r:    
#     if x['ild'] == False:
#         continue
#     d={}
#     d['n'] = x['n']
#     d['id'] = x['id']
#     d['mc'] = x['mc'] #可攜帶數量
#     d['d'] = x['d'] #描述
#     d['msid'] = x['msid'] #對應技能編號
#     if x['n'] in l_name:
#         d['get'] = '追憶碎片交換所'
#     else:
#         d['get'] = 0
#     l.append(d)
    
# s3 = json.dumps(l,ensure_ascii=False)
# f=open('item.json',mode='w',encoding="utf-8")
# r=f.write(s3)
# f.close()

# r = requests.get(addressF).json()
# l=[]
# for x in r:    
#     if x['d'] == 'クエストで獲得したアイテムを一つ増やす。たべものではないが気にしないでください':
#         continue
#     if 'クエストで獲得したアイテムを一つ増やす' in x['d']:
#         continue
#     del x['sp']
#     del x['r']
#     if x['n'] in l_name:
#         x['get'] = '追憶碎片交換所'
#     else:
#         x['get'] = 0
#     l.append(x)
    
# s3 = json.dumps(l,ensure_ascii=False)
# f=open('food.json',mode='w',encoding="utf-8")
# r2=f.write(s3)
# f.close()




#更新特殊技能表
url='https://otogi-rest.otogi-frontier.com/api/USkills'
my_headers = {'token': 'c33e1c6f-be57-4284-81b9-e4deff317c89'
              ,'Content-Type': 'application/Json'}
try:
    r_skill=requests.get(url, headers=my_headers).json()
except:
    print('token錯誤')
    sys.exit()
my_skill = set()
for x in r_skill:
    my_skill.add(x['MSkillId'])
my_skill = list(my_skill)
#找我有的技能，但不在l_search內，也不在data內
f=open('fileAll.txt',mode='r',encoding="utf-8")
data=f.read()
f.close()
data=data.split('\n')[3:]
list_of_wiki_id=[]
for x in data:
    if x =='}}':
        continue    
    y=int(x.split('|')[-1])
    for z in range(y//10*10+1,y+1):
        list_of_wiki_id.append(z)

f=open('skill_new2.json',mode='r',encoding="utf-8")
skill_new2=f.read()
skill_new2=json.loads(skill_new2)
f.close()


dict_skill = {item['id']:item for item in skill_new2}
for x in my_skill:
    if x in list_of_wiki_id:
        continue
    if x in dict_skill and dict_skill[x]['n'] not in l_search and dict_skill[x]['n'] not in l_search_trash :
        y=dict_skill[x]
        print(y['n'])
        print(y['d'])
        print('----------------------')
            
            


