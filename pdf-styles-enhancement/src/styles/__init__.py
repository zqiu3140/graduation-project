import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from styles.classic_style import ClassicStyle
from styles.modern_style import ModernStyle
from styles.vintage_style import VintageStyle
from styles.minimalist_style import MinimalistStyle
from styles.artistic_style import ArtisticStyle
from styles.nature_style import NatureStyle
from styles.cinematic_style import CinematicStyle
from styles.seasonal_style import SeasonalStyle
from styles.tech_style import TechStyle
from styles.travel_style import TravelStyle


def generate_pdf(title, photo_groups, style="classic", output_dir=None):
    """
    生成 PDF 旅遊回憶錄
    
    參數:
    title (str): 回憶錄標題
    photo_groups (dict): 按天分組的照片列表
    style (str): 設計風格 - "classic", "modern" 或 "vintage"
    output_dir (str): 輸出目錄路徑，如果為 None，則使用當前目錄
    """
    
    page_width, page_height = 11 * inch, 8.5 * inch
    
    # 確保輸出目錄存在
    if output_dir is None:
        # 如果沒有指定，則使用專案的 result 目錄
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
        output_dir = os.path.join(root_dir, 'result')
    
    # 創建完整輸出路徑
    output_file = os.path.join(output_dir, f"{title}_{style}.pdf")
    c = canvas.Canvas(output_file,pagesize=(page_width, page_height))
    # 註冊字型
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    font_path = os.path.join(root_dir, 'resources', 'fonts', 'Chinese.ttf')
    pdfmetrics.registerFont(TTFont('Myfont', font_path))
    
# 選擇風格
    if style == "classic":
        styler = ClassicStyle()
    elif style == "modern":
        styler = ModernStyle()
    elif style == "vintage":
        styler = VintageStyle()
    elif style == "minimalist":
        styler = MinimalistStyle()
    elif style == "artistic":
        styler = ArtisticStyle()
    elif style == "nature":
        styler = NatureStyle()
    elif style == "cinematic":
        styler = CinematicStyle()
    elif style == "seasonal":
        styler = SeasonalStyle()
    elif style == "tech":
        styler = TechStyle()
    elif style == "travel":
        styler = TravelStyle()
    else:
        styler = ClassicStyle()  # 預設風格
    
    # 創建封面
    styler.create_cover_page(c, title, page_width, page_height)
    
    # 頁碼計數
    page_number = 1
    
    # 頁面邊距設置
    margin_left = 0.75 * inch
    margin_right = 0.75 * inch
    margin_top = 2 * inch
    margin_bottom = 0.75 * inch
    
    # 計算可用空間
    usable_width = page_width - margin_left - margin_right
    usable_height = page_height - margin_top - margin_bottom
    
    # 計算網格大小（2x2 網格）
    grid_width = usable_width / 2
    grid_height = usable_height / 2
    
    # 設定照片大小（保持一定的邊距）
    inner_margin = 0.1 * inch
    photo_width = grid_width - 2 * inner_margin
    photo_height = grid_height - 2 * inner_margin
    
    page_number += 1
    
    for day in sorted(photo_groups.keys()):
        photos = photo_groups[day]
        num_photos = len(photos)
        
        # 每頁照片數可以根據風格略有不同
        photos_per_page = styler.photos_per_page
        num_pages = (num_photos + photos_per_page - 1) // photos_per_page

        for page in range(num_pages):
            c.showPage()  # 開始新的一頁
            
            # 應用頁面樣式
            styler.apply_page_style(c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom)
            
            # 添加頁面標題和說明
            styler.add_page_header(c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left)
            
            # 計算當前頁面的照片範圍
            start_index = page * photos_per_page
            end_index = min((page + 1) * photos_per_page, num_photos)

            # 放置照片
            for i in range(start_index, end_index):
                # 計算照片在當前頁面的索引
                photo_index = i - start_index
                
                # 獲取照片佈局位置
                x, y, current_photo_width, current_photo_height = styler.get_photo_position(
                    photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width, usable_height, page_width, margin_right, margin_bottom)

                try:
                    c.saveState()  # 保存當前狀態
                    # 繪製照片邊框和裝飾
                    styler.draw_photo_frame(c, x, y, current_photo_width, current_photo_height)
                    # 獲取照片檔名（不含路徑）作為可能的標題
                    photo_filename = os.path.basename(photos[i])
                    photo_title = os.path.splitext(photo_filename)[0]
                    c.setFillColorRGB(1,1,1,1.0) # 確保填充顏色為白色
                    c.drawImage(
                        photos[i], 
                        x + styler.frame_padding, 
                        y + styler.frame_padding+15,
                        width=current_photo_width - 2*styler.frame_padding, 
                        height=current_photo_height - styler.frame_padding - styler.caption_height,
                        preserveAspectRatio=True,
                        anchor='c'
                    )                     
                    # 繪製照片 - 確保高品質渲染
                    
                    # 添加照片標題
                    
                    styler.add_photo_caption(c, photo_title, x, y, current_photo_width, current_photo_height)
                    c.restoreState()  # 恢復狀態
    
                except Exception as e:
                    print(f"錯誤：無法載入圖片 {photos[i]}: {e}")
                    # 繪製錯誤預留位置
                    styler.draw_error_placeholder(c, x, y, current_photo_width, current_photo_height, photo_title)
            
            # 添加頁腳和頁碼
            styler.add_footer(c, page_number, page_width, page_height, margin_bottom, day)
            page_number += 1
    
    # 添加後記頁
    styler.add_epilogue_page(c, title, page_width, page_height)
    
    c.save()
    print(f"已生成 {style} 風格的 PDF: {title}_{style}.pdf")
