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

app = FastAPI()

# 初始化Firebase (您需要提供自己的憑證檔案)
cred = credentials.Certificate("../key/g-project-60175-firebase-adminsdk-fbsvc-2d2703fd7f.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'g-project-60175.firebasestorage.app'
})
db = firestore.client()
bucket = storage.bucket()

class MemoryRequest(BaseModel):
    title: str
    trip_id: str
    user_id: str
    style: str = "classic"
    
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
            # 為每天的照片添加計數器
            photo_counter = 1
            
            for photo in photos_ref:
                photo_data = photo.to_dict()
                photo_url = photo_data.get('url')
                
                if photo_url:
                    try:
                        # 加入調試信息
                        print(f"正在處理照片 URL: {photo_url}")
                        
                        # 改進的 URL 處理方式
                        if photo_url.startswith('gs://'):
                            # 直接使用 gs:// 路徑
                            blob_path = photo_url.replace(f'gs://{bucket.name}/', '')
                            print(f"使用 gs:// 路徑: {blob_path}")
                        else:
                            # 更精確地解析 Firebase Storage URL
                            if 'firebasestorage.googleapis.com' in photo_url:
                                # 從 URL 中提取完整路徑
                                # 查找 '/o/' 後面的內容直到 '?'
                                path_start = photo_url.find('/o/') + 3
                                path_end = photo_url.find('?', path_start) if '?' in photo_url else len(photo_url)
                                encoded_path = photo_url[path_start:path_end]
                                
                                # URL 解碼
                                import urllib.parse
                                decoded_path = urllib.parse.unquote(encoded_path)
                                blob_path = decoded_path
                                
                                print(f"從 Firebase URL 提取的路徑: {blob_path}")
                            else:
                                # 回退方案
                                url_parts = photo_url.split('/')
                                blob_path = f"trips/{trip_id}/albums/{day_id}/{url_parts[-1]}"
                                print(f"使用回退方案路徑: {blob_path}")
                        
                        # 嘗試獲取 blob
                        print(f"正在獲取 blob: {blob_path}")
                        blob = bucket.blob(blob_path)
                        
                        # 使用 Day{day}_{photo_counter} 格式命名
                        filename = f"Day{day}_{photo_counter}.jpg"
                        local_path = os.path.join(temp_dir, filename)
                        print(f"準備下載到臨時路徑: {local_path}")
                        blob.download_to_filename(local_path)
                        print(f"成功下載照片：{filename}")
                        photos_for_day.append(local_path)
                        total_photos += 1
                        # 增加照片計數器
                        photo_counter += 1
                    except Exception as e:
                        print(f"下載照片時出錯: {e}, URL: {photo_url}")
            
            if photos_for_day:  # 只添加有照片的日期
                photo_groups[day] = photos_for_day
        
        if total_photos == 0:
            print(f"處理完成，總共找到 {total_photos} 張照片")
            print(f"照片分組情況: {', '.join([f'第{d}天: {len(ps)}張' for d, ps in photo_groups.items()])}")
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