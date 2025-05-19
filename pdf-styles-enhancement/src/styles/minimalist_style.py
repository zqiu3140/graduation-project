from datetime import datetime
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
class MinimalistStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        self.main_color = (0, 0, 0)  # 黑色
        self.text_color = (0.2, 0.2, 0.2)  # 深灰色
        self.bg_color = (1, 1, 1)  # 純白色

    def create_cover_page(self, c, title, page_width, page_height):
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(*self.main_color)
        main_title = "旅遊回憶"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 36)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.5*inch, main_title)
        
        # 副標題
        c.setFont('Myfont', 24)
        c.setFillColorRGB(*self.text_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 24)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.5*inch, subtitle)
        

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        header_y = page_height - margin_top + 0.5 * inch
        c.setFont('Myfont', 18)
        c.setFillColorRGB(*self.main_color)
        header_text = f"第 {day} 天"
        c.drawString(margin_left, header_y, header_text)

    def draw_photo_frame(self, c, x, y, width, height):
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(1)
        c.rect(x, y, width, height, stroke=True, fill=False)

    def add_photo_caption(self, c, caption, x, y, width, height):
        if len(caption) > 20:
            caption = caption[:17] + "..."
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color,1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y +5
        c.drawString(caption_x, caption_y, caption)

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        footer_y = margin_bottom / 2
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color)
        page_text = f"{page_number}"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width)/2, footer_y, page_text)

    def add_epilogue_page(self, c, title, page_width, page_height):
        c.showPage()
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        c.setFont('Myfont', 24)
        c.setFillColorRGB(*self.main_color)
        epilogue_text = f"{title} 結束"
        text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 24)
        c.drawString((page_width - text_width)/2, page_height/2, epilogue_text)