import mysql.connector
from ckip_transformers.nlp import CkipWordSegmenter
from Levenshtein import distance as lev_distance
from itertools import chain
from pypinyin import lazy_pinyin
from difflib import SequenceMatcher

# 使用 GPU
import torch
print(f"Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

# 閾值設定
SIMILARITY_THRESHOLD = 0.6
KEYWORD_MATCH_THRESHOLD = 0.7

# 拼音快取
pinyin_cache = {}


def get_pinyin(text):
    if text not in pinyin_cache:
        pinyin_cache[text] = "".join(lazy_pinyin(text))
    return pinyin_cache[text]


def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0


def pinyin_similarity(pinyin1, pinyin2):
    return SequenceMatcher(None, pinyin1, pinyin2).ratio()


def generate_ngrams(tokens, n):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def validate_keywords(place_keywords, test_ws, threshold=0.7):
    match_count = 0
    test_ws_set = set(test_ws)

    place_pinyin_list = ["".join(lazy_pinyin(word)) for word in place_keywords]
    test_ws_pinyin_list = ["".join(lazy_pinyin(word)) for word in test_ws]

    for idx, kw in enumerate(place_keywords):
        kw_pinyin = place_pinyin_list[idx]
        matched = False

        for i, test_word in enumerate(test_ws):
            if kw == test_word:
                matched = True
                break
            if lev_distance(kw, test_word) <= 1:
                matched = True
                break
            if pinyin_similarity(kw_pinyin, test_ws_pinyin_list[i]) >= 0.85:
                matched = True
                break

        if matched:
            match_count += 1

    match_rate = match_count / len(place_keywords)
    return match_rate >= threshold


# 資料庫連接
try:
    conn = mysql.connector.connect(
        user='root', password='dragonsys',
        host='sql.dragonsys.eu.org', database='MIS_Final',
        charset='utf8mb4', collation='utf8mb4_unicode_ci')
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"資料庫連接失敗: {err}")
    exit(1)

# CKIP 初始化
try:
    ws_driver = CkipWordSegmenter(model="bert-base", device=0)
except Exception as e:
    print(f"斷詞器初始化失敗: {e}")
    exit(1)

# 查詢景點
try:
    cursor.execute("""
        SELECT loc_name, area_name, spot_name
        FROM Location, Area, Spot
        WHERE Location.loc_id = Area.loc_id
        AND Area.area_id = Spot.area_id
        AND REPLACE(REPLACE(Location.loc_name, '縣', ''), '市', '') = '嘉義'
    """)
    rows = cursor.fetchall()
except mysql.connector.Error as err:
    print(f"讀取資料庫失敗: {err}")
    exit(1)

# 斷詞景點
texts = [row[2] for row in rows]
ws_results = ws_driver(texts, use_delim=True)
place_dict = {row[2]: ws for row, ws in zip(rows, ws_results)}

# 讀取字幕
file_path = r"D:\\1114534\\畢專程式測試\\暫存\\generated_subtitles.txt"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        test_text = f.read()
except Exception as e:
    print(f"讀取檔案失敗: {e}")
    exit(1)

# 字幕斷詞
try:
    test_ws = ws_driver([test_text], use_delim=True)[0]
except Exception as e:
    print(f"測試文本斷詞失敗: {e}")
    exit(1)

# 比對
matches = {}
for place, words in place_dict.items():
    word_str = "".join(words)
    word_set = set(words)
    n = len(words)

    # 為該景點產生 n±1 長度的 n-gram
    candidate_ngrams = []
    for delta in [-1, 0, 1]:
        current_n = n + delta
        if current_n > 0:
            candidate_ngrams.extend(generate_ngrams(test_ws, current_n))

    best_score = 0
    best_ngram = None
    for ngram in candidate_ngrams:
        ngram_tokens = ngram.split()
        ngram_str = "".join(ngram_tokens)
        ngram_set = set(ngram_tokens)

        jaccard = jaccard_similarity(word_set, ngram_set)
        if jaccard < 0.2:
            continue

        word_pinyin = get_pinyin(word_str)
        ngram_pinyin = get_pinyin(ngram_str)
        pinyin_score = pinyin_similarity(word_pinyin, ngram_pinyin)

        lev_score = 1 - (lev_distance(word_str, ngram_str) /
                         max(len(word_str), len(ngram_str)))

        final_score = 0.4 * pinyin_score + 0.3 * jaccard + 0.3 * lev_score
        if final_score > best_score:
            best_score = final_score
            best_ngram = ngram

    if best_score > SIMILARITY_THRESHOLD:
        matches[place] = (best_ngram, best_score)

# 關鍵詞驗證
filtered_matches = {}
for place, (best_ngram, best_score) in matches.items():
    if validate_keywords(place_dict[place], test_ws, KEYWORD_MATCH_THRESHOLD):
        filtered_matches[place] = (best_ngram, best_score)

print(f"關鍵詞驗證後，匹配結果數: {len(filtered_matches)}")

# 寫入結果
output_file_path = r"D:\\1114534\\畢專程式測試\\暫存\\matching_results.txt"
try:
    with open(output_file_path, "w", encoding="utf-8") as f:
        for place, (ngram, score) in filtered_matches.items():
            f.write(f"可能匹配的地點: {place}\n")
            f.write(f"  - 文本片段: {ngram}, 相似度: {score:.2f}\n")
    print(f"匹配結果已寫入 {output_file_path}")
except Exception as e:
    print(f"寫入檔案失敗: {e}")
finally:
    cursor.close()
    conn.close()
