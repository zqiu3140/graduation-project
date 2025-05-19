import os
import math
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
from reportlab.pdfgen.pathobject import PDFPathObject

class NatureStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        # 更豐富的自然色彩方案
        self.main_color = (0.2, 0.5, 0.3)  # 森林綠
        self.accent_color = (0.6, 0.4, 0.2)  # 泥土棕
        self.text_color = (0.1, 0.3, 0.1)  # 深綠
        self.bg_color = (0.95, 0.98, 0.95)  # 淺綠白
        self.leaf_color = (0.3, 0.6, 0.25)  # 葉綠
        self.wood_color = (0.5, 0.35, 0.2)  # 木材色
        self.flower_color = (0.9, 0.7, 0.8)  # 花朵粉色
        self.water_color = (0.2, 0.4, 0.7)  # 水藍色
        
        # 降低每頁照片數量，讓照片更大更突出
        self.photos_per_page = 2

    def create_cover_page(self, c, title, page_width, page_height):
        """創建更具層次感的自然風格封面"""
        # 漸變背景效果 - 模擬自然光線
        steps = 100
        for i in range(steps):
            y = i * (page_height/steps)
            height = page_height/steps
            # 由深到淺的漸變，模擬自然日光
            intensity = 0.95 - (i / steps) * 0.3
            # 略微加入黃色調，更像自然光照
            c.setFillColorRGB(intensity*0.95, intensity*0.98, intensity*0.85)
            c.rect(0, y, page_width, height, fill=True, stroke=False)
    
        # 左側裝飾條 - 樹幹效果
        sidebar_width = 2.5 * inch
        c.setFillColorRGB(*self.wood_color, 0.8)
        c.rect(0, 0, sidebar_width, page_height, fill=True, stroke=False)
        
        # 樹皮紋理效果
        c.setStrokeColorRGB(0.3, 0.2, 0.1, 0.2)
        for i in range(40):
            x1 = random.uniform(0.2*inch, 2.3*inch)
            y1 = random.uniform(0, page_height)
            length = random.uniform(0.3, 1.5) * inch
            c.setLineWidth(random.uniform(0.5, 2.0))
            c.line(x1, y1, x1 + random.uniform(-0.1, 0.1)*inch, y1 + length)
    
        # 在整個頁面右側繪製藤蔓和葉子裝飾
        self.draw_vines_and_leaves(c, sidebar_width*0.9, 0, page_width-sidebar_width*0.9, page_height)
    
        # 標題背景 - 自然葉形框架
        title_x = sidebar_width + 0.4*inch
        title_y = page_height/2 - 0.5*inch
        title_width = 5 * inch
        title_height = 3 * inch
        
        # 柔和的背景光暈 - 模擬森林中的光斑
        c.setFillColorRGB(1, 1, 0.9, 0.2)
        for i in range(20):
            glow_x = title_x + random.uniform(0, title_width)
            glow_y = title_y + random.uniform(0, title_height)
            glow_size = random.uniform(0.5, 1.5) * inch
            c.circle(glow_x, glow_y, glow_size, fill=True, stroke=False)
        
        # 主標題 - 使用更有自然感的字體大小和位置
        c.setFont('Myfont', 48)
        c.setFillColorRGB(0.1, 0.3, 0.1, 0.95)  # 較深的綠色，接近完全不透明
        main_title = "自然之旅"
        main_width = pdfmetrics.stringWidth(main_title, 'Myfont', 48)
        c.drawString(title_x + (title_width - main_width)/2, title_y + 1.5*inch, main_title)
    
        # 裝飾分隔線 - 模擬樹枝
        c.setStrokeColorRGB(*self.wood_color, 0.8)
        c.setLineWidth(3)
        branch_width = main_width * 1.2
        # 不是直線而是略微彎曲的樹枝
        p = PDFPathObject()
        p.moveTo(title_x + (title_width - branch_width)/2, title_y + 1.3*inch)
        p.curveTo(
            title_x + (title_width - branch_width)/2 + branch_width*0.25, title_y + 1.25*inch,
            title_x + (title_width - branch_width)/2 + branch_width*0.75, title_y + 1.35*inch,
            title_x + (title_width - branch_width)/2 + branch_width, title_y + 1.3*inch
        )
        c.drawPath(p, stroke=1, fill=0)
        
        # 副標題 - 使用優雅的字體和位置
        c.setFont('Myfont', 32)
        c.setFillColorRGB(*self.text_color, 1.0)  # 確保完全不透明
        subtitle = title
        sub_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 32)
        c.drawString(title_x + (title_width - sub_width)/2, title_y + 0.5*inch, subtitle)
        
        # 底部自然元素 - 草地輪廓
        self.draw_grass_silhouette(c, 0, 0, page_width, 1.2*inch)
        
        # 日期和簽名 - 放在像手寫的位置上
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color, 0.9)
        date_text = f"製作於 {datetime.now().strftime('%Y年%m月%d日')}"
        c.drawString(page_width - 2.5*inch, 0.8*inch, date_text)

    def draw_vines_and_leaves(self, c, x, y, width, height):
        """繪製藤蔓和葉子裝飾"""
        c.saveState()
        # 設定藤蔓和葉子的顏色和線寬
        c.setStrokeColorRGB(*self.accent_color, 0.5)
        c.setLineWidth(1.0)
        
        # 繪製幾條主藤蔓
        vine_count = random.randint(3, 5)
        for v in range(vine_count):
            # 主藤蔓起點
            start_x = x + random.uniform(0, width*0.3)
            start_y = y + random.uniform(0, height*0.1)
            
            # 藤蔓曲線控制點
            points = [(start_x, start_y)]
            segment_count = random.randint(5, 8)
            for i in range(segment_count):
                next_x = start_x + (i+1) * width / segment_count * random.uniform(0.8, 1.2)
                next_y = start_y + height * random.uniform(0.1, 0.9)
                points.append((next_x, next_y))
            
            # 繪製藤蔓
            p = PDFPathObject()
            p.moveTo(points[0][0], points[0][1])
            for i in range(1, len(points)):
                p.lineTo(points[i][0], points[i][1])
            c.drawPath(p, stroke=1, fill=0)
            
            # 在藤蔓上添加葉子
            for i in range(1, len(points)):
                if random.random() < 0.7:  # 不是每個段都有葉子
                    leaf_x = points[i][0]
                    leaf_y = points[i][1]
                    size = random.uniform(0.2, 0.4) * inch
                    self.draw_leaf(c, leaf_x, leaf_y, size, random.uniform(0, 360))
        
        # 添加一些隨機分布的小花
        flower_count = random.randint(5, 8)
        for _ in range(flower_count):
            flower_x = x + random.uniform(width*0.2, width*0.9)
            flower_y = y + random.uniform(height*0.1, height*0.9)
            self.draw_flower(c, flower_x, flower_y, random.uniform(0.15, 0.25)*inch)
        
        c.restoreState()
        
    def draw_leaf(self, c, x, y, size, angle):
        """繪製自然風格的葉子"""
        c.saveState()
        c.translate(x, y)
        c.rotate(angle)
        
        # 葉子填充
        c.setFillColorRGB(*self.leaf_color, random.uniform(0.3, 0.5))
        
        # 葉子邊緣
        c.setStrokeColorRGB(*self.text_color, 0.3)
        c.setLineWidth(0.5)
        
        # 繪製簡單的葉形
        p = PDFPathObject()
        p.moveTo(0, 0)
        p.curveTo(size*0.3, size*0.5, size*0.7, size*0.5, size, 0)
        p.curveTo(size*0.7, -size*0.5, size*0.3, -size*0.5, 0, 0)
        c.drawPath(p, stroke=1, fill=1)
        
        # 葉脈
        c.setStrokeColorRGB(*self.text_color, 0.2)
        c.setLineWidth(0.3)
        c.line(0, 0, size, 0)
        
        # 次級脈絡
        vein_count = random.randint(3, 5)
        for i in range(vein_count):
            ratio = (i+1) / (vein_count+1)
            length = size * ratio * 0.8
            angle = 30 - 60 * ratio
            # 兩側的葉脈
            c.line(size*ratio, 0, size*ratio+length*0.3*math.cos(math.radians(angle)), length*math.sin(math.radians(angle)))
            c.line(size*ratio, 0, size*ratio+length*0.3*math.cos(math.radians(-angle)), length*math.sin(math.radians(-angle)))
        
        c.restoreState()
        
    def draw_flower(self, c, x, y, size):
        """繪製簡單的花朵"""
        c.saveState()
        # 花瓣
        c.setFillColorRGB(*self.flower_color, random.uniform(0.5, 0.7))
        petal_count = 5
        for i in range(petal_count):
            angle = i * (360/petal_count)
            c.saveState()
            c.translate(x, y)
            c.rotate(angle)
            # 橢圓形花瓣
            p = PDFPathObject()
            p.moveTo(0, 0)
            p.curveTo(size*0.3, size*0.2, size*0.7, size*0.2, size, 0)
            p.curveTo(size*0.7, -size*0.2, size*0.3, -size*0.2, 0, 0)
            c.drawPath(p, stroke=0, fill=1)
            c.restoreState()
        
        # 花蕊
        c.setFillColorRGB(0.9, 0.8, 0.2, 0.8)
        c.circle(x, y, size*0.15, fill=True, stroke=False)
        
        c.restoreState()

    def draw_grass_silhouette(self, c, x, y, width, height):
        """繪製草地輪廓"""
        c.saveState()
        c.setFillColorRGB(*self.main_color, 0.3)
        
        # 繪製起伏的草地
        grass_segments = 100
        points = []
        for i in range(grass_segments + 1):
            segment_x = x + i * (width / grass_segments)
            # 基礎高度加上隨機波動
            segment_y = y + height * random.uniform(0.1, 0.3)
            points.append((segment_x, segment_y))
        
        # 繪製基本形狀
        p = PDFPathObject()
        p.moveTo(x, y)
        p.lineTo(points[0][0], points[0][1])
        for i in range(1, len(points)):
            p.lineTo(points[i][0], points[i][1])
        p.lineTo(x + width, y)
        p.lineTo(x, y)
        c.drawPath(p, stroke=0, fill=1)
        
        # 添加一些草葉
        for i in range(0, len(points), 3):
            base_x = points[i][0]
            base_y = points[i][1]
            
            # 隨機草葉
            blade_count = random.randint(1, 3)
            for j in range(blade_count):
                height_factor = random.uniform(0.5, 1.2)
                c.setStrokeColorRGB(*self.main_color, random.uniform(0.6, 0.9))
                c.setLineWidth(random.uniform(0.5, 1.5))
                
                # 彎曲的草葉
                p = PDFPathObject()
                p.moveTo(base_x, base_y)
                blade_height = height * height_factor * 0.3
                control_x = base_x + random.uniform(-0.1, 0.1) * inch
                p.curveTo(
                    base_x + random.uniform(-0.05, 0.05) * inch, base_y + blade_height * 0.3,
                    control_x, base_y + blade_height * 0.6,
                    control_x, base_y + blade_height
                )
                c.drawPath(p, stroke=1, fill=0)
        
        c.restoreState()

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用自然風格頁面背景"""
        # 基礎背景，略帶紙張質感
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 紙張質感效果
        for _ in range(1000):
            x = random.uniform(0, page_width)
            y = random.uniform(0, page_height)
            size = random.uniform(0.01, 0.03) * inch
            intensity = random.uniform(0.02, 0.05)
            c.setFillColorRGB(0.8, 0.8, 0.75, intensity)
            c.circle(x, y, size, fill=True, stroke=False)
        
        # 頁眉背景 - 漸變森林感
        c.saveState()
        header_height = margin_top * 1.2
        for i in range(20):
            y = page_height - header_height + i * (header_height / 20)
            height = header_height / 20
            
            # 由深到淺的綠色漸變
            intensity = 0.3 - (i / 20) * 0.2
            c.setFillColorRGB(self.main_color[0], self.main_color[1], self.main_color[2], intensity)
            c.rect(0, y, page_width, height, fill=True, stroke=False)
        
        # 頁眉裝飾 - 簡單樹葉輪廓
        leaf_count = random.randint(5, 8)
        for _ in range(leaf_count):
            leaf_x = random.uniform(margin_left*0.5, page_width-margin_right*0.5)
            leaf_y = page_height - random.uniform(0, header_height*0.8)
            self.draw_leaf(c, leaf_x, leaf_y, random.uniform(0.2, 0.4)*inch, random.uniform(0, 360))
        
        # 頁腳區域 - 簡單草地效果
        c.setFillColorRGB(*self.main_color, 0.1)
        c.rect(0, 0, page_width, margin_bottom * 0.8, fill=True, stroke=False)
        
        # 角落裝飾 - 藤蔓效果
        corner_size = 1.5 * inch
        # 左下角藤蔓
        self.draw_corner_vine(c, margin_left*0.3, margin_bottom*0.3, corner_size, 45)
        # 右下角藤蔓
        self.draw_corner_vine(c, page_width-margin_right*0.3, margin_bottom*0.3, corner_size, 135)
        
        c.restoreState()
    
    def draw_corner_vine(self, c, x, y, size, angle):
        """繪製角落藤蔓裝飾"""
        c.saveState()
        c.translate(x, y)
        c.rotate(angle)
        
        # 主藤蔓
        c.setStrokeColorRGB(*self.accent_color, 0.6)
        c.setLineWidth(1.2)
        
        # 彎曲的藤蔓
        p = PDFPathObject()
        p.moveTo(0, 0)
        p.curveTo(
            size*0.3, size*0.1,
            size*0.7, size*0.3,
            size, size
        )
        c.drawPath(p, stroke=1, fill=0)
        
        # 添加幾片葉子
        leaf_positions = [0.3, 0.6, 0.9]
        for pos in leaf_positions:
            if random.random() < 0.7:
                # 計算藤蔓上的點位置
                curve_x = pos * size
                curve_y = pos * pos * size
                # 繪製葉子
                leaf_size = size * 0.25 * random.uniform(0.8, 1.2)
                leaf_angle = random.uniform(-30, 30)
                c.saveState()
                c.translate(curve_x, curve_y)
                c.rotate(leaf_angle)
                self.draw_leaf(c, 0, 0, leaf_size, 0)
                c.restoreState()
        
        c.restoreState()

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """添加自然風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch
        
        # 標題文字
        c.setFont('Myfont', 22)
        c.setFillColorRGB(1, 1, 1, 1.0)  # 確保完全不透明
        header_text = f"{title} - 第 {day} 天"
        c.drawString(margin_left, header_y, header_text)
        
        # 右側頁碼指示
        c.setFont('Myfont', 14)
        c.setFillColorRGB(1, 1, 1, 0.9)
        page_text = f"{page + 1}/{num_pages}"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        
        # 頁碼背景 - 葉子形狀
        leaf_x = page_width - margin_left - text_width - 0.3*inch
        leaf_y = header_y - 0.1*inch
        leaf_size = 0.8 * inch
        c.saveState()
        c.setFillColorRGB(*self.leaf_color, 0.3)
        c.translate(leaf_x, leaf_y)
        
        # 橢圓形葉子背景
        p = PDFPathObject()
        p.moveTo(0, 0)
        p.curveTo(leaf_size*0.4, leaf_size*0.3, leaf_size*0.8, leaf_size*0.3, leaf_size, 0)
        p.curveTo(leaf_size*0.8, -leaf_size*0.3, leaf_size*0.4, -leaf_size*0.3, 0, 0)
        c.drawPath(p, stroke=0, fill=1)
        c.restoreState()
        
        # 繪製頁碼
        c.drawRightString(page_width - margin_left, header_y, page_text)

    def get_photo_position(self, photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width=None, usable_height=None, page_width=None, margin_right=None, margin_bottom=None):
        """自然風格照片位置 - 均勻佈局"""
        # 確保使用完整寬度
        if usable_width is None:
            usable_width = grid_width * 2
        
        # 計算每張照片的標準尺寸
        photo_width = (usable_width - inner_margin * 3) / 2  # 減去邊距，然後平均分配給兩張照片
        photo_height = grid_height - inner_margin * 2 - self.caption_height+100
        
        # 根據照片索引決定位置 (水平排列)
        if photo_index % 2 == 0:  # 第一張照片 - 左側
            x = margin_left + inner_margin
            y = page_height - margin_top - grid_height + inner_margin-150
        else:  # 第二張照片 - 右側
            x = margin_left + photo_width + inner_margin * 2
            y = page_height - margin_top - grid_height + inner_margin-150
        
        # 添加輕微隨機偏移 - 保持自然感，但不影響整體佈局
        offset = 0.03 * inch  # 減小偏移量，確保不破壞整體對齊
        x += random.uniform(-offset, offset)
        y += random.uniform(-offset, offset)
        
        return x, y, photo_width, photo_height

    def draw_photo_frame(self, c, x, y, width, height):
        """繪製自然風格照片邊框"""
        c.saveState()
        
        # 略微的陰影效果
        shadow_offset = 0.08 * inch
        c.setFillColorRGB(0.3, 0.3, 0.3, 0.2)
        c.rect(x + shadow_offset, y - shadow_offset, width, height, fill=True, stroke=False)
        
        # 照片底色
        c.setFillColorRGB(1, 1, 1, 1.0)
        c.rect(x, y, width, height, fill=True, stroke=False)
        
        # 自然材質邊框 - 模擬木質相框
        frame_width = 0.12 * inch
        
        # 木質紋理邊框
        c.setFillColorRGB(*self.wood_color, 0.85)
        # 上邊框
        c.rect(x-frame_width, y+height, width+2*frame_width, frame_width, fill=True, stroke=False)
        # 右邊框
        c.rect(x+width, y-frame_width, frame_width, height+2*frame_width, fill=True, stroke=False)
        # 下邊框
        c.rect(x-frame_width, y-frame_width, width+2*frame_width, frame_width, fill=True, stroke=False)
        # 左邊框
        c.rect(x-frame_width, y-frame_width, frame_width, height+2*frame_width, fill=True, stroke=False)
        
        # 添加木質紋理
        c.setStrokeColorRGB(0.3, 0.2, 0.1, 0.1)
        c.setLineWidth(0.3)
        
        # 水平紋理
        grain_count = int(width / (0.1 * inch))
        for i in range(grain_count):
            grain_x = x + i * (width / grain_count)
            c.line(grain_x, y-frame_width, grain_x, y+height+frame_width)
        
        # 角落裝飾 - 葉子
        corner_size = 0.25 * inch
        corners = [
            (x-frame_width/2, y-frame_width/2), 
            (x+width+frame_width/2, y-frame_width/2),
            (x-frame_width/2, y+height+frame_width/2), 
            (x+width+frame_width/2, y+height+frame_width/2)
        ]
        
        for i, (cx, cy) in enumerate(corners):
            angle = i * 90
            self.draw_leaf(c, cx, cy, corner_size, angle)
        
        c.restoreState()

    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加自然風格照片標題"""
        if len(caption) > 20:
            caption = caption[:17] + "..."
        
        c.saveState()
        
        # 標題背景 - 模擬樹皮質感
        c.setFillColorRGB(*self.wood_color, 0.4)
        caption_height = self.caption_height - 0.05*inch
        c.roundRect(x, y, width, caption_height, radius=0.05*inch, fill=True, stroke=False)
        
        # 木質紋理背景
        grain_count = 20
        c.setStrokeColorRGB(0.3, 0.2, 0.1, 0.07)
        for i in range(grain_count):
            y_pos = y + i * (caption_height / grain_count)
            variation = random.uniform(-0.01, 0.01) * inch
            c.setLineWidth(random.uniform(0.2, 0.7))
            c.line(x, y_pos + variation, x + width, y_pos + variation)
        
        # 標題文字 - 模擬手寫風格
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1, 1.0)  # 白色文字，確保不透明
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        
        # 輕微的旋轉效果
        c.saveState()
        c.translate(x + width/2, y + 0.12*inch)
        rotation = random.uniform(-1, 1)
        c.rotate(rotation)
        c.drawString(-text_width/2, 0, caption)
        c.restoreState()
        
        # 小葉子裝飾
        if random.random() < 0.5:  # 50%機率添加裝飾
            leaf_x = x + random.choice([0.1*inch, width-0.1*inch])
            leaf_y = y + caption_height * 0.8
            leaf_size = 0.15 * inch
            self.draw_leaf(c, leaf_x, leaf_y, leaf_size, random.uniform(0, 360))
        
        c.restoreState()

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加自然風格頁腳"""
        footer_y = margin_bottom / 2
        
        c.saveState()
        
        # 簡單的草地效果作為背景
        grass_height = margin_bottom * 0.5
        self.draw_grass_silhouette(c, 0, 0, page_width, grass_height)
        
        # 頁碼文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color, 1.0)  # 確保不透明
        page_text = f"第 {page_number} 頁"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        
        # 頁碼背景 - 樹葉形狀
        bg_x = (page_width - text_width) / 2 - 0.2*inch
        bg_y = footer_y - 0.1*inch
        bg_width = text_width + 0.4*inch
        bg_height = 0.3*inch
        
        # 橢圓葉子形背景
        c.setFillColorRGB(*self.main_color, 0.3)
        c.roundRect(bg_x, bg_y, bg_width, bg_height, radius=0.1*inch, fill=True, stroke=False)
        
        # 頁碼文字
        c.drawString((page_width - text_width)/2, footer_y, page_text)
        
        # 日期裝飾
        c.setFont('Myfont', 9)
        date_text = datetime.now().strftime('%Y年%m月%d日')
        date_width = pdfmetrics.stringWidth(date_text, 'Myfont', 9)
        c.drawString(page_width - margin_bottom - date_width, 0.2*inch, date_text)
        
        # 某些頁可能隨機添加小動物剪影
        if random.random() < 0.2:  # 20%幾率
            self.draw_animal_silhouette(c, random.uniform(1*inch, page_width-1*inch), 0.4*inch)
        
        c.restoreState()
    
    def draw_animal_silhouette(self, c, x, y):
        """繪製簡單的動物剪影"""
        c.saveState()
        c.setFillColorRGB(0.1, 0.1, 0.1, 0.6)
        
        # 隨機選擇動物類型
        animal_type = random.choice(["rabbit", "bird", "squirrel"])
        
        if animal_type == "rabbit":
            # 兔子剪影
            size = 0.3 * inch
            # 身體
            c.ellipse(x-size*0.5, y-size*0.3, x+size*0.5, y+size*0.3, fill=True, stroke=False)
            # 頭部
            c.circle(x+size*0.6, y+size*0.2, size*0.25, fill=True, stroke=False)
            # 耳朵
            p = PDFPathObject()
            p.moveTo(x+size*0.5, y+size*0.3)
            p.curveTo(x+size*0.6, y+size*0.8, x+size*0.8, y+size*0.8, x+size*0.7, y+size*0.3)
            p.lineTo(x+size*0.5, y+size*0.3)
            c.drawPath(p, stroke=0, fill=1)
            
            p = PDFPathObject()
            p.moveTo(x+size*0.7, y+size*0.3)
            p.curveTo(x+size*0.8, y+size*0.7, x+size*1.0, y+size*0.7, x+size*0.9, y+size*0.3)
            p.lineTo(x+size*0.7, y+size*0.3)
            c.drawPath(p, stroke=0, fill=1)
            
        elif animal_type == "bird":
            # 鳥剪影
            size = 0.25 * inch
            # 身體
            c.ellipse(x-size*0.6, y-size*0.3, x+size*0.6, y+size*0.3, fill=True, stroke=False)
            # 頭部
            c.circle(x+size*0.6, y+size*0.3, size*0.25, fill=True, stroke=False)
            # 尾巴
            p = PDFPathObject()
            p.moveTo(x-size*0.6, y)
            p.curveTo(x-size*1.0, y+size*0.4, x-size*1.2, y-size*0.4, x-size*0.6, y-size*0.2)
            p.lineTo(x-size*0.6, y)
            c.drawPath(p, stroke=0, fill=1)
            # 喙
            p = PDFPathObject()
            p.moveTo(x+size*0.8, y+size*0.3)
            p.lineTo(x+size*1.1, y+size*0.4)
            p.lineTo(x+size*0.8, y+size*0.2)
            p.lineTo(x+size*0.8, y+size*0.3)
            c.drawPath(p, stroke=0, fill=1)
            
        else:  # squirrel
            # 松鼠剪影
            size = 0.3 * inch
            # 身體
            c.ellipse(x-size*0.3, y-size*0.5, x+size*0.3, y+size*0.2, fill=True, stroke=False)
            # 頭部
            c.circle(x, y+size*0.4, size*0.25, fill=True, stroke=False)
            # 尾巴
            p = PDFPathObject()
            p.moveTo(x-size*0.1, y-size*0.4)
            p.curveTo(x-size*0.8, y-size*0.2, x-size*0.7, y+size*0.6, x-size*0.2, y+size*0.2)
            p.curveTo(x-size*0.3, y+size*0.1, x-size*0.2, y-size*0.3, x-size*0.1, y-size*0.4)
            c.drawPath(p, stroke=0, fill=1)
        
        c.restoreState()

    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加自然風格後記頁"""
        c.showPage()
        
        # 自然漸變背景 - 模擬日落
        steps = 100
        for i in range(steps):
            y = i * (page_height/steps)
            height = page_height/steps
            # 自上而下漸變，模擬天空到地面的過渡
            ratio = i / steps
            if ratio < 0.6:  # 天空部分 - 從淡藍到黃昏色
                r = 0.7 + ratio * 0.3
                g = 0.8 + ratio * 0.1
                b = 0.9 - ratio * 0.4
            else:  # 地面部分 - 漸變到綠色
                new_ratio = (ratio - 0.6) / 0.4
                r = 0.7 - new_ratio * 0.4
                g = 0.8 - new_ratio * 0.3
                b = 0.5 - new_ratio * 0.3
            
            c.setFillColorRGB(r, g, b)
            c.rect(0, page_height-y-height, page_width, height, fill=True, stroke=False)
        
        # 山脈剪影
        self.draw_mountain_silhouette(c, 0, page_height*0.4, page_width, page_height*0.3)
        
        # 前景樹木剪影
        tree_count = random.randint(5, 8)
        for i in range(tree_count):
            x = i * (page_width / (tree_count-1))
            y = page_height * 0.4
            height = random.uniform(1.5, 3) * inch
            self.draw_tree_silhouette(c, x, y, height)
        
        # 裝飾性花邊框
        margin = 1 * inch
        c.setStrokeColorRGB(*self.main_color, 0.7)
        c.setLineWidth(2)
        c.rect(margin, margin, page_width-2*margin, page_height-2*margin, stroke=True, fill=False)
        
        # 每個角落添加葉子裝飾
        corner_size = 0.8 * inch
        c.saveState()
        
        # 左上角
        self.draw_leaf(c, margin, page_height-margin, corner_size, 45)
        # 右上角
        self.draw_leaf(c, page_width-margin, page_height-margin, corner_size, 135)
        # 左下角
        self.draw_leaf(c, margin, margin, corner_size, -45)
        # 右下角
        self.draw_leaf(c, page_width-margin, margin, corner_size, -135)
        c.restoreState()
        
        # 中央文字區域 - 模擬樹幹橫斷面
        center_y = page_height * 0.6
        title_box_width = 6 * inch
        title_box_height = 3 * inch
        title_box_x = (page_width - title_box_width) / 2
        title_box_y = center_y - title_box_height/2
        
        # 圓形木紋背景
        c.setFillColorRGB(*self.wood_color, 0.6)
        c.circle(page_width/2, center_y, title_box_width*0.4, fill=True, stroke=False)
        
        # 添加木紋年輪
        c.setStrokeColorRGB(0.3, 0.2, 0.1, 0.2)
        ring_count = 8
        for i in range(ring_count):
            radius = title_box_width * 0.4 * (1 - i/ring_count)
            c.setLineWidth(random.uniform(0.5, 1.5))
            c.circle(page_width/2, center_y, radius, fill=False, stroke=True)
        
        # 結束語標題
        c.setFont('Myfont', 42)
        c.setFillColorRGB(*self.bg_color, 0.9)  # 淺色文字對比木紋背景
        epilogue_text = "自然之旅結束"
        text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 42)
        c.drawString((page_width - text_width)/2, center_y + 0.5*inch, epilogue_text)
        
        # 副標題
        c.setFont('Myfont', 18)
        c.setFillColorRGB(*self.bg_color, 0.8)
        subtitle = f"{title} · 回憶永存"
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 18)
        c.drawString((page_width - text_width)/2, center_y - 0.5*inch, subtitle)
        
        # 日期
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.bg_color, 0.7)
        date_text = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        text_width = pdfmetrics.stringWidth(date_text, 'Myfont', 14)
        c.drawString((page_width - text_width)/2, center_y - 1*inch, date_text)
        
        # 底部草地
        self.draw_grass_silhouette(c, 0, 0, page_width, 2*inch)
    
    def draw_mountain_silhouette(self, c, x, y, width, height):
        """繪製山脈剪影"""
        c.saveState()
        c.setFillColorRGB(0.15, 0.25, 0.2, 0.7)
        
        # 主山脈
        peak_count = random.randint(3, 5)
        points = [(x, y)]
        
        for i in range(peak_count):
            # 計算每個山峰的位置
            peak_x = x + width * (i+1)/(peak_count+1)
            peak_y = y + height * random.uniform(0.7, 1.0)
            points.append((peak_x, peak_y))
            
            # 在主峰間添加小峰
            if i < peak_count-1:
                small_x = x + width * (i+1.5)/(peak_count+1)
                small_y = y + height * random.uniform(0.4, 0.7)
                points.append((small_x, small_y))
        
        points.append((x+width, y))
        
        # 繪製山脈
        p = PDFPathObject()
        p.moveTo(points[0][0], points[0][1])
        for px, py in points[1:]:
            p.lineTo(px, py)
        c.drawPath(p, stroke=0, fill=1)
        
        # 添加一層淺色山脈作為背景
        c.setFillColorRGB(0.2, 0.3, 0.25, 0.4)
        background_points = [(x, y)]
        bg_peak_count = random.randint(2, 4)
        
        for i in range(bg_peak_count):
            bg_x = x + width * (i+1)/(bg_peak_count+1)
            bg_y = y + height * random.uniform(0.3, 0.6)
            background_points.append((bg_x, bg_y))
        
        background_points.append((x+width, y))
        
        p = PDFPathObject()
        p.moveTo(background_points[0][0], background_points[0][1])
        for px, py in background_points[1:]:
            p.lineTo(px, py)
        c.drawPath(p, stroke=0, fill=1)
        
        c.restoreState()
    
    def draw_tree_silhouette(self, c, x, y, height):
        """繪製樹木剪影"""
        c.saveState()
        c.setFillColorRGB(0.1, 0.15, 0.1, 0.8)
        
        # 樹幹
        trunk_width = height * 0.06
        trunk_height = height * 0.4
        c.rect(x-trunk_width/2, y, trunk_width, trunk_height, fill=True, stroke=False)
        
        # 樹冠 - 根據樹的類型隨機選擇
        tree_type = random.choice(["pine", "broad", "round"])
        
        if tree_type == "pine":
            # 松樹形狀 - 三角形
            crown_width = height * 0.4
            crown_height = height * 0.6
            # 多層三角形樹冠
            layer_count = random.randint(3, 5)
            for i in range(layer_count):
                layer_y = y + trunk_height + (i/layer_count) * crown_height
                layer_width = crown_width * (1 - i/layer_count * 0.6)
                # 三角形
                p = PDFPathObject()
                p.moveTo(x, layer_y + crown_height/layer_count)
                p.lineTo(x - layer_width/2, layer_y)
                p.lineTo(x + layer_width/2, layer_y)
                p.lineTo(x, layer_y + crown_height/layer_count)
                c.drawPath(p, stroke=0, fill=1)
        
        elif tree_type == "broad":
            # 闊葉樹 - 不規則橢圓形
            crown_width = height * 0.6
            crown_height = height * 0.7
            # 主樹冠
            c.ellipse(x-crown_width/2, y+trunk_height, x+crown_width/2, y+trunk_height+crown_height, fill=True, stroke=False)
            # 一些不規則分支
            branch_count = random.randint(3, 5)
            for i in range(branch_count):
                branch_angle = random.uniform(0, 360)
                branch_x = x + math.cos(math.radians(branch_angle)) * crown_width * 0.3
                branch_y = y + trunk_height + crown_height * 0.6 + math.sin(math.radians(branch_angle)) * crown_height * 0.3
                branch_size = random.uniform(0.2, 0.4) * crown_width
                c.circle(branch_x, branch_y, branch_size, fill=True, stroke=False)
        
        else:  # round
            # 圓形樹冠
            crown_radius = height * 0.35
            c.circle(x, y+trunk_height+crown_radius, crown_radius, fill=True, stroke=False)
            # 一些較小的附加樹冠，增加自然感
            for _ in range(3):
                sub_x = x + random.uniform(-crown_radius*0.7, crown_radius*0.7)
                sub_y = y + trunk_height + crown_radius + random.uniform(-crown_radius*0.5, crown_radius*0.5)
                sub_radius = crown_radius * random.uniform(0.4, 0.6)
                c.circle(sub_x, sub_y, sub_radius, fill=True, stroke=False)
        
        c.restoreState()