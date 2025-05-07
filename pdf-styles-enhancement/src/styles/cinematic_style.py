import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from styles.base_style import BaseStyle
import random
class CinematicStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        self.main_color = (0.1, 0.1, 0.1)  # 近黑色
        self.accent_color = (0.8, 0.1, 0.1)  # 電影紅
        self.text_color = (0.9, 0.9, 0.9)  # 近白色
        self.bg_color = (0.15, 0.15, 0.15)  # 深灰色
        self.photos_per_page = 2  # 電影風格每頁照片更少，更大更有沖擊力
        self.caption_height = 0.5 * inch  # 更大的標題區

    def create_cover_page(self, c, title, page_width, page_height):
        # 黑色背景
        c.setFillColorRGB(*self.main_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部和底部的膠片條紋
        c.setFillColorRGB(0, 0, 0)
        stripe_height = 0.3*inch
        for i in range(10):
            if i % 2 == 0:
                c.rect(i*inch, 0, 0.5*inch, stripe_height, fill=True, stroke=False)
                c.rect(i*inch, page_height-stripe_height, 0.5*inch, stripe_height, fill=True, stroke=False)
        
        # 中央紅色標題區塊
        c.setFillColorRGB(*self.accent_color)
        c.rect(1*inch, (page_height-3*inch)/2, page_width-2*inch, 3*inch, fill=True, stroke=False)
        
        # 標題白色邊框
        c.setStrokeColorRGB(*self.text_color)
        c.setLineWidth(2)
        c.rect(1.2*inch, (page_height-2.6*inch)/2, page_width-2.4*inch, 2.6*inch, fill=False, stroke=True)
        
        # 主標題 (電影標題風格)
        c.setFont('Myfont', 42)
        c.setFillColorRGB(*self.text_color)
        main_title = "電影式旅程"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 42)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.6*inch, main_title)
        
        # 副標題
        c.setFont('Myfont', 28)
        c.setFillColorRGB(*self.text_color, 0.9)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 28)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
        
        # 年份 (電影放映年份風格)
        c.setFont('Myfont', 18)
        c.setFillColorRGB(*self.text_color, 0.8)
        year_text = f"{datetime.now().strftime('%Y')}"
        text_width = pdfmetrics.stringWidth(year_text, 'Myfont', 18)
        c.drawString((page_width - text_width)/2, page_height/2 - 1*inch, year_text)

    def get_photo_position(self, photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width=None, usable_height=None, page_width=None, margin_right=None, margin_bottom=None):
        """電影風格的照片佈局 - 左右並排"""
        # 計算單個照片寬度 (左右並排)
        single_width = (usable_width / 2) - inner_margin
        
        # 保持電影寬螢幕比例 (16:9)
        photo_height = (single_width * 9) / 16
        
        # 確保高度不超過可用高度
        if photo_height > usable_height - 2*inner_margin:
            photo_height = usable_height - 2*inner_margin
            # 調整寬度維持比例
            single_width = (photo_height * 16) / 9
        
        # 垂直置中
        y_offset = (usable_height - photo_height) / 2
        y = page_height - margin_top - photo_height - y_offset
        
        if photo_index == 0:
            # 左側照片
            x = margin_left + inner_margin
        else:
            # 右側照片
            x = margin_left + (usable_width/2) + inner_margin
            
        return x, y, single_width, photo_height
    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        # 深色背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部和底部的膠片條紋
        c.setFillColorRGB(0, 0, 0)
        stripe_height = 0.2*inch
        for i in range(20):
            if i % 2 == 0:
                c.rect(i*0.5*inch, 0, 0.25*inch, stripe_height, fill=True, stroke=False)
                c.rect(i*0.5*inch, page_height-stripe_height, 0.25*inch, stripe_height, fill=True, stroke=False)

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        header_y = page_height - margin_top + 0.4 * inch
        
        # 電影場景編號風格
        c.setFont('Myfont', 18)
        c.setFillColorRGB(*self.accent_color)
        scene_text = f"場景 {day}.{page + 1}"
        c.drawString(margin_left, header_y, scene_text)
        
        # 右側時間碼
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.text_color)
        timecode = f"{random.randint(0,9)}:{random.randint(10,59)}:{random.randint(10,59)}"
        c.drawRightString(page_width - margin_left, header_y, timecode)

    def draw_photo_frame(self, c, x, y, width, height):
        # 電影膠片風格的照片邊框
        
        # 黑色外邊框
        c.setFillColorRGB(0, 0, 0)
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(3)
        c.rect(x-0.1*inch, y-0.1*inch, width+0.2*inch, height+0.2*inch, fill=True, stroke=True)
        
        # 內部白色邊框
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(1)
        c.rect(x, y, width, height, fill=True, stroke=True)
        
        # 膠片打孔效果
        hole_size = 0.1*inch
        spacing = 0.3*inch
        c.setFillColorRGB(0, 0, 0)
        
        # 左側打孔
        for i in range(int(height/spacing)):
            c.circle(x - 0.15*inch, y + i*spacing + 0.15*inch, hole_size, fill=True, stroke=False)
            
        # 右側打孔
        for i in range(int(height/spacing)):
            c.circle(x + width + 0.15*inch, y + i*spacing + 0.15*inch, hole_size, fill=True, stroke=False)

    def add_photo_caption(self, c, caption, x, y, width, height):
        if len(caption) > 25:
            caption = caption[:22] + "..."
        
        # 電影字幕風格標題
        c.setFillColorRGB(0, 0, 0, 0.7)
        caption_height = self.caption_height
        caption_y = y - caption_height  # 標題放在照片下方
        c.rect(x, caption_y, width, caption_height, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.text_color)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 14)
        caption_x = x + (width - text_width) / 2
        c.drawString(caption_x, caption_y + 0.18*inch, caption)

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        footer_y = margin_bottom / 2
        
        # 電影片尾風格頁碼
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.accent_color)
        page_text = f"- {page_number} -"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width)/2, footer_y + 0.1*inch, page_text)
        
        # 製作信息
        c.setFont('Myfont', 10)
        c.setFillColorRGB(*self.text_color)
        credit = f"導演: 您 | 攝影: 您 | {datetime.now().strftime('%Y')}"
        c.drawRightString(page_width - 1*inch, footer_y - 0.1*inch, credit)

    def add_epilogue_page(self, c, title, page_width, page_height):
        c.showPage()
        
        # 黑色背景
        c.setFillColorRGB(0, 0, 0)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 片尾字幕風格
        c.setFont('Myfont', 30)
        c.setFillColorRGB(*self.text_color)
        
        # 依次顯示的片尾字幕
        credits = [
            "終",
            f"{title}",
            f"製作於 {datetime.now().strftime('%Y年%m月%d日')}",
            "感謝觀賞"
        ]
        
        spacing = page_height / (len(credits) + 2)
        for i, line in enumerate(credits):
            y_pos = page_height - (i + 1) * spacing
            text_width = pdfmetrics.stringWidth(line, 'Myfont', 30)
            c.drawString((page_width - text_width)/2, y_pos, line)