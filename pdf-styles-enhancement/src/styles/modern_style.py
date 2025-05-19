from datetime import datetime
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
class ModernStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        self.main_color = (0.1, 0.6, 0.8)  # 亮藍色
        self.accent_color = (0.8, 0.2, 0.2)  # 亮紅色
        self.text_color = (0.2, 0.2, 0.2)  # 深灰色
        self.bg_color = (1, 1, 1)  # 純白色
        self.caption_height = 0.4 * inch
        
    def create_cover_page(self, c, title, page_width, page_height):
        """創建現代簡約風格的封面頁"""
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 彩色色塊
        c.setFillColorRGB(*self.main_color, 0.8)
        c.rect(0, 0, page_width, 3*inch, fill=True, stroke=False)
        
        c.setFillColorRGB(*self.accent_color, 0.7)
        c.rect(0, page_height - 2*inch, page_width, 2*inch, fill=True, stroke=False)
        
        # 標題
        c.setFont('Myfont', 48)
        c.setFillColorRGB(1, 1, 1)
        main_title = "旅行足跡"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 48)
        c.drawString((page_width - text_width)/2, page_height - 1.7*inch, main_title)
        
        # 副標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(*self.text_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 36)
        c.drawString((page_width - text_width)/2, page_height/2, subtitle)
        
        # 裝飾線
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(4)
        c.line(page_width/2 - 2*inch, page_height/2 - 0.3*inch, 
               page_width/2 + 2*inch, page_height/2 - 0.3*inch)
        
        # 底部文字
        c.setFont('Myfont', 14)
        c.setFillColorRGB(1, 1, 1)
        bottom_text = f"{datetime.now().strftime('%Y年%m月')}"
        text_width = pdfmetrics.stringWidth(bottom_text, 'Myfont', 14)
        c.drawString((page_width - text_width)/2, 1*inch, bottom_text)
        
        
    
    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用現代頁面樣式"""
        # 純白背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部裝飾條
        c.setFillColorRGB(*self.main_color, 0.8)
        c.rect(0, page_height - margin_top - 0.2*inch, page_width, margin_top, fill=True, stroke=False)
        
        # 底部裝飾條
        c.setFillColorRGB(*self.accent_color, 0.7)
        c.rect(0, 0, page_width, margin_bottom, fill=True, stroke=False)
    
    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """添加現代風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch
        
        # 頁面標題
        c.setFont('Myfont', 20)
        c.setFillColorRGB(1, 1, 1)
        header_text = f"{title} - 第 {day} 天"
        c.drawString(margin_left, header_y, header_text)
        
        # 頁碼資訊
        c.setFont('Myfont', 14)
        c.setFillColorRGB(1, 1, 1)
        page_text = f"{page + 1} / {num_pages}"
        page_text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        c.drawString(page_width - margin_left - page_text_width, header_y, page_text)
    
    def draw_photo_frame(self, c, x, y, width, height):
        """繪製現代風格照片邊框"""
        
        # 彩色邊框
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(3)
        c.rect(x, y, width, height-10, fill=False, stroke=True)
        c.setFillColorRGB(1, 1, 1,1)
    
    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加現代風格照片標題"""
        if len(caption) > 20:
            caption = caption[:17] + "..."
        
        # 彩色標題列
        c.setFillColorRGB(*self.main_color, 0.5)
        c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
        
        # 白色文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(1, 1, 1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y + 0.15*inch
        c.drawString(caption_x, caption_y, caption)
    
    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加現代風格頁腳"""
        footer_y = margin_bottom / 2
        
        # 頁碼
        c.setFont('Myfont', 14)
        c.setFillColorRGB(1, 1, 1)
        page_text = f"{page_number}"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        c.drawString((page_width - text_width) / 2, footer_y, page_text)
        
        # 日期資訊
        c.setFont('Myfont', 10)
        c.setFillColorRGB(1, 1, 1)
        date_text = f"{datetime.now().strftime('%Y.%m.%d')}"
        c.drawString(page_width - 1.5*inch, footer_y, date_text)
    
    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加現代風格後記頁"""
        c.showPage()
        
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 頂部色塊
        c.setFillColorRGB(*self.main_color, 0.8)
        c.rect(0, page_height - 2*inch, page_width, 2*inch, fill=True, stroke=False)
        
        # 標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(1, 1, 1)
        epilogue_title = "旅程結束"
        text_width = pdfmetrics.stringWidth(epilogue_title, 'Myfont', 36)
        c.drawString((page_width - text_width) / 2, page_height - 1.7*inch, epilogue_title)
        
        # 分隔線
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        c.line(2*inch, page_height - 2.2*inch, page_width - 2*inch, page_height - 2.2*inch)
        
        # 後記文字
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.text_color)
        epilogue_text = f"感謝您閱讀「{title}」旅程回憶"
        epilogue_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 16)
        c.drawString((page_width - epilogue_width) / 2, page_height / 2, epilogue_text)
        
        # 日期
        date = datetime.now().strftime("%Y年%m月")
        date_width = pdfmetrics.stringWidth(date, 'Myfont', 14)
        c.setFont('Myfont', 14)
        c.drawString((page_width - date_width) / 2, 2*inch, date)

class VintageStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        self.photos_per_page = 3  # Vintage風格每頁照片少一些，更突出照片
        self.main_color = (0.5, 0.4, 0.3)  # 棕色
        self.accent_color = (0.8, 0.7, 0.5)  # 米色/淡金色
        self.text_color = (0.4, 0.3, 0.3)  # 深棕色
        self.bg_color = (0.98, 0.97, 0.95)  # 淺米色，接近紙張顏色
        self.frame_padding = 0.15 * inch # 復古風格邊框留白更多
        self.caption_height = 0.35 * inch # 標題列稍高一些

    def create_cover_page(self, c, title, page_width, page_height):
        """創建復古風格的封面頁"""
        # 紙張背景色
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)

        # 粗糙紋理邊框
        c.setStrokeColorRGB(*self.main_color, 0.5) # 使用主色調棕色，稍微透明
        c.setLineWidth(3)
        c.rect(0.3*inch, 0.3*inch, page_width-0.6*inch, page_height-0.6*inch, stroke=True, fill=False)

        # 標題橫幅背景
        c.setFillColorRGB(*self.accent_color)
        banner_height = 2*inch
        c.rect(0, page_height/2 - banner_height/2, page_width, banner_height, fill=True, stroke=False)

        # 主標題
        c.setFont('Myfont', 52)
        c.setFillColorRGB(*self.main_color)
        main_title = "旅行回憶冊" # 更符合復古感覺的標題
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 52)
        c.drawString((page_width - text_width)/2, page_height/2 + 0.3*inch, main_title)

        # 副標題
        c.setFont('Myfont', 28)
        c.setFillColorRGB(*self.text_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 28)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.8*inch, subtitle)

        # 年份
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.accent_color)
        year_text = f"年份 {datetime.now().strftime('%Y')}"
        text_width = pdfmetrics.stringWidth(year_text, 'Myfont', 16)
        c.drawString((page_width - text_width)/2, 1.2*inch, year_text)

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用復古頁面樣式，增添紋理效果"""
        # 基本背景色
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
    
        # 增加紋理效果 (點狀或線條紋理)
        c.setFillColorRGB(*self.main_color, 0.03) 
        for i in range(0, int(page_height), 4):
            for j in range(0, int(page_width), 4):
                if random.random() > 0.7:  # 只繪製30%的點，形成不規則紋理
                    c.circle(j, i, 0.5, fill=True, stroke=False)
    
        # 復古邊框
        c.setStrokeColorRGB(*self.accent_color, 0.5)
        c.setLineWidth(1)
        c.setDash([3, 2])  # 虛線樣式
        c.rect(0.5*inch, 0.5*inch, page_width-inch, page_height-inch, stroke=True, fill=False)
        c.setDash([])  # 重置虛線設置

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """添加復古風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch

        # 標題文字 (深棕色，襯線字體或類似手寫體)
        c.setFont('Myfont', 22) # 稍大的字體
        c.setFillColorRGB(*self.text_color)
        header_text = f"{title} - Day {day}" # 英文Day更復古
        c.drawString(margin_left, header_y, header_text)

        # 頁碼 (米色，放置在右側)
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.accent_color)
        page_text = f"Page {page + 1} of {num_pages}" # 英文Page of 更復古
        page_text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        c.drawString(page_width - margin_left - page_text_width, header_y, page_text)

        # 細分隔線 (米色，位於標題下方)
        c.setStrokeColorRGB(*self.accent_color, 0.8) # 更淡的米色
        c.setLineWidth(0.8) # 細線
        c.line(margin_left, header_y - 0.3*inch, page_width - margin_left, header_y - 0.3*inch)

    def draw_photo_frame(self, c, x, y, width, height):
        """繪製復古照片邊框"""
        # 略微傾斜的陰影 (模仿老照片的陰影)
        c.setFillColorRGB(0.3, 0.3, 0.3, 0.3) # 柔和陰影
        c.rotate(2) # 稍微傾斜
        c.rect(x + 0.1*inch, y - 0.12*inch, width, height, fill=True, stroke=False)
        c.rotate(-2) # 恢復角度

        # 米色內邊框 (模擬老照片的邊框)
        c.setFillColorRGB(*self.bg_color) # 背景色填充，製造內邊距留白
        c.setStrokeColorRGB(*self.accent_color) # 米色邊框
        c.setLineWidth(1)
        c.rect(x, y, width, height, fill=True, stroke=True)
        c.setFillColorRGB(1, 1, 1,0.4)

    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加復古風格照片標題"""
        if len(caption) > 25: # 復古標題可以稍微長一些
            caption = caption[:22] + "..."

        # 標題底部不規則紙張背景 (類比手寫標籤)
        c.setFillColorRGB(*self.accent_color, 0.2) # 非常輕的米色半透明背景
        c.rect(x - 0.05*inch, y, width + 0.1*inch, self.caption_height, fill=True, stroke=False) # 略微突出的背景

        # 深棕色標題文字 (手寫或襯線字體)
        c.setFont('Myfont', 14) # 稍大的字體
        c.setFillColorRGB(*self.text_color,1)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 14)
        caption_x = x + (width - text_width) / 2
        caption_y = y 
        c.drawString(caption_x, caption_y, caption)

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加復古風格頁腳"""
        footer_y = margin_bottom / 2

        # 底部裝飾線條 (雙線，米色和棕色)
        c.setStrokeColorRGB(*self.accent_color, 0.6) # 米色上層線
        c.setLineWidth(0.8)
        c.line(1.5*inch, footer_y + 0.25*inch, page_width - 1.5*inch, footer_y + 0.25*inch)

        c.setStrokeColorRGB(*self.main_color, 0.7) # 棕色下層線
        c.setLineWidth(0.5)
        c.line(1.5*inch, footer_y + 0.15*inch, page_width - 1.5*inch, footer_y + 0.15*inch)

        # 頁碼 (深棕色，羅馬數字或簡單數字)
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.text_color)
        page_text = f"No. {page_number}" # No. 更復古
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        c.drawString((page_width - text_width) / 2, footer_y - 0.05*inch, page_text) # 稍微向下調整位置

        # 日期 (米色，右對齊)
        c.setFont('Myfont', 10)
        c.setFillColorRGB(*self.accent_color)
        date_text = f"{datetime.now().strftime('%d %b %Y')}" # Day Month Year 格式更復古
        c.drawRightString(page_width - 1.5*inch, footer_y - 0.05*inch, date_text)

    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加復古風格後記頁"""
        c.showPage()

        # 紙張背景色
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)

        # 中心大標題 (深棕色，襯線字體)
        c.setFont('Myfont', 48)
        c.setFillColorRGB(*self.text_color)
        epilogue_title = "旅程的紀念" # 更正式和懷舊的標題
        text_width = pdfmetrics.stringWidth(epilogue_title, 'Myfont', 48)
        c.drawCentredString(page_width/2, page_height - 3*inch, epilogue_title) # 使用居中繪製

        # 底線或裝飾線 (米色)
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        line_width = 4*inch # 線條更長一些
        c.line((page_width - line_width) / 2, page_height - 3.3*inch,
               (page_width + line_width) / 2, page_height - 3.3*inch)

        # 後記感謝文字 (深棕色，更正式的感謝語)
        c.setFont('Myfont', 18) # 字體稍微大一些
        c.setFillColorRGB(*self.text_color)
        epilogue_text = f"感謝您一同回顧這段美好的「{title}」旅程。" # 更正式的語句
        epilogue_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 18)
        c.drawCentredString(page_width/2, page_height / 2, epilogue_text) # 居中

        # 引用語錄 (斜體或強調字體，放置在主要文本下方)
        quote = "旅行，是靈魂的故鄉" # 更符合復古情懷的語錄
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.main_color) # 使用主色調強調
        quote_width = pdfmetrics.stringWidth(quote, 'Myfont', 16)
        c.drawCentredString(page_width/2, page_height / 2 - 1.2*inch, quote) # 居中，稍微下移

        # 署名日期 (米色，頁面底部)
        date = datetime.now().strftime("%Y年 %b") # 年份和月份就可以了，更簡潔
        date_width = pdfmetrics.stringWidth(date, 'Myfont', 14)
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.accent_color)
        c.drawCentredString(page_width/2, 1.5*inch, date) # 居中，底部