from flask import Flask, request, jsonify
import os
import re
import json
import torch
import traceback
import Levenshtein
import mysql.connector
from yt_dlp import YoutubeDL
from pypinyin import lazy_pinyin
from mysql.connector import Error
from difflib import SequenceMatcher
from collections import defaultdict
from faster_whisper import WhisperModel

app = Flask(__name__)

# === 設定 ===
SIMILARITY_THRESHOLD_FIRST = 0.94
SIMILARITY_THRESHOLD_SECOND = 0.835
CACHE_PATH = r"D:\\1114534\\畢專程式測試\\暫存\\pinyin_cache.json"
file_path = r"D:\\1114534\\畢專程式測試\\暫存\\generated_subtitles1.txt"
output_dir = r"D:\\1114534\\畢專程式測試\\暫存"

os.makedirs(output_dir, exist_ok=True)

# === 載入拼音快取 ===
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            pinyin_cache = json.load(f)
    except json.JSONDecodeError:
        print("偵測到快取檔案格式錯誤，將使用空白快取。")
        pinyin_cache = {}
else:
    pinyin_cache = {}


# === 過濾或移除特殊字元的函數 ===
def sanitize_filename(filename):
    sanitized = re.sub(r'[^\w\s]', '', filename).replace(" ", "_")
    return sanitized[:100]


# === yt-dlp選項設置，只下載字幕和音訊 ===
def download_subtitle_and_audio(video_url):
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': ['zh-TW', 'zh-Hant'],
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)

        sanitized_title = sanitize_filename(video_title)
        downloaded_audio_file = ydl.prepare_filename(
            info_dict).replace('.webm', '.flac')
        sanitized_audio_file = os.path.join(
            output_dir, f"{sanitized_title}.flac")

        if os.path.exists(downloaded_audio_file):
            os.rename(downloaded_audio_file, sanitized_audio_file)
            print(f"音訊檔案已重命名為：{sanitized_audio_file}")
        else:
            print(f"未找到預期的音訊檔案：{downloaded_audio_file}")

        # 確定字幕檔案路徑
        subtitles = info_dict.get('subtitles', {})
        subtitle_path = None
        if subtitles:
            subtitle_path = os.path.join(
                output_dir, f"{video_title}.zh-TW.vtt")
            if not os.path.exists(subtitle_path):
                subtitle_path = os.path.join(
                    output_dir, f"{video_title}.zh-Hant.vtt")

            if os.path.exists(subtitle_path):
                print(f"字幕檔案已找到：{subtitle_path}")
            else:
                print("字幕檔案未找到，可能下載失敗或名稱不匹配。")
                subtitle_path = None

        return video_title, sanitized_audio_file, subtitle_path


# === 清理 VTT 檔案，只保留字幕內容 ===
def clean_vtt_file(vtt_path, output_path):
    if not os.path.exists(vtt_path):
        return None

    with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
        lines = vtt_file.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line or "-->" in line or line.isdigit() or line in ["WEBVTT", "Kind: captions", "Language: zh-TW"]:
            continue
        cleaned_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("\n".join(cleaned_lines))

    return output_path


# === 檢查是否需要使用whisper生成字幕 ===
def generate_subtitle_if_needed(audio_file, subtitle_path, output_dir, cleaned_subtitle_path):
    if subtitle_path and os.path.exists(subtitle_path):
        print(f"使用影片的字幕檔：{subtitle_path}")
        clean_vtt_file(subtitle_path, cleaned_subtitle_path)
        return cleaned_subtitle_path
    else:
        print("未找到字幕檔，使用 Whisper 生成字幕...")
        transcript_path = generate_subtitle_with_whisper(
            audio_file, output_dir)
        if not os.path.exists(transcript_path):
            raise Exception("字幕生成失敗，無法找到生成的字幕檔案")
        return transcript_path


# === 使用 Whisper 生成字幕 ===
def generate_subtitle_with_whisper(audio_file, output_dir):
    """
    使用 Whisper 生成字幕。
    Args:
        audio_file (str): 音訊檔案的路徑。
        output_dir (str): 輸出字幕檔案的目錄。
    Returns:
        str: 生成的字幕檔案的路徑。
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    model = WhisperModel("medium", device=device, compute_type=compute_type)
    segments, _ = model.transcribe(audio_file, language="zh")
    full_text = "".join([segment.text for segment in segments])
    subtitle_path = os.path.join(output_dir, "generated_subtitles.txt")
    with open(subtitle_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"字幕已生成：{subtitle_path}")
    return subtitle_path


# === 連接資料庫 ===
def connect_to_database():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='dragonsys',
            host='sql.dragonsys.eu.org',
            database='MIS_Final',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        if cnx.is_connected():
            print("成功連接到資料庫")
            cursor = cnx.cursor(dictionary=True)
            return cnx, cursor
    except Error as e:
        print(f"資料庫連接失敗：{e}")
        return None, None


def extract_location_from_title(cursor, title):
    """
    從影片標題中提取縣市和行政區名稱，並根據資料庫進行模糊篩選。
    """
    # 從資料庫中獲取所有縣市名稱
    cursor.execute("SELECT DISTINCT loc_name FROM Location")
    all_locations = [row['loc_name'] for row in cursor.fetchall()]
    if not all_locations:
        raise Exception("資料庫中沒有縣市名稱資料")

    # 從資料庫中獲取所有行政區名稱
    cursor.execute("SELECT DISTINCT area_name FROM Area")
    all_areas = [row['area_name'] for row in cursor.fetchall()]
    if not all_areas:
        raise Exception("資料庫中沒有行政區名稱資料")

    # 初始化結果
    loc_names = []
    area_names = []

    # 特殊處理 "嘉義" 和 "新竹"
    if "嘉義" in title:
        loc_names.extend(["嘉義市", "嘉義縣"])
    elif "新竹" in title:
        loc_names.extend(["新竹市", "新竹縣"])
    else:
        # 模糊匹配縣市名稱
        for loc in all_locations:
            if loc.replace("市", "").replace("縣", "") in title:
                loc_names.append(loc)

    if not loc_names:
        raise Exception("無法從標題中提取縣市名稱")

    # 如果有提取到縣市名稱，篩選出對應的行政區
    query = """
        SELECT DISTINCT area_name
        FROM Area
        JOIN Location ON Area.loc_id = Location.loc_id
        WHERE Location.loc_name IN (%s)
    """ % (", ".join(["%s"] * len(loc_names)))
    cursor.execute(query, loc_names)
    possible_areas = [row['area_name'] for row in cursor.fetchall()]

    if not possible_areas:
        raise Exception("無法根據縣市名稱篩選出對應的行政區")

    # 模糊匹配行政區名稱
    for area in possible_areas:
        if area.replace("市", "").replace("鄉", "").replace("鎮", "") in title:
            area_names.append(area)

    return loc_names, area_names


# === 將字幕內容轉換為拼音列表 ===
def text_to_pinyin_list(text: str) -> list:
    return [get_char_pinyin(ch) for ch in text]


# === 獲取單個字的拼音 ===
def get_char_pinyin(char: str) -> str:
    if char not in pinyin_cache:
        pinyin_cache[char] = lazy_pinyin(char)[0]
    return pinyin_cache[char]


# === 將景點名稱轉換為拼音並存儲在字典中 ===
def spot_names_to_pinyin(spot_names):
    spot_pinyin_dict = defaultdict(list)
    for spot_name in spot_names:
        pinyin = lazy_pinyin(spot_name)
        spot_pinyin_str = ' '.join(pinyin)
        spot_pinyin_dict[spot_pinyin_str].append(spot_name)
    return spot_pinyin_dict


def save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(pinyin_cache, f, ensure_ascii=False, indent=2)


# === 比對字幕內容和景點名稱 ===
def compare_location_with_layers(transcript_pinyin_list, spot_pinyin_dict):
    first_layer_matches = {}
    second_layer_matches = {}
    used_segments = set()

    # 第一層比對：完全匹配
    for spot_pinyin, spot_names in spot_pinyin_dict.items():
        spot_len = len(spot_pinyin.split())  # 獲取景點拼音名稱的長度

        # 生成對應長度的 n-gram
        candidate_ngrams = [
            " ".join(transcript_pinyin_list[i:i + spot_len])
            for i in range(len(transcript_pinyin_list) - spot_len + 1)
        ]

        # 比對 n-gram 與景點拼音名稱
        for ngram in candidate_ngrams:
            if ngram == spot_pinyin:
                first_layer_matches[spot_pinyin] = {
                    "match": ngram,
                    "spot_names": spot_names
                }
                used_segments.add(ngram)

    # 從文本中移除第一層匹配的 n-gram
    remaining_pinyin_list = transcript_pinyin_list[:]
    for ngram in used_segments:
        ngram_len = len(ngram.split())
        for i in range(len(remaining_pinyin_list) - ngram_len + 1):
            if " ".join(remaining_pinyin_list[i:i + ngram_len]) == ngram:
                # 將匹配的 n-gram 替換為空白，避免重疊
                for j in range(i, i + ngram_len):
                    remaining_pinyin_list[j] = ""

    # 移除空白元素
    remaining_pinyin_list = [p for p in remaining_pinyin_list if p]

    # 第二層比對：相似度計算
    for spot_pinyin, spot_names in spot_pinyin_dict.items():
        spot_len = len(spot_pinyin.split())  # 獲取景點拼音名稱的長度

        # 生成對應長度的 n-gram
        candidate_ngrams = [
            " ".join(remaining_pinyin_list[i:i + spot_len])
            for i in range(len(remaining_pinyin_list) - spot_len + 1)
        ]

        # 比對 n-gram 與景點拼音名稱
        for ngram in candidate_ngrams:
            if ngram in used_segments:  # 跳過已匹配的 n-gram
                continue
            similarity = 1 - \
                Levenshtein.distance(spot_pinyin, ngram) / \
                max(len(spot_pinyin), len(ngram))
            if similarity >= SIMILARITY_THRESHOLD_SECOND:
                second_layer_matches[spot_pinyin] = {
                    "match": ngram,
                    "spot_names": spot_names,
                    "similarity": similarity
                }

    print(f"第一層比對結果：{first_layer_matches}")
    print(f"第二層比對結果：{second_layer_matches}")

    save_cache()
    return {
        "first_layer": first_layer_matches,
        "second_layer": second_layer_matches
    }


# === Flask ===
@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': '未提供影片網址'}), 400

    try:
        # 連接資料庫
        cnx, cursor = connect_to_database()
        if not cnx or not cursor:
            return jsonify({'error': '資料庫連接失敗'}), 500

        # 取得影片標題
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', None)
            sanitized_title = sanitize_filename(video_title)
            print("影片標題：", sanitized_title)

        # 下載影片音訊和字幕
        video_title, audio_file, subtitle_path = download_subtitle_and_audio(
            video_url)

        # 如果有字幕檔，清理字幕內容
        transcript_path = generate_subtitle_if_needed(
            audio_file, subtitle_path, output_dir, file_path)

        # 讀取清理後的字幕內容
        if not os.path.exists(transcript_path):
            raise Exception("字幕檔案不存在，請檢查字幕下載或生成邏輯。")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()

        if not transcript.strip():
            raise Exception("字幕檔案內容為空，請檢查字幕清理邏輯。")
        print(f"字幕內容長度：{len(transcript)}")
        print(f"字幕內容預覽：{transcript[:100]}")

        # 從標題中提取縣市和行政區名稱
        loc_names, area_names = extract_location_from_title(
            cursor, video_title)
        if not loc_names:
            print("無法從標題中提取縣市名稱")
            return jsonify({'error': '無法從標題中提取縣市名稱'}), 400
        print("提取出的縣市名稱：", loc_names)
        print("提取出的行政區名稱：", area_names)

        # 根據縣市和行政區篩選景點
        if loc_names:
            query = """
                SELECT loc_name, area_name, spot_name
                FROM Location, Area, Spot
                WHERE Location.loc_id = Area.loc_id
                AND Area.area_id = Spot.area_id
                AND Location.loc_name IN (%s)
            """ % (", ".join(["%s"] * len(loc_names)))

            params = loc_names

            if area_names:
                query += " AND Area.area_name IN (%s)" % (
                    ", ".join(["%s"] * len(area_names)))
                params.extend(area_names)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                print("資料庫查詢結果為空")
                raise Exception("資料庫中沒有符合條件的資料")
            print(f"查詢結果數量：{len(rows)}")

        # 提取景點名稱
        spot_names = [row['spot_name'] for row in rows]

        # 預處理文本和景點名稱的拼音
        transcript_pinyin_list = text_to_pinyin_list(transcript)
        if not transcript_pinyin_list:
            raise Exception("字幕內容的拼音列表為空")

        spot_pinyin_dict = spot_names_to_pinyin(spot_names)
        if not spot_pinyin_dict:
            raise Exception("景點名稱的拼音字典為空")

        # 比對結果
        results = compare_location_with_layers(
            transcript_pinyin_list, spot_pinyin_dict)
        if not results["first_layer"] and not results["second_layer"]:
            raise Exception("未找到任何匹配的景點")

        # 提取匹配的景點名稱（合併第一層和第二層）
        matched_places = []

        # 合併第一層結果
        for match in results["first_layer"].values():
            matched_places.append({
                "spot_names": match["spot_names"],
                "match": match["match"]
            })

        # 合併第二層結果
        for match in results["second_layer"].values():
            matched_places.append({
                "spot_names": match["spot_names"],
                "match": match["match"],
                "similarity": match["similarity"]
            })

        return jsonify({
            'status': 'success',
            'matched_places': matched_places
        })

    except Exception as e:
        print("發生未預期的錯誤：", e)
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'error': '伺服器內部錯誤',
            'details': str(e)
        }), 500

    finally:
        cursor.close()
        cnx.close()

        # 刪除音訊檔案
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"音訊檔案已刪除：{audio_file}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
