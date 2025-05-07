from collections import defaultdict
import os
import re

def get_day_number(filename):
    """從檔案名稱中提取天數，例如 'Day1_1.jpg' 提取 1"""
    try:
        filename = os.path.basename(filename)  # 確保只處理檔案名稱，不包含路徑
        match = re.match(r"Day(\d+)", filename)  # 使用正則表達式提取數字
        if match:
            day_number = int(match.group(1))
            return day_number
        else:
            print(f"無效的天數格式：{filename}")
            return None
    except ValueError:
        print(f"無效的天數格式：{filename}")
        return None

def group_photos_by_day(photo_files):
    """按天數分組照片"""
    photo_groups = defaultdict(list)
    for filename in photo_files:
        day_number = get_day_number(filename)
        if day_number is not None:
            photo_groups[day_number].append(filename)
    return photo_groups