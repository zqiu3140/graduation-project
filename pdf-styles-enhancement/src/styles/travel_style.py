import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
import math

class TravelStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        # 旅行風格顏色方案：溫暖的大地色調
        self.main_color = (0.35, 0.55, 0.45)  # 森林綠
        self.accent_color = (0.85, 0.6, 0.25)  # 沙漠黃
        self.text_color = (0.3, 0.25, 0.2)  # 深咖啡色
        self.bg_color = (0.97, 0.95, 0.9)  # 米紙色
        self.photos_per_page = 3  # 每頁照片數量改為 3
        
        # 裝飾元素的座標
        self.stamp_positions = []
        
    def create_stamp(self, c, x, y, size=0.8*inch):
        """創建旅行印章效果"""
        stamp_types = ['circular', 'square', 'visa']
        stamp_type = random.choice(stamp_types)
        
        # 隨機顏色，偏紅色調
        r = random.uniform(0.6, 1.0)
        g = random.uniform(0.1, 0.5)
        b = random.uniform(0.1, 0.4)
        alpha = random.uniform(0.15, 0.5)  # 透明度
        
        c.saveState()
        c.setFillColorRGB(r, g, b, alpha)
        c.setStrokeColorRGB(r, g, b, alpha*1.2)
        c.setLineWidth(0.5)
        
        if stamp_type == 'circular':
            # 圓形印章
            c.circle(x, y, size/2, stroke=1, fill=1)
            # 添加內部文字
            c.setFillColorRGB(r*0.8, g*0.8, b*0.8, alpha*1.5)
            c.setFont('Myfont', 10)
            date_text = datetime.now().strftime("%y.%m.%d")
            c.drawCentredString(x, y, "旅行印記")
            c.drawCentredString(x, y-14, date_text)
            
        elif stamp_type == 'square':
            # 方形印章
            offset = size/2
            c.rect(x-offset, y-offset, size, size, stroke=1, fill=1)
            # 添加內部文字
            c.setFillColorRGB(r*0.8, g*0.8, b*0.8, alpha*1.5)
            c.setFont('Myfont', 10)
            c.drawCentredString(x, y+5, "景點紀念")
            c.drawCentredString(x, y-10, datetime.now().strftime("%Y/%m/%d"))
            
        else:  # visa
            # 簽證類型印章 - 長方形
            w, h = size*1.5, size*0.8
            c.rect(x-w/2, y-h/2, w, h, stroke=1, fill=1)
            # 添加內部紋理
            c.setFillColorRGB(r*0.8, g*0.8, b*0.8, alpha*1.5)
            c.setFont('Myfont', 9)
            c.drawCentredString(x, y+5, "旅行")
            c.drawCentredString(x, y-10, datetime.now().strftime("%Y年%m月"))
            
        c.restoreState()
        
    def create_cover_page(self, c, title, page_width, page_height):
        """創建旅行風格的封面頁"""
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 舊地圖紋理效果
        self.draw_map_background(c, page_width, page_height)
        
        # 旅行行李箱樣式的外框
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(4)
        c.roundRect(inch, inch, page_width-2*inch, page_height-2*inch, radius=0.3*inch, stroke=True, fill=False)
        
        # 行李箱裝飾帶
        c.setFillColorRGB(*self.accent_color)
        c.rect(inch, page_height/2-0.2*inch, page_width-2*inch, 0.4*inch, fill=True, stroke=False)
        
        # 主標題 - 模擬旅行貼紙效果
        label_width = 4.5*inch
        label_height = 1.5*inch
        label_x = (page_width - label_width)/2
        label_y = page_height/2 + 1.5*inch
        
        # 標籤背景
        c.setFillColorRGB(1, 1, 1, 0.8)
        c.setStrokeColorRGB(*self.accent_color)
        c.setLineWidth(2)
        c.roundRect(label_x, label_y, label_width, label_height, radius=0.1*inch, stroke=True, fill=True)
        
        # 標題文字
        c.setFont('Myfont', 42)
        c.setFillColorRGB(*self.main_color)
        main_title = "旅行回憶"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 42)
        c.drawString((page_width - text_width)/2, label_y + label_height/2-20 , main_title)
        
        # 副標題 - 護照標記風格
        c.setFont('Myfont', 28)
        c.setFillColorRGB(*self.text_color)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 28)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.05*inch, subtitle)
        
        # 底部文字 - 模擬護照號碼或日期
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.text_color)
        bottom_text = f"製作於 {datetime.now().strftime('%Y年%m月%d日')}"
        text_width = pdfmetrics.stringWidth(bottom_text, 'Myfont', 14)
        c.drawString((page_width - text_width)/2, 1.5*inch, bottom_text)
        
        # 添加幾個裝飾性印章
        for i in range(3):
            stamp_x = random.uniform(1.5*inch, page_width-1.5*inch)
            stamp_y = random.uniform(1.5*inch, page_height-1.5*inch)
            # 避免印章蓋到標題
            if not (label_x-inch < stamp_x < label_x+label_width+inch and 
                   label_y-inch < stamp_y < label_y+label_height+inch):
                stamp_size = random.uniform(0.6, 1.0) * inch
                self.create_stamp(c, stamp_x, stamp_y, stamp_size)
    
    def draw_map_background(self, c, page_width, page_height):
        """繪製地圖風格的背景紋理"""
        c.saveState()
        
        # 繪製一些地圖風格的細紋理
        c.setStrokeColorRGB(0.6, 0.5, 0.4, 0.08)
        c.setLineWidth(0.5)
        
        # 經線
        for i in range(0, int(page_width), int(0.5*inch)):
            # 曲線變形，使其看起來像舊地圖
            c.setLineWidth(random.uniform(0.2, 0.6))
            alpha = random.uniform(0.03, 0.08)
            c.setStrokeColorRGB(0.6, 0.5, 0.4, alpha)
            
            for y in range(0, int(page_height), 10):
                offset = random.uniform(-2, 2)
                if y+10 < page_height:
                    c.line(i+offset, y, i+(offset*1.5), y+10)
        
        # 緯線
        for i in range(0, int(page_height), int(0.5*inch)):
            c.setLineWidth(random.uniform(0.2, 0.6))
            alpha = random.uniform(0.03, 0.08)
            c.setStrokeColorRGB(0.6, 0.5, 0.4, alpha)
            
            for x in range(0, int(page_width), 10):
                offset = random.uniform(-2, 2)
                if x+10 < page_width:
                    c.line(x, i+offset, x+10, i+(offset*1.5))
        
        c.restoreState()
    
    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用旅行頁面樣式"""
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 淡淡的地圖背景紋理
        self.draw_map_background(c, page_width, page_height)
        
        # 護照邊框效果
        c.setStrokeColorRGB(*self.main_color, 0.7)
        c.setLineWidth(1.5)
        c.roundRect(0.5*inch, 0.5*inch, page_width-inch, page_height-inch, radius=0.2*inch, stroke=True, fill=False)
        
        # 隨機添加 1-2 個印章效果，但避開照片區域
        self.stamp_positions = []
        for _ in range(random.randint(1, 2)):
            x = random.choice([random.uniform(0.5*inch, margin_left-0.5*inch), 
                              random.uniform(page_width-margin_right+0.5*inch, page_width-0.5*inch)])
            y = random.choice([random.uniform(0.5*inch, margin_bottom-0.5*inch), 
                              random.uniform(page_height-margin_top+0.5*inch, page_height-0.5*inch)])
            self.stamp_positions.append((x, y))
            self.create_stamp(c, x, y)
    
    def get_photo_position(self, photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width=None, usable_height=None, page_width=None, margin_right=None, margin_bottom=None):
        """計算照片位置 - 旅行相簿風格佈局"""
        # 使用 3 張照片的佈局
        # 第一張大照片，下面兩張小照片
        
        if photo_index == 0:
            # 第一張大照片佔據頂部行的全寬
            x = margin_left + inner_margin
            y = page_height - margin_top - grid_height + inner_margin
            width = usable_width - 2*inner_margin
            height = grid_height - 2*inner_margin
        else:
            # 底部兩張照片各佔一半寬度
            col = photo_index - 1  # 0 or 1
            x = margin_left + col * (usable_width/2) + inner_margin
            y = page_height - margin_top - 2*grid_height + inner_margin
            width = (usable_width/2) - 2*inner_margin
            height = grid_height - 2*inner_margin
            
        return x, y, width, height
    
    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """添加旅行風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch
        
        # 頁面標題區背景 - 旅行票券風格
        header_width = page_width - 2*margin_left
        header_height = 0.7*inch
        header_x = margin_left
        header_bg_y = header_y - 0.6*inch
        
        c.setFillColorRGB(*self.accent_color, 0.2)
        c.roundRect(header_x, header_bg_y, header_width, header_height, radius=0.1*inch, fill=True, stroke=False)
        
        # 票券打孔效果
        hole_radius = 0.08*inch
        for i in range(5):
            hole_x = header_x + header_width * (i+1) / 6
            c.setFillColorRGB(*self.bg_color)
            c.circle(hole_x, header_bg_y, hole_radius, fill=True, stroke=False)
            c.circle(hole_x, header_bg_y + header_height, hole_radius, fill=True, stroke=False)
        
        # 頁面標題
        c.setFont('Myfont', 20)
        c.setFillColorRGB(self.text_color[0], self.text_color[1], self.text_color[2], 1.0)
        header_text = f"{title} - 第 {day} 天"
        c.drawString(margin_left + 0.2*inch, header_y, header_text)
        
        # 頁碼資訊
        c.setFont('Myfont', 14)
        c.setFillColorRGB(self.text_color[0], self.text_color[1], self.text_color[2], 1.0)
        page_text = f"第 {page + 1} 頁 / 共 {num_pages} 頁"
        page_text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        c.drawString(page_width - margin_left - page_text_width - 0.2*inch, header_y, page_text)
    
    def draw_photo_frame(self, c, x, y, width, height):
        """繪製旅行風格照片邊框"""
        # 旅行票根風格邊框
        border = 0.04*inch
        
        # 照片陰影
        c.setFillColorRGB(0.2, 0.2, 0.2, 0.2)
        c.rect(x + 0.08*inch, y - 0.08*inch, width, height, fill=True, stroke=False)
        
        # 照片背景
        c.setFillColorRGB(1, 1, 1)
        c.rect(x, y, width, height, fill=True, stroke=False)
        
        # 照片邊框 - 類似舊照片邊框的效果
        c.setStrokeColorRGB(*self.accent_color, 0.8)
        c.setLineWidth(1)
        c.rect(x+border, y+border, width-2*border, height-2*border, stroke=True, fill=False)
        
        # 加入紙膠帶效果
        c.saveState()
        c.setFillColorRGB(random.uniform(0.7, 0.9), random.uniform(0.7, 0.9), random.uniform(0.7, 0.9), 0.5)
        
        # 隨機選擇 1-2 個角落添加膠帶
        corners = [(x, y+height), (x+width, y+height), (x, y), (x+width, y)]
        selected_corners = random.sample(corners, random.randint(1, 2))
        
        for corner in selected_corners:
            corner_x, corner_y = corner
            tape_width = random.uniform(0.2, 0.3) * inch
            tape_angle = random.uniform(-30, 30)
            
            c.saveState()
            c.translate(corner_x, corner_y)
            c.rotate(tape_angle)
            c.rect(-tape_width/2, -tape_width/2, tape_width, tape_width, fill=True, stroke=False)
            c.restoreState()
        
        c.restoreState()
    
    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加旅行風格照片標題"""
        if len(caption) > 25:
            caption = caption[:22] + "..."
            
        # 手寫標籤風格的背景
        c.setFillColorRGB(*self.accent_color, 0.2)
        c.roundRect(x+0.1*inch, y+0.05*inch, width-0.2*inch, self.caption_height-0.1*inch, radius=0.05*inch, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 12)
        c.setFillColorRGB(self.text_color[0], self.text_color[1], self.text_color[2], 1.0)
        text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
        caption_x = x + (width - text_width) / 2
        caption_y = y + 0.15*inch
        c.drawString(caption_x, caption_y, caption)
    
    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加旅行風格頁腳"""
        footer_y = margin_bottom / 2
        
        # 裝飾線 - 虛線效果，類似旅行路線
        c.setStrokeColorRGB(*self.accent_color, 0.7)
        c.setDash([5, 3])
        c.setLineWidth(1)
        c.line(1*inch, footer_y + 0.2*inch, page_width - 1*inch, footer_y + 0.2*inch)
        c.setDash([])
        
        # 頁碼 - 路標風格
        c.setFont('Myfont', 12)
        c.setFillColorRGB(*self.main_color)
        page_text = f"- {page_number} -"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
        
        # 小路標背景
        sign_width = text_width + 0.4*inch
        sign_height = 0.3*inch
        sign_x = (page_width - sign_width) / 2
        sign_y = footer_y - 0.1*inch
        
        c.setFillColorRGB(*self.accent_color, 0.3)
        c.roundRect(sign_x, sign_y, sign_width, sign_height, radius=0.05*inch, fill=True, stroke=False)
        
        c.setFillColorRGB(*self.text_color)
        c.drawString((page_width - text_width) / 2, footer_y, page_text)
        
        # 日期資訊
        c.setFont('Myfont', 10)
        c.setFillColorRGB(self.text_color[0], self.text_color[1], self.text_color[2], 1.0)
        date_text = f"第 {day} 天 | {datetime.now().strftime('%Y年%m月%d日')}"
        c.drawString(1*inch, footer_y, date_text)
        
        # 添加指南針裝飾
        self.draw_compass(c, page_width - 1.5*inch, footer_y, 0.2*inch)
    
    def draw_compass(self, c, x, y, size):
        """繪製指南針裝飾"""
        c.saveState()
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(*self.main_color)
        c.setFillColorRGB(*self.bg_color)
        
        # 外圓
        c.circle(x, y, size, stroke=True, fill=True)
        
        # 內部星形
        c.setFillColorRGB(*self.accent_color, 0.6)
        
        # 四個主要方向
        points = []
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            px = x + size * 0.8 * math.cos(rad)
            py = y + size * 0.8 * math.sin(rad)
            points.append((px, py))
            
            # 短線
            px2 = x + size * 0.5 * math.cos(rad)
            py2 = y + size * 0.5 * math.sin(rad)
            c.line(px2, py2, px, py)
        
        # 連接星形 - 正確使用 lines 方法
        c.setStrokeColorRGB(*self.accent_color, 0.6)
        line_segments = []
        for i in range(len(points)):
            next_i = (i + 1) % len(points)
            line_segments.append((points[i][0], points[i][1], points[next_i][0], points[next_i][1]))
        c.lines(line_segments)
        
        # 中心點
        c.setFillColorRGB(*self.main_color)
        c.circle(x, y, size * 0.1, stroke=False, fill=True)
        
        c.restoreState()
    
    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加旅行風格後記頁"""
        c.showPage()
        
        # 背景
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 地圖背景紋理
        self.draw_map_background(c, page_width, page_height)
        
        # 裝飾邊框 - 旅行行李箱風格
        c.setStrokeColorRGB(*self.main_color)
        c.setLineWidth(3)
        c.roundRect(0.8*inch, 0.8*inch, page_width-1.6*inch, page_height-1.6*inch, radius=0.3*inch, stroke=True, fill=False)
        
        # 行李箱裝飾帶
        c.setFillColorRGB(*self.accent_color, 0.4)
        c.rect(0.8*inch, page_height/2-0.2*inch, page_width-1.6*inch, 0.4*inch, fill=True, stroke=False)
        
        # 標題
        c.setFont('Myfont', 36)
        c.setFillColorRGB(self.text_color[0], self.text_color[1], self.text_color[2], 1.0)
        epilogue_title = "旅程的尾聲"
        text_width = pdfmetrics.stringWidth(epilogue_title, 'Myfont', 36)
        c.drawString((page_width - text_width) / 2, page_height - 3*inch, epilogue_title)
        
        # 裝飾線 - 虛線效果，類似旅行路線
        c.setStrokeColorRGB(*self.accent_color)
        c.setDash([6, 4])
        c.setLineWidth(1.5)
        c.line(2*inch, page_height - 3.2*inch, page_width - 2*inch, page_height - 3.2*inch)
        c.setDash([])
        
        # 後記文字
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.text_color)
        epilogue_text = f"感謝您翻閱「{title}」旅行回憶錄"
        epilogue_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 16)
        c.drawString((page_width - epilogue_width) / 2, page_height / 2, epilogue_text)
        
        # 旅行名言
        quote = "每一次旅行都是一本不會重複的書，每一頁都是獨特的回憶。"
        quote_width = pdfmetrics.stringWidth(quote, 'Myfont', 16)
        c.drawString((page_width - quote_width) / 2, page_height / 2 - 1*inch, quote)
        
        # 日期與地點簽名風格
        date = datetime.now().strftime("%Y年%m月%d日")
        date_width = pdfmetrics.stringWidth(date, 'Myfont', 14)
        c.setFont('Myfont', 14)
        c.drawString((page_width - date_width) / 2, 2*inch, date)
        
        # 添加幾個旅行印章裝飾
        for i in range(4):
            stamp_x = random.uniform(1.5*inch, page_width-1.5*inch)
            stamp_y = random.uniform(1.2*inch, page_height-1.2*inch)
            # 避免印章蓋到標題和文字
            if not (page_width/2-2*inch < stamp_x < page_width/2+2*inch and 
                   page_height/2-1.5*inch < stamp_y < page_height/2+0.5*inch) and \
               not (page_width/2-2*inch < stamp_x < page_width/2+2*inch and 
                   page_height-3.5*inch < stamp_y < page_height-2.5*inch):
                stamp_size = random.uniform(0.6, 1.0) * inch
                self.create_stamp(c, stamp_x, stamp_y, stamp_size)