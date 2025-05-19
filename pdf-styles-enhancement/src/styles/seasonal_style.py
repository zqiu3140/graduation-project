import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from styles.base_style import BaseStyle
import random
class SeasonalStyle(BaseStyle):
    def __init__(self, season="spring"):
        super().__init__()
        self.season = season.lower()
        
        # 根據季節設定顏色
        if self.season == "spring":
            self.main_color = (0.4, 0.8, 0.4)  # 嫩綠色
            self.accent_color = (0.9, 0.6, 0.8,)  # 粉紅色
            self.text_color = (0.3, 0.5, 0.3,1)  # 綠色
            self.bg_color = (0.98, 1.0, 0.98)  # 淺綠白色
            self.season_name = "春季"
            
        elif self.season == "summer":
            self.main_color = (0.0, 0.6, 0.8)  # 海藍色
            self.accent_color = (1.0, 0.8, 0.2,1)  # 陽光黃
            self.text_color = (0.1, 0.4, 0.6,1)  # 深藍色
            self.bg_color = (0.95, 1.0, 1.0)  # 淺藍色
            self.season_name = "夏季"
            
        elif self.season == "autumn":
            self.main_color = (0.8, 0.4, 0.0)  # 橙褐色
            self.accent_color = (0.6, 0.3, 0.1)  # 深褐色
            self.text_color = (0.5, 0.3, 0.0,1)  # 棕色
            self.bg_color = (1.0, 0.97, 0.94)  # 米色
            self.season_name = "秋季"
            
        elif self.season == "winter":
            self.main_color = (0.2, 0.3, 0.7)  # 寶藍色
            self.accent_color = (0.9, 0.9, 0.9)  # 雪白色
            self.text_color = (0.2, 0.2, 0.4,1)  # 深藍灰
            self.bg_color = (0.97, 0.97, 1.0)  # 淺藍白
            self.season_name = "冬季"
        else:
            # 預設春季
            self.main_color = (0.4, 0.8, 0.4)
            self.accent_color = (0.9, 0.6, 0.8)
            self.text_color = (0.3, 0.5, 0.3)
            self.bg_color = (0.98, 1.0, 0.98)
            self.season_name = "春季"

    def create_cover_page(self, c, title, page_width, page_height):
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 季節性裝飾背景元素
        if self.season == "spring":
            # 春季: 花朵圖案
            c.setFillColorRGB(*self.accent_color, 0.2)
            for i in range(30):
                x = random.uniform(0.5*inch, page_width-0.5*inch)
                y = random.uniform(0.5*inch, page_height-0.5*inch)
                size = random.uniform(0.1, 0.3) * inch
                c.circle(x, y, size, fill=True, stroke=False)
                
        elif self.season == "summer":
            # 夏季: 波浪線條
            c.setStrokeColorRGB(*self.main_color, 0.2)
            c.setLineWidth(2)
            for i in range(10):
                y = i * (page_height/10)
                c.line(0, y, page_width, y + random.uniform(-0.5, 0.5)*inch)
                
        elif self.season == "autumn":
            # 秋季: 落葉圖案
            c.setFillColorRGB(*self.main_color, 0.1)
            for i in range(20):
                x = random.uniform(0.5*inch, page_width-0.5*inch)
                y = random.uniform(0.5*inch, page_height-0.5*inch)
                size = random.uniform(0.2, 0.4) * inch
                c.rect(x, y, size, size, fill=True, stroke=False)
                
        elif self.season == "winter":
            # 冬季: 雪花圖案
            c.setFillColorRGB(*self.accent_color, 0.2)
            for i in range(40):
                x = random.uniform(0.5*inch, page_width-0.5*inch)
                y = random.uniform(0.5*inch, page_height-0.5*inch)
                size = random.uniform(0.05, 0.15) * inch
                c.circle(x, y, size, fill=True, stroke=False)
        
        # 季節標題
        c.setFont('Myfont', 48)
        c.setFillColorRGB(*self.main_color,1)
        main_title = f"{self.season_name}之旅"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 48)
        c.drawString((page_width - text_width)/2, page_height/2 + 1*inch, main_title)
        
        # 裝飾線
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(3)
        c.line((page_width - 4*inch)/2, page_height/2 + 0.7*inch, 
               (page_width + 4*inch)/2, page_height/2 + 0.7*inch)
        
        # 副標題
        c.setFont('Myfont', 32)
        c.setFillColorRGB(*self.text_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 32)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
        
        # 底部裝飾
        c.setFillColorRGB(*self.main_color, 0.7)
        c.rect(0, 0, page_width, 1*inch, fill=True, stroke=False)
        c.setFont('Myfont', 14)
        c.setFillColorRGB(1, 1, 1)
        date_text = f"{datetime.now().strftime('%Y年%m月')}"
        date_width = pdfmetrics.stringWidth(date_text, 'Myfont', 14)
        c.drawString((page_width - date_width)/2, 0.4*inch, date_text)

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部和底部季節性裝飾
        c.setFillColorRGB(*self.main_color, 0.2)
        c.rect(0, page_height - margin_top, page_width, margin_top, fill=True, stroke=False)
        c.rect(0, 0, page_width, margin_bottom, fill=True, stroke=False)

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        header_y = page_height - margin_top + 0.5 * inch
        
        # 季節標誌
        c.setFont('Myfont', 22)
        c.setFillColorRGB(*self.main_color)
        season_icon = ""
        if self.season == "spring": season_icon = "【春】"
        elif self.season == "summer": season_icon = "【夏】"
        elif self.season == "autumn": season_icon = "【秋】"
        elif self.season == "winter": season_icon = "【冬】"
        c.setFillColorRGB(*self.main_color,1)
        header_text = f"{season_icon}{title} - 第 {day} 天"
        c.drawString(margin_left, header_y, header_text)

    def draw_photo_frame(self, c, x, y, width, height):
        # 根據季節繪製不同風格的邊框
        c.setFillColorRGB(1, 1, 1)
        
        if self.season == "spring":
            # 春季: 柔和的弧形邊框
            c.setStrokeColorRGB(*self.accent_color)
            c.setLineWidth(2)
            c.roundRect(x, y, width, height, 10, stroke=True, fill=True)
            
        elif self.season == "summer":
            # 夏季: 明亮的直角邊框
            c.setStrokeColorRGB(*self.main_color)
            c.setLineWidth(3)
            c.rect(x, y, width, height, stroke=True, fill=True)
            
        elif self.season == "autumn":
            # 秋季: 不規則邊框
            c.setStrokeColorRGB(*self.main_color)
            c.setLineWidth(2)
            c.rect(x-0.05*inch, y+0.05*inch, width+0.1*inch, height-0.1*inch, stroke=True, fill=False)
            c.rect(x, y, width, height, stroke=True, fill=True)
            
        elif self.season == "winter":
            # 冬季: 雙線邊框
            c.setStrokeColorRGB(*self.main_color)
            c.setLineWidth(1)
            c.rect(x-0.1*inch, y-0.1*inch, width+0.2*inch, height+0.2*inch, stroke=True, fill=False)
            c.rect(x, y, width, height, stroke=True, fill=True)

    def add_photo_caption(self, c, caption, x, y, width, height):
        if len(caption) > 20:
            caption = caption[:17] + "..."
            
        # 季節性標題背景
        c.setFillColorRGB(*self.main_color, 0.8)
        c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y + 0.1*inch
        c.drawString(caption_x, caption_y, caption)

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        footer_y = margin_bottom / 2
        
        # 季節標誌 + 頁碼
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color)
        season_icon = ""
        if self.season == "spring": season_icon = "【春】"
        elif self.season == "summer": season_icon = "【夏】"
        elif self.season == "autumn": season_icon = "【秋】"
        elif self.season == "winter": season_icon = "【冬】"
        
        page_text = f"{season_icon}第 {page_number} 頁"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width)/2, footer_y, page_text)

    def add_epilogue_page(self, c, title, page_width, page_height):
        c.showPage()
        
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 季節性裝飾
        if self.season == "spring":
            c.setFillColorRGB(*self.accent_color, 0.3)
            for i in range(50):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                size = random.uniform(0.05, 0.2) * inch
                c.circle(x, y, size, fill=True, stroke=False)
                
        elif self.season == "summer":
            c.setStrokeColorRGB(*self.main_color, 0.3)
            for i in range(15):
                y1 = random.uniform(0, page_height)
                y2 = y1 + random.uniform(-1, 1) * inch
                c.line(0, y1, page_width, y2)
                
        elif self.season == "autumn":
            c.setFillColorRGB(*self.main_color, 0.2)
            for i in range(30):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                size = random.uniform(0.1, 0.3) * inch
                c.rect(x, y, size, size, fill=True, stroke=False)
                
        elif self.season == "winter":
            c.setFillColorRGB(*self.accent_color, 0.2)
            for i in range(70):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                size = random.uniform(0.03, 0.1) * inch
                c.circle(x, y, size, fill=True, stroke=False)
        
        # 中央色塊
        c.setFillColorRGB(*self.main_color, 0.7)
        c.roundRect((page_width-6*inch)/2, (page_height-3*inch)/2, 6*inch, 3*inch, 20, fill=True, stroke=False)
        
        # 標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(1, 1, 1)
        epilogue_text = f"{self.season_name}回憶結束"
        text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 36)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.5*inch, epilogue_text)
        
        # 日期
        c.setFont('Myfont', 18)
        c.setFillColorRGB(1, 1, 1, 0.9)
        date_text = f"{title} • {datetime.now().strftime('%Y年%m月')}"
        date_width = pdfmetrics.stringWidth(date_text, 'Myfont', 18)
        c.drawString((page_width - date_width)/2, page_height/2 - 0.3*inch, date_text)