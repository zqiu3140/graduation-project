from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore, storage
import tempfile
import os
from typing import List, Optional, Dict
import uuid
from datetime import datetime, date
from collections import defaultdict

# 導入本地模組
from styles import generate_pdf
from Takepicture import get_date_from_image

app = FastAPI()

# 初始化Firebase (您需要提供自己的憑證檔案)
cred = credentials.Certificate("../key/g-project-60175-firebase-adminsdk-fbsvc-2d2703fd7f.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'g-project-60175.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

class MemoryRequest(BaseModel):
    title: str
    trip_id: str
    user_id: str
    style: str = "classic"

def group_photos_by_exif_date(photo_files):
    """根據照片的EXIF拍攝日期分組照片"""
    photo_groups = defaultdict(list)
    unknown_date_group = []
    
    # 獲取行程的所有日期並排序
    all_dates = []
    
    for photo_path in photo_files:
        photo_date = get_date_from_image(photo_path)
        if photo_date:
            all_dates.append(photo_date)
    
    # 移除重複日期並排序
    unique_dates = sorted(list(set(all_dates)))
    
    # 如果沒有有效日期，返回空分組
    if not unique_dates:
        return {}
    
    # 將日期映射到行程天數（第1天，第2天...）
    date_to_day = {date_val: day_num for day_num, date_val in enumerate(unique_dates, 1)}
    
    # 根據EXIF日期將照片分配到相應的天數
    for photo_path in photo_files:
        photo_date = get_date_from_image(photo_path)
        if photo_date and photo_date in date_to_day:
            day_number = date_to_day[photo_date]
            photo_groups[day_number].append(photo_path)
        else:
            # 沒有EXIF日期資訊的照片放在未知組（將在後續處理中分配）
            unknown_date_group.append(photo_path)
    
    # 處理沒有EXIF日期的照片（平均分配到各天）
    if unknown_date_group:
        # 如果所有照片都沒有日期，創建一個默認的第1天
        if not photo_groups:
            photo_groups[1] = unknown_date_group
        else:
            # 平均分配到已有的天數中
            days = sorted(photo_groups.keys())
            for i, photo in enumerate(unknown_date_group):
                day = days[i % len(days)]
                photo_groups[day].append(photo)
    
    return photo_groups
# 添加新端點，與 Flutter 應用匹配
@app.post("/Memory_genre")
async def create_memory_genre(request: MemoryRequest, background_tasks: BackgroundTasks):
    # 直接呼叫現有函數，避免重複代碼
    return await create_memory(request, background_tasks)

@app.post("/generate-memory")
async def create_memory(request: MemoryRequest, background_tasks: BackgroundTasks):
    # 檢查行程是否存在
    trip_ref = db.collection('trips').document(request.trip_id)
    trip = trip_ref.get()
    
    if not trip.exists:
        raise HTTPException(status_code=404, detail="找不到指定行程")
    
    # 非同步處理PDF生成
    background_tasks.add_task(
        process_memory_generation, 
        request.title, 
        request.trip_id, 
        request.user_id, 
        request.style
    )
    
    return {"status": "processing", "message": "回憶錄生成中，完成後會通知您"}

async def process_memory_generation(title: str, trip_id: str, user_id: str, style: str):
    try:
        temp_dir = tempfile.mkdtemp()
        
        # 從 Firebase 獲取行程資訊
        trip_doc = db.collection('trips').document(trip_id).get()
        trip_data = trip_doc.to_dict()
        start_date = trip_data.get('start_date')
        end_date = trip_data.get('end_date')
        
        # 計算行程天數
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days + 1
        
        # 直接按照天數分組獲取照片
        photo_groups = {}
        total_photos = 0
        
        for day in range(1, days + 1):
            day_id = f'day{day}'
            photos_ref = db.collection('trips').document(trip_id).collection('albums').document(day_id).collection('photos').order_by('timestamp').get()
            
            photos_for_day = []
            for photo in photos_ref:
                photo_data = photo.to_dict()
                photo_url = photo_data.get('url')
                
                if photo_url:
                    try:
                        # 改進的 URL 處理方式
                        if photo_url.startswith('gs://'):
                            # 直接使用 gs:// 路徑
                            blob_path = photo_url.replace(f'gs://{bucket.name}/', '')
                        else:
                            # 對於 HTTPS URL，使用更可靠的方法提取路徑
                            url_parts = photo_url.split('/')
                            if 'firebasestorage.googleapis.com' in photo_url:
                                # 提取標準 Firebase Storage URL 路徑
                                obj_path = url_parts[-1].split('?')[0]
                                blob_path = f"trips/{trip_id}/albums/{day_id}/{obj_path}"
                            else:
                                # 回退方案
                                blob_path = f"trips/{trip_id}/albums/{day_id}/{url_parts[-1]}"
                        
                        # 嘗試獲取 blob
                        blob = bucket.blob(blob_path)
                        
                        filename = f"{uuid.uuid4().hex}.jpg"
                        local_path = os.path.join(temp_dir, filename)
                        blob.download_to_filename(local_path)
                        photos_for_day.append(local_path)
                        total_photos += 1
                    except Exception as e:
                        print(f"下載照片時出錯: {e}, URL: {photo_url}")
            
            if photos_for_day:  # 只添加有照片的日期
                photo_groups[day] = photos_for_day
        
        if total_photos == 0:
            raise Exception("此行程沒有關聯的照片")
        
        # 生成 PDF
        output_dir = tempfile.mkdtemp()
        generate_pdf(title, photo_groups, style=style, output_dir=output_dir)
        
        # 上傳生成的 PDF
        pdf_filename = f"{title}_{style}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        # 上傳 PDF 到 Firebase Storage
        pdf_blob = bucket.blob(f"memories/{user_id}/{pdf_filename}")
        pdf_blob.upload_from_filename(pdf_path)
        pdf_url = f"gs://{bucket.name}/memories/{user_id}/{pdf_filename}"
        
        # 將記錄保存到 Firestore
        memory_doc = db.collection('memories').add({
            'title': title,
            'trip_id': trip_id,
            'user_id': user_id,
            'style': style,
            'pdf_url': pdf_url,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        
        # 添加通知
        db.collection('users').document(user_id).collection('notifications').add({
            'type': 'memory_generated',
            'title': f'您的"{title}"回憶錄已生成完成',
            'message': f'您的旅行回憶錄已準備好，請點擊查看',
            'pdf_url': pdf_url,
            'created_at': firestore.SERVER_TIMESTAMP,
            'read': False
        })
        
        # 清理臨時文件
        for day_photos in photo_groups.values():
            for file in day_photos:
                if os.path.exists(file):
                    os.remove(file)
        os.remove(pdf_path)
        
    except Exception as e:
        print(f"處理回憶錄生成時出錯: {e}")
        # 添加錯誤通知
        if user_id:
            db.collection('users').document(user_id).collection('notifications').add({
                'type': 'memory_error',
                'title': '回憶錄生成失敗',
                'message': f'生成"{title}"時遇到問題: {str(e)}',
                'created_at': firestore.SERVER_TIMESTAMP,
                'read': False
            })

# 啟動服務
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)