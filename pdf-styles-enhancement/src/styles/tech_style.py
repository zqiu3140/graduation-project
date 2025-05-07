from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
import random
from datetime import datetime
import math
from styles.base_style import BaseStyle

class TechStyle(BaseStyle):
    def __init__(self):
        # 科技藍色與灰色配色
        super().__init__()
        self.main_color = (0.0, 0.4, 0.8)  # 科技藍
        self.accent_color = (0.2, 0.7, 0.9)  # 亮藍色
        self.text_color = (0.1, 0.1, 0.2)  # 近黑色
        self.bg_color = (0.95, 0.97, 1.0)  # 淺藍白色
        self.caption_height = 0.4 * inch
        self.photos_per_page = 4

    def create_cover_page(self, c, title, page_width, page_height):
        # 漸變背景
        steps = 150
        for i in range(steps):
            y = i * (page_height/steps)
            height = page_height/steps
            intensity = 0.95 - (i / steps) * 0.15
            c.setFillColorRGB(intensity*0.95, intensity*0.97, intensity*1.0)
            c.rect(0, y, page_width, height, fill=True, stroke=False)
        
        # 繪製科技圖案背景 (電路板風格)
        c.setStrokeColorRGB(*self.main_color, 0.2)
        c.setLineWidth(0.5)
        
        # 水平線
        for i in range(20):
            y = random.uniform(0, page_height)
            length = random.uniform(1, 4) * inch
            x = random.uniform(0, page_width - length)
            c.line(x, y, x + length, y)
            
            # 添加節點
            if random.random() > 0.5:
                c.circle(x, y, 0.05*inch, fill=False, stroke=True)
            if random.random() > 0.5:
                c.circle(x + length, y, 0.05*inch, fill=False, stroke=True)
        
        # 垂直線
        for i in range(20):
            x = random.uniform(0, page_width)
            length = random.uniform(1, 4) * inch
            y = random.uniform(0, page_height - length)
            c.line(x, y, x, y + length)
            
            # 添加節點
            if random.random() > 0.5:
                c.circle(x, y, 0.05*inch, fill=False, stroke=True)
            if random.random() > 0.5:
                c.circle(x, y + length, 0.05*inch, fill=False, stroke=True)
        
        # 標題區塊
        title_block_width = 6 * inch
        title_block_height = 3.5 * inch
        c.setFillColorRGB(*self.main_color, 0.85)
        c.rect((page_width - title_block_width)/2,
               (page_height - title_block_height)/2,
               title_block_width, title_block_height, fill=True, stroke=False)
        
        # 裝飾性邊框
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        c.setDash([5, 2])
        c.rect((page_width - title_block_width)/2 + 0.1*inch,
               (page_height - title_block_height)/2 + 0.1*inch,
               title_block_width - 0.2*inch, title_block_height - 0.2*inch, 
               fill=False, stroke=True)
        c.setDash([])
        
        # 主標題
        c.setFont('Myfont', 42)
        c.setFillColorRGB(1, 1, 1)
        main_title = "科技之旅"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 42)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.8*inch, main_title)
        
        # 副標題
        c.setFont('Myfont', 24)
        c.setFillColorRGB(1, 1, 1, 0.9)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 24)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.1*inch, subtitle)
        
        # 數位時間戳
        c.setFont('Myfont', 16)
        c.setFillColorRGB(1, 1, 1, 0.8)
        timestamp = f"TIMESTAMP: {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}"
        text_width = pdfmetrics.stringWidth(timestamp, 'Myfont', 16)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.8*inch, timestamp)
        
        # 底部裝飾條
        c.setFillColorRGB(*self.accent_color, 0.7)
        c.rect(0, 0, page_width, 0.5*inch, fill=True, stroke=False)
        
        # 版本號
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1)
        version = f"v1.0.{random.randint(1,999)}"
        c.drawRightString(page_width - 0.5*inch, 0.2*inch, version)

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部和底部條帶
        c.setFillColorRGB(*self.main_color, 0.8)
        c.rect(0, page_height - margin_top, page_width, margin_top, fill=True, stroke=False)
        c.rect(0, 0, page_width, margin_bottom, fill=True, stroke=False)
        
        # 添加科技風格裝飾
        c.setStrokeColorRGB(*self.accent_color, 0.4)
        c.setFillColorRGB(*self.accent_color, 0.1)
        c.setLineWidth(1)
        
        # 右側裝飾條
        bar_width = 0.5 * inch
        c.rect(page_width - bar_width, margin_bottom, bar_width, 
               page_height - margin_top - margin_bottom, fill=True, stroke=True)
        
        # 裝飾元素
        for i in range(10):
            y = margin_bottom + i * (page_height - margin_top - margin_bottom) / 10
            c.line(page_width - bar_width, y, page_width, y)
            if random.random() > 0.6:
                c.setFillColorRGB(*self.accent_color, 0.6)
                c.circle(page_width - bar_width/2, y, 0.08*inch, fill=True, stroke=False)

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        header_y = page_height - margin_top + 0.5 * inch
        
        # 標題
        c.setFont('Myfont', 18)
        c.setFillColorRGB(1, 1, 1)
        header_text = f"{title} • DAY {day}"
        c.drawString(margin_left, header_y, header_text)
        
        # 右側技術資訊
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1, 0.8)
        tech_info = f"ID: {random.randint(1000, 9999)} | {datetime.now().strftime('%Y-%m-%d')}"
        c.drawRightString(page_width - margin_left - 0.6*inch, header_y, tech_info)
        
        # 進度條
        progress = (page + 1) / num_pages
        bar_width = 3 * inch
        bar_height = 0.15 * inch
        c.setStrokeColorRGB(1, 1, 1, 0.5)
        c.setFillColorRGB(1, 1, 1, 0.2)
        c.rect(page_width - margin_left - 0.6*inch - bar_width, 
               header_y - 0.3*inch, bar_width, bar_height, fill=True, stroke=True)
        c.setFillColorRGB(*self.accent_color)
        c.rect(page_width - margin_left - 0.6*inch - bar_width, 
               header_y - 0.3*inch, bar_width * progress, bar_height, fill=True, stroke=False)

    def draw_photo_frame(self, c, x, y, width, height):
        # 主照片背景
        c.setFillColorRGB(1, 1, 1)
        c.rect(x, y, width, height, fill=True, stroke=False)
        
        # 技術風格邊框
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(1.5)
        
        # 點線效果
        c.setDash([5, 2])
        c.rect(x, y, width, height, fill=False, stroke=True)
        c.setDash([])
        
        # 角標裝飾
        corner_size = 0.2 * inch
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(1.5)
        
        # 左上角
        c.line(x, y + corner_size, x, y)
        c.line(x, y, x + corner_size, y)
        
        # 右上角
        c.line(x + width - corner_size, y, x + width, y)
        c.line(x + width, y, x + width, y + corner_size)
        
        # 左下角
        c.line(x, y + height - corner_size, x, y + height)
        c.line(x, y + height, x + corner_size, y + height)
        
        # 右下角
        c.line(x + width - corner_size, y + height, x + width, y + height)
        c.line(x + width, y + height, x + width, y + height - corner_size)
        
        # 座標刻度
        c.setLineWidth(0.5)
        tick_length = 0.05 * inch
        num_ticks = 10
        
        for i in range(num_ticks):
            tx = x + width * (i / (num_ticks-1))
            c.line(tx, y - tick_length, tx, y)
            
            ty = y + height * (i / (num_ticks-1))
            c.line(x - tick_length, ty, x, ty)

    def add_photo_caption(self, c, caption, x, y, width, height):
        if len(caption) > 20:
            caption = caption[:17] + "..."
        
        # 標題背景
        c.setFillColorRGB(*self.main_color, 0.9)
        c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
        
        # 技術指標裝飾
        c.setFillColorRGB(*self.accent_color, 0.7)
        indicator_width = 0.1 * inch
        c.rect(x, y, indicator_width, self.caption_height, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y + 0.13*inch
        c.drawString(caption_x, caption_y, caption)
        
        # 產生隨機技術指標
        c.setFont('Myfont', 8)
        c.setFillColorRGB(1, 1, 1, 0.7)
        tech_indicator = f"#{random.randint(1000, 9999)}"
        c.drawRightString(x + width - 0.1*inch, caption_y - 0.07*inch, tech_indicator)

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        footer_y = margin_bottom / 2
        
        # 頁碼
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1)
        page_text = f"PAGE {page_number}"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width)/2, footer_y, page_text)
        
        # 左側元數據
        c.setFont('Myfont', 9)
        c.setFillColorRGB(1, 1, 1, 0.8)
        meta = f"Day {day} • Seq {page_number:03d}"
        c.drawString(1*inch, footer_y, meta)
        
        # 右側技術信息
        tech = f"Res: 300dpi • RGB • {"%.2f" % (random.random() + 1.0)}MB"
        c.drawRightString(page_width - 1*inch, footer_y, tech)

    def add_epilogue_page(self, c, title, page_width, page_height):
        c.showPage()
        
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 中央圓形
        circle_radius = 3 * inch
        c.setFillColorRGB(*self.main_color, 0.8)
        c.circle(page_width/2, page_height/2, circle_radius, fill=True, stroke=False)
        
        # 技術風格裝飾
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(1)
        
        # 同心圓
        for r in [0.8, 0.6, 0.4]:
            c.setStrokeColorRGB(*self.accent_color, 0.7)
            c.setDash([5, 3])
            c.circle(page_width/2, page_height/2, circle_radius * r, fill=False, stroke=True)
            c.setDash([])
        
        # 放射線
        for i in range(12):
            angle = i * 30 * math.pi / 180
            x1 = page_width/2 + math.cos(angle) * circle_radius * 0.4
            y1 = page_height/2 + math.sin(angle) * circle_radius * 0.4
            x2 = page_width/2 + math.cos(angle) * circle_radius * 1.1
            y2 = page_height/2 + math.sin(angle) * circle_radius * 1.1
            c.setStrokeColorRGB(*self.accent_color)
            c.line(x1, y1, x2, y2)
            
        # 結束標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(1, 1, 1)
        epilogue_text = "數位旅程結束"
        text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 36)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.3*inch, epilogue_text)
        
        # 完成時間
        c.setFont('Myfont', 16)
        c.setFillColorRGB(1, 1, 1, 0.8)
        timestamp = f"項目完成 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ts_width = pdfmetrics.stringWidth(timestamp, 'Myfont', 16)
        c.drawString((page_width - ts_width)/2, page_height/2 - 0.7*inch, timestamp)
        
        # 底部標題
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.accent_color)
        c.drawCentredString(page_width/2, page_height/6, title)