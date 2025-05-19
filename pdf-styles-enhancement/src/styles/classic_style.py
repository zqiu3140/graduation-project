import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle

class ClassicStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        self.main_color = (0.1, 0.3, 0.5)  # 深藍色
        self.accent_color = (0.7, 0.5, 0.2)  # 金色
        self.text_color = (0.2, 0.2, 0.3)  # 深灰藍色
        self.bg_color = (0.95, 0.95, 0.95)  # 米白色
        
    def create_cover_page(self, c, title, page_width, page_height):
        """創建經典優雅風格的封面頁"""
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 裝飾邊框
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        c.rect(0.5*inch, 0.5*inch, page_width-inch, page_height-inch, stroke=True, fill=False)
        
        # 內邊框
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(1)
        c.rect(0.7*inch, 0.7*inch, page_width-1.4*inch, page_height-1.4*inch, stroke=True, fill=False)
        
        # 主標題
        c.setFont('Myfont', 42)
        c.setFillColorRGB(*self.main_color)
        
        # 測量文本以居中
        main_title = "旅行回憶錄"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 42)
        c.drawString((page_width - text_width)/2, page_height/2 + 1.5*inch, main_title)
        
        # 副標題
        c.setFont('Myfont', 32)
        c.setFillColorRGB(*self.accent_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 32)
        c.drawString((page_width - text_width)/2, page_height/2, subtitle)
        
        # 底部文字
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.text_color)
        bottom_text = f"製作於 {datetime.now().strftime('%Y年%m月')}"
        text_width = pdfmetrics.stringWidth(bottom_text, 'Myfont', 14)
        c.drawString((page_width - text_width)/2, 1.5*inch, bottom_text)
        
    
    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用經典頁面樣式"""
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 裝飾邊框
        c.setStrokeColorRGB(*self.main_color, 0.3)
        c.setLineWidth(1)
        c.rect(0.4*inch, 0.4*inch, page_width-0.8*inch, page_height-0.8*inch, stroke=True, fill=False)
    
    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """添加經典風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch
        
        # 頁面標題
        c.setFont('Myfont', 20)
        c.setFillColorRGB(*self.main_color)
        header_text = f"{title} - 第 {day} 天"
        c.drawString(margin_left, header_y, header_text)
        
        # 頁碼資訊
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.text_color)
        page_text = f"第 {page + 1} 頁 / 共 {num_pages} 頁"
        page_text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        c.drawString(page_width - margin_left - page_text_width, header_y, page_text)
        
        # 分隔線
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(1)
        c.line(margin_left, header_y - 0.2*inch, page_width - margin_left, header_y - 0.2*inch)
    
    def draw_photo_frame(self, c, x, y, width, height):
        """繪製經典照片邊框"""
        # 下層陰影
        c.setFillColorRGB(0.2, 0.2, 0.2, 0.2)
        c.rect(x + 0.08*inch, y - 0.08*inch, width, height, fill=True, stroke=False)
        
        # 照片邊框
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(1.5)
        c.rect(x, y, width, height, fill=True, stroke=True)
        c.setFillColorRGB(1, 1, 1,1)
        
    
    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加經典風格照片標題"""
        if len(caption) > 20:
            caption = caption[:17] + "..."
            
        # 標題底部背景
        c.setFillColorRGB(0.9, 0.9, 0.95)
        c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color,1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y + 0.1*inch
        c.drawString(caption_x, caption_y, caption)
    
    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加經典風格頁腳"""
        footer_y = margin_bottom / 2
        
        # 分隔線
        c.setStrokeColorRGB(*self.accent_color, 0.7)
        c.setLineWidth(0.5)
        c.line(1*inch, footer_y + 0.2*inch, page_width - 1*inch, footer_y + 0.2*inch)
        
        # 頁碼
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color)
        page_text = f"- {page_number} -"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width) / 2, footer_y, page_text)
        
        # 日期資訊
        c.setFont('Myfont', 10)
        date_text = f"第 {day} 天 | {datetime.now().strftime('%Y年%m月%d日')}"
        c.drawString(1*inch, footer_y, date_text)
    
    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加經典風格後記頁"""
        c.showPage()
        
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 裝飾邊框
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        c.rect(0.5*inch, 0.5*inch, page_width-inch, page_height-inch, stroke=True, fill=False)
        
        # 標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(*self.main_color)
        epilogue_title = "旅行的尾聲"
        text_width = pdfmetrics.stringWidth(epilogue_title, 'Myfont', 36)
        c.drawString((page_width - text_width) / 2, page_height - 3*inch, epilogue_title)
        
        # 分隔線
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(1)
        c.line(2*inch, page_height - 3.2*inch, page_width - 2*inch, page_height - 3.2*inch)
        
        # 後記文字
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.text_color)
        epilogue_text = f"感謝您翻閱「{title}」回憶錄"
        epilogue_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 16)
        c.drawString((page_width - epilogue_width) / 2, page_height / 2, epilogue_text)
        
        # 日期
        quote = "每一次旅行都是一次成長，每張照片都是一個故事。"
        quote_width = pdfmetrics.stringWidth(quote, 'Myfont', 16)
        c.drawString((page_width - quote_width) / 2, page_height / 2 - 1*inch, quote)
        
        # 日期
        date = datetime.now().strftime("%Y年%m月")
        date_width = pdfmetrics.stringWidth(date, 'Myfont', 14)
        c.setFont('Myfont', 14)
        c.drawString((page_width - date_width) / 2, 2*inch, date)