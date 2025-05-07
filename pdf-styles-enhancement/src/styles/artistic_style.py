import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
import os
import math
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from styles.base_style import BaseStyle
import random
from reportlab.pdfgen.pathobject import PDFPathObject


class ArtisticStyle(BaseStyle):
    def __init__(self):
        super().__init__()
        # 更豐富的藝術配色方案
        self.main_color = (0.15, 0.35, 0.65)  # 深藍色
        self.accent_color = (0.85, 0.25, 0.25)  # 暗紅色
        self.text_color = (0.1, 0.1, 0.1)  # 深灰色
        self.bg_color = (0.98, 0.96, 0.92)  # 米色畫布
        self.gold_color = (0.85, 0.65, 0.15)  # 金色點綴
        
        # 藝術風格設置
        self.artistic_style = random.choice(["watercolor", "oil", "sketch", "modern"])
        
        # 設置每頁照片數量為 2 (讓照片更大，更有藝術展示效果)
        self.photos_per_page = 2

    def create_cover_page(self, c, title, page_width, page_height):
        # 畫布質感背景
        self.draw_canvas_texture(c, page_width, page_height)
        
        # 藝術框架
        self.draw_artistic_frame(c, page_width, page_height)
        
        # 裝飾圖案
        self.draw_decorative_patterns(c, page_width, page_height)
        
        # 標題 - 藝術字體效果
        c.setFont('Myfont', 54)
        c.setFillColorRGB(*self.main_color, 0.9)
        main_title = "藝術之旅"
        text_width = pdfmetrics.stringWidth(main_title, 'Myfont', 54)
        
        # 繪製陰影效果
        c.setFillColorRGB(0.2, 0.2, 0.3, 0.3)
        c.drawString((page_width - text_width)/2 + 0.05*inch, page_height/2 + 1*inch - 0.05*inch, main_title)
        
        # 繪製主標題
        c.setFillColorRGB(*self.main_color, 0.9)
        c.drawString((page_width - text_width)/2, page_height/2 + 1*inch, main_title)
        
        # 金色裝飾線
        c.setStrokeColorRGB(*self.gold_color)
        c.setLineWidth(2)
        line_width = text_width * 1.2
        c.line((page_width - line_width)/2, page_height/2 + 0.8*inch, 
               (page_width + line_width)/2, page_height/2 + 0.8*inch)
        
        # 副標題
        c.setFont('Myfont', 32)
        c.setFillColorRGB(*self.accent_color, 0.95)
        subtitle = title
        text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 32)
        c.drawString((page_width - text_width)/2, page_height/2 - 0.5*inch, subtitle)
        
        # 簽名風格的日期和標記
        c.setFont('Myfont', 16)
        c.setFillColorRGB(*self.text_color, 0.8)
        date_text = f"創作於 {datetime.now().strftime('%Y年%m月%d日')}"
        c.drawString(page_width - 3*inch, 1.2*inch, date_text)
        
        # 繪製藝術簽名
        self.draw_artistic_signature(c, 1.5*inch, 1.2*inch)

    def draw_canvas_texture(self, c, page_width, page_height):
        """繪製畫布質感背景"""
        # 基礎背景色
        c.setFillColorRGB(*self.bg_color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # 根據藝術風格繪製不同質感
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩紙質感 - 隨機小色塊
            for _ in range(2000):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                size = random.uniform(0.01*inch, 0.03*inch)
                opacity = random.uniform(0.01, 0.04)
                r = self.bg_color[0] * random.uniform(0.9, 1.1)
                g = self.bg_color[1] * random.uniform(0.9, 1.1)
                b = self.bg_color[2] * random.uniform(0.9, 1.1)
                c.setFillColorRGB(r, g, b, opacity)
                c.circle(x, y, size, fill=True, stroke=False)
                
        elif self.artistic_style == "oil":
            # 油畫布質感 - 紋理線條
            c.setStrokeColorRGB(0.4, 0.4, 0.4, 0.03)
            for i in range(0, int(page_height), 3):
                c.setLineWidth(random.uniform(0.1, 0.5))
                c.line(0, i, page_width, i + random.uniform(-2, 2))
                
        elif self.artistic_style == "sketch":
            # 素描紙質感 - 點狀紋理
            for _ in range(5000):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                size = random.uniform(0.2, 0.8)
                opacity = random.uniform(0.01, 0.05)
                c.setFillColorRGB(0.2, 0.2, 0.2, opacity)
                c.rect(x, y, size, size, fill=True, stroke=False)
        
        else:  # modern
            # 現代藝術質感 - 幾何塊狀
            for _ in range(15):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                width = random.uniform(0.5*inch, 3*inch)
                height = random.uniform(0.5*inch, 3*inch)
                opacity = random.uniform(0.01, 0.04)
                color_choice = random.choice([self.main_color, self.accent_color, self.gold_color])
                c.setFillColorRGB(*color_choice, opacity)
                c.rect(x, y, width, height, fill=True, stroke=False)
        
        c.restoreState()

    def draw_artistic_frame(self, c, page_width, page_height):
        """繪製藝術風格邊框"""
        c.saveState()
        
        margin = 0.5 * inch
        
        if self.artistic_style == "watercolor":
            # 水彩暈染效果邊框
            c.setStrokeColorRGB(*self.main_color, 0.4)
            c.setLineWidth(5)
            for i in range(8):
                offset = i * 1.5
                c.setStrokeColorRGB(*self.main_color, 0.1 - i*0.01)
                c.roundRect(margin - offset, margin - offset, 
                           page_width - 2*margin + 2*offset, 
                           page_height - 2*margin + 2*offset, 
                           radius=10, stroke=True, fill=False)
                
        elif self.artistic_style == "oil":
            # 厚重的油畫框架
            c.setStrokeColorRGB(*self.accent_color, 0.7)
            c.setLineWidth(8)
            c.roundRect(margin, margin, page_width - 2*margin, page_height - 2*margin, radius=15, stroke=True, fill=False)
            
            # 內框
            c.setStrokeColorRGB(*self.gold_color, 0.6)
            c.setLineWidth(3)
            c.roundRect(margin + 0.2*inch, margin + 0.2*inch, 
                       page_width - 2*margin - 0.4*inch, 
                       page_height - 2*margin - 0.4*inch, 
                       radius=10, stroke=True, fill=False)
                
        elif self.artistic_style == "sketch":
            # 手繪草稿風格邊框
            c.setStrokeColorRGB(*self.text_color, 0.5)
            c.setLineWidth(1)
            c.setDash([5, 2])
            
            # 不規則線條模擬手繪感 - 使用路徑物件
            p = PDFPathObject()
            p.moveTo(margin, margin)
            p.lineTo(page_width - margin, margin)
            p.lineTo(page_width - margin, page_height - margin)
            p.lineTo(margin, page_height - margin)
            p.lineTo(margin, margin)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash([])
        
        else:  # modern
            # 現代藝術邊框 - 不對稱設計
            c.setFillColorRGB(*self.main_color, 0.15)
            c.rect(margin, margin, 0.5*inch, page_height - 2*margin, fill=True, stroke=False)
            c.rect(margin, margin, page_width - 2*margin, 0.5*inch, fill=True, stroke=False)
            
            c.setFillColorRGB(*self.accent_color, 0.15)
            c.rect(page_width - margin - 0.5*inch, margin, 0.5*inch, page_height - 2*margin, fill=True, stroke=False)
            c.rect(margin, page_height - margin - 0.5*inch, page_width - 2*margin, 0.5*inch, fill=True, stroke=False)
        
        c.restoreState()

    def draw_decorative_patterns(self, c, page_width, page_height):
        """繪製裝飾性圖案"""
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩飛濺效果
            for _ in range(10):
                x = random.uniform(0.5*inch, page_width - 0.5*inch)
                y = random.uniform(0.5*inch, page_height - 0.5*inch)
                size = random.uniform(0.1*inch, 0.3*inch)
                opacity = random.uniform(0.05, 0.15)
                color_choice = random.choice([self.main_color, self.accent_color])
                
                # 隨機水彩飛濺
                c.setFillColorRGB(*color_choice, opacity)
                for i in range(8):
                    splash_x = x + random.uniform(-size*2, size*2)
                    splash_y = y + random.uniform(-size*2, size*2)
                    splash_size = random.uniform(size*0.2, size)
                    c.circle(splash_x, splash_y, splash_size, fill=True, stroke=False)
                
        elif self.artistic_style == "oil":
            # 油畫質感裝飾
            for corner in [(0.7*inch, 0.7*inch), (page_width-0.7*inch, 0.7*inch), 
                          (0.7*inch, page_height-0.7*inch), (page_width-0.7*inch, page_height-0.7*inch)]:
                x, y = corner
                
                # 繪製角落花紋
                c.setFillColorRGB(*self.gold_color, 0.2)
                for i in range(5):
                    angle = i * (2*math.pi/5)
                    petal_x = x + math.cos(angle) * 0.4*inch
                    petal_y = y + math.sin(angle) * 0.4*inch
                    c.circle(petal_x, petal_y, 0.15*inch, fill=True, stroke=False)
                
                # 中心圓
                c.setFillColorRGB(*self.accent_color, 0.3)
                c.circle(x, y, 0.2*inch, fill=True, stroke=False)
                
        elif self.artistic_style == "sketch":
            # 素描風格裝飾
            c.setStrokeColorRGB(*self.text_color, 0.3)
            c.setLineWidth(0.7)
            
            # 簡易花草素描
            for _ in range(5):
                x = random.uniform(0.5*inch, page_width - 0.5*inch)
                y = random.choice([0.5*inch, page_height - 0.5*inch])
                
                # 莖
                stem_height = random.uniform(0.5*inch, 1.5*inch)
                c.line(x, y, x, y + stem_height if y < 1*inch else y - stem_height)
                
                # 簡易葉子
                leaf_count = random.randint(2, 4)
                for i in range(leaf_count):
                    leaf_y = y + (i/leaf_count) * stem_height if y < 1*inch else y - (i/leaf_count) * stem_height
                    leaf_x = x + random.choice([-1, 1]) * random.uniform(0.1*inch, 0.3*inch)
                    c.line(x, leaf_y, leaf_x, leaf_y + random.uniform(0.05*inch, 0.15*inch))
        
        else:  # modern
            # 現代藝術裝飾 - 幾何形狀
            for _ in range(8):
                x = random.uniform(1*inch, page_width - 1*inch)
                y = random.uniform(1*inch, page_height - 1*inch)
                size = random.uniform(0.2*inch, 0.5*inch)
                shape_type = random.choice(["circle", "triangle", "rectangle"])
                color_choice = random.choice([self.main_color, self.accent_color, self.gold_color])
                c.setFillColorRGB(*color_choice, 0.1)
                
                if shape_type == "circle":
                    c.circle(x, y, size, fill=True, stroke=False)
                elif shape_type == "triangle":
                    c.setFillColorRGB(*color_choice, 0.1)
                    points = [
                        (x, y + size),
                        (x - size, y - size),
                        (x + size, y - size)
                    ]
                    p=PDFPathObject()
                    p.moveTo(points[0][0], points[0][1])
                    for px, py in points[1:]:
                        p.lineTo(px, py)
                    p.lineTo(points[0][0], points[0][1])
                    c.drawPath(p, stroke=0, fill=1)  # 修改這行，使用 drawPath 代替 fill
                else:  # rectangle
                    rotation = random.uniform(0, 45)
                    c.saveState()
                    c.translate(x, y)
                    c.rotate(rotation)
                    c.rect(-size/2, -size/2, size, size, fill=True, stroke=False)
                    c.restoreState()
        
        c.restoreState()

    def draw_artistic_signature(self, c, x, y):
        """繪製藝術簽名效果"""
        c.saveState()
        
        c.setStrokeColorRGB(*self.gold_color, 0.8)
        c.setLineWidth(1.5)
        
        # 簡單的藝術簽名
        width = 1.2 * inch
        height = 0.3 * inch
        
        # 基礎曲線
        points = [
            (x, y),
            (x + width*0.3, y - height*0.5),
            (x + width*0.7, y + height*0.5),
            (x + width, y)
        ]
        p=PDFPathObject()
        p.moveTo(points[0][0], points[0][1])
        p.curveTo(points[1][0], points[1][1], 
                 points[2][0], points[2][1],
                 points[3][0], points[3][1])
        c.drawPath(p, stroke=1, fill=0)  # 修改這行，用 drawPath 代替 stroke

        
        # 點綴
        c.setFillColorRGB(*self.gold_color, 0.8)
        c.circle(x + random.uniform(width*0.8, width), y + random.uniform(-0.05*inch, 0.05*inch), 
                0.03*inch, fill=True, stroke=False)
        
        c.restoreState()

    def apply_page_style(self, c, page_width, page_height, margin_top, margin_left, margin_right, margin_bottom):
        """應用藝術風格到頁面"""
        # 繪製藝術背景
        self.draw_canvas_texture(c, page_width, page_height)
        
        # 根據藝術風格添加裝飾
        if self.artistic_style == "watercolor":
            # 水彩頁面風格 - 頁面邊緣水彩暈染
            c.saveState()
            for edge in ["top", "right", "bottom", "left"]:
                color_choice = random.choice([self.main_color, self.accent_color])
                c.setFillColorRGB(*color_choice, 0.05)
                
                if edge == "top":
                    for i in range(20):
                        x = random.uniform(0, page_width)
                        y = page_height - random.uniform(0, 0.8*inch)
                        size = random.uniform(0.1*inch, 0.4*inch)
                        c.circle(x, y, size, fill=True, stroke=False)
                elif edge == "right":
                    for i in range(20):
                        x = page_width - random.uniform(0, 0.8*inch)
                        y = random.uniform(0, page_height)
                        size = random.uniform(0.1*inch, 0.4*inch)
                        c.circle(x, y, size, fill=True, stroke=False)
                elif edge == "bottom":
                    for i in range(20):
                        x = random.uniform(0, page_width)
                        y = random.uniform(0, 0.8*inch)
                        size = random.uniform(0.1*inch, 0.4*inch)
                        c.circle(x, y, size, fill=True, stroke=False)
                else:  # left
                    for i in range(20):
                        x = random.uniform(0, 0.8*inch)
                        y = random.uniform(0, page_height)
                        size = random.uniform(0.1*inch, 0.4*inch)
                        c.circle(x, y, size, fill=True, stroke=False)
            c.restoreState()
                
        elif self.artistic_style == "oil":
            # 油畫頁面風格 - 簡單的油畫框架
            c.saveState()
            c.setStrokeColorRGB(*self.gold_color, 0.4)
            c.setLineWidth(4)
            c.rect(0.3*inch, 0.3*inch, page_width - 0.6*inch, page_height - 0.6*inch, 
                  stroke=True, fill=False)
            c.restoreState()
            
        elif self.artistic_style == "sketch":
            # 素描頁面風格
            c.saveState()
            # 隨機鉛筆線條效果
            c.setStrokeColorRGB(0.3, 0.3, 0.3, 0.1)
            for _ in range(30):
                c.setLineWidth(random.uniform(0.5, 1.5))
                x1 = random.uniform(0, page_width)
                y1 = random.uniform(0, page_height)
                length = random.uniform(0.5*inch, 2*inch)
                angle = random.uniform(0, 2*math.pi)
                x2 = x1 + math.cos(angle) * length
                y2 = y1 + math.sin(angle) * length
                c.line(x1, y1, x2, y2)
            c.restoreState()
        
        else:  # modern
            # 現代藝術頁面風格 - 幾何分區
            c.saveState()
            # 隨機色塊
            for _ in range(3):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                width = random.uniform(1*inch, 3*inch)
                height = random.uniform(1*inch, 3*inch)
                color_choice = random.choice([self.main_color, self.accent_color, self.gold_color])
                c.setFillColorRGB(*color_choice, 0.05)
                c.rect(x, y, width, height, fill=True, stroke=False)
            c.restoreState()

    def get_photo_position(self, photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width=None, usable_height=None, page_width=None, margin_right=None, margin_bottom=None):
        """藝術風格的照片位置計算 - 每頁2張照片"""
        
        # 根據風格決定照片佈局
        if self.artistic_style == "watercolor" or self.artistic_style == "sketch":
            # 上下佈局 - 稍微錯開的感覺
            row = photo_index
            offset_x = random.uniform(-0.1, 0.1) * inch  # 輕微水平偏移
            
            x = margin_left + offset_x + inner_margin
            y = page_height - margin_top - (row + 1) * grid_height + inner_margin
            
            width = usable_width - 2 * inner_margin
            height = grid_height - 2 * inner_margin - self.caption_height
            
        else:  # oil or modern
            # 左右佈局 - 對稱展示
            col = photo_index
            
            x = margin_left + col * grid_width + inner_margin
            y = (page_height - usable_height) / 2 + inner_margin
            
            width = grid_width - 2 * inner_margin
            height = usable_height - 2 * inner_margin - self.caption_height
        
        return x, y, width, height

    def add_page_header(self, c, title, day, page, num_pages, page_width, page_height, margin_top, margin_left):
        """藝術風格頁眉"""
        header_y = page_height - margin_top + 0.5 * inch
        
        c.saveState()
        
        # 裝飾線條或圖案
        if self.artistic_style == "watercolor":
            # 水彩風格裝飾
            c.setFillColorRGB(*self.main_color, 0.2)
            c.rect(margin_left - 0.2*inch, header_y - 0.4*inch, 
                  page_width - margin_left*2 + 0.4*inch, 0.7*inch, 
                  fill=True, stroke=False)
            
        elif self.artistic_style == "oil":
            # 油畫風格的金色底線
            c.setStrokeColorRGB(*self.gold_color, 0.7)
            c.setLineWidth(2)
            c.line(margin_left, header_y - 0.3*inch, 
                  page_width - margin_left, header_y - 0.3*inch)
            
        elif self.artistic_style == "sketch":
            # 手繪線條
            c.setStrokeColorRGB(*self.text_color, 0.5)
            c.setLineWidth(1)
            c.setDash([5, 2])
            c.line(margin_left, header_y - 0.3*inch, 
                  page_width - margin_left, header_y - 0.3*inch)
            c.setDash([])
            
        else:  # modern
            # 現代藝術矩形
            c.setFillColorRGB(*self.accent_color, 0.15)
            c.rect(margin_left - 0.1*inch, header_y - 0.35*inch, 
                  3*inch, 0.5*inch, fill=True, stroke=False)
        
        # 標題文字
        c.setFont('Myfont', 18)
        c.setFillColorRGB(*self.main_color, 1.0)  # 確保不透明
        header_text = f"{title} - 第 {day} 天"
        c.drawString(margin_left, header_y, header_text)
        
        # 添加藝術感頁碼
        c.setFont('Myfont', 14)
        c.setFillColorRGB(*self.accent_color, 1.0)
        page_text = f"{page + 1}/{num_pages}"
        text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 14)
        
        if self.artistic_style == "watercolor" or self.artistic_style == "sketch":
            # 簡單頁碼
            c.drawRightString(page_width - margin_left, header_y, page_text)
        else:
            # 裝飾頁碼
            c.setFillColorRGB(*self.gold_color, 0.2)
            c.circle(page_width - margin_left - text_width/2 - 0.2*inch, header_y - 0.05*inch, 
                    0.25*inch, fill=True, stroke=False)
            c.setFillColorRGB(*self.text_color, 1.0)
            c.drawRightString(page_width - margin_left, header_y, page_text)
        
        c.restoreState()

    def draw_photo_frame(self, c, x, y, width, height):
        """繪製藝術風格照片邊框，帶有創意效果"""
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩風格相框
            # 陰影層
            c.setFillColorRGB(0.2, 0.2, 0.2, 0.2)
            shadow_offset = 0.08 * inch
            c.rect(x+shadow_offset, y-shadow_offset, width, height, fill=True, stroke=False)
            
            # 照片白色底
            c.setFillColorRGB(1, 1, 1, 1.0)  # 確保不透明
            c.rect(x, y, width, height, fill=True, stroke=False)
            
            # 水彩邊緣效果
            for _ in range(50):
                edge = random.choice(["top", "right", "bottom", "left"])
                if edge == "top":
                    px = x + random.uniform(0, width)
                    py = y + height - random.uniform(0, 0.1*inch)
                elif edge == "right":
                    px = x + width - random.uniform(0, 0.1*inch)
                    py = y + random.uniform(0, height)
                elif edge == "bottom":
                    px = x + random.uniform(0, width)
                    py = y + random.uniform(0, 0.1*inch)
                else:  # left
                    px = x + random.uniform(0, 0.1*inch)
                    py = y + random.uniform(0, height)
                
                size = random.uniform(0.02*inch, 0.08*inch)
                color_choice = random.choice([self.main_color, self.accent_color])
                c.setFillColorRGB(*color_choice, random.uniform(0.1, 0.3))
                c.circle(px, py, size, fill=True, stroke=False)
            
        elif self.artistic_style == "oil":
            # 厚重油畫框
            # 陰影
            c.setFillColorRGB(0.2, 0.2, 0.2, 0.3)
            shadow_offset = 0.12 * inch
            c.rect(x+shadow_offset, y-shadow_offset, width, height, fill=True, stroke=False)
            
            # 外框 - 金色畫框效果
            frame_width = 0.15 * inch
            c.setFillColorRGB(*self.gold_color, 0.8)
            c.rect(x-frame_width, y-frame_width, width+2*frame_width, height+2*frame_width, fill=True, stroke=False)
            
            # 內框 - 白色
            c.setFillColorRGB(1, 1, 1, 1.0)
            c.rect(x, y, width, height, fill=True, stroke=False)
            
            # 框上光澤效果
            c.setFillColorRGB(1, 1, 1, 0.3)
            corner_size = 0.1 * inch
            # 左上角高光
            c.rect(x-frame_width, y+height, corner_size, frame_width, fill=True, stroke=False)
            # 右下角高光
            c.rect(x+width-corner_size+frame_width, y-frame_width, corner_size, frame_width, fill=True, stroke=False)
            
        elif self.artistic_style == "sketch":
            # 素描風格相框
            
            # 照片白色底
            c.setFillColorRGB(1, 1, 1, 1.0)
            c.rect(x, y, width, height, fill=True, stroke=False)
            
            # 手繪線條效果
            c.setStrokeColorRGB(*self.text_color, 0.7)
            c.setLineWidth(1)
            
            # 四邊繪製不規則線條
            for edge in ["top", "right", "bottom", "left"]:
                c.setLineWidth(random.uniform(0.5, 1.5))
                if edge == "top":
                    y1 = y + height
                    x1 = x
                    x2 = x + width
                    y2 = y1
                    # 模擬手繪不規則線
                    segments = 8
                    p=PDFPathObject()
                    p.moveTo(x1, y1)
                    for i in range(1, segments):
                        segment_x = x1 + (x2-x1) * (i/segments)
                        segment_y = y1 + random.uniform(-0.04*inch, 0.04*inch)
                        p.lineTo(segment_x, segment_y)
                    p.lineTo(x2, y2)
                    
                elif edge == "right":
                    x1 = x + width
                    y1 = y + height
                    x2 = x1
                    y2 = y
                    segments = 8
                    p.moveTo(x1, y1)
                    for i in range(1, segments):
                        segment_y = y1 - (y1-y2) * (i/segments)
                        segment_x = x1 + random.uniform(-0.04*inch, 0.04*inch)
                        p.lineTo(segment_x, segment_y)
                    p.lineTo(x2, y2)
                    
                elif edge == "bottom":
                    y1 = y
                    x1 = x + width
                    x2 = x
                    y2 = y1
                    segments = 8
                    p.moveTo(x1, y1)
                    for i in range(1, segments):
                        segment_x = x1 - (x1-x2) * (i/segments)
                        segment_y = y1 + random.uniform(-0.04*inch, 0.04*inch)
                        p.lineTo(segment_x, segment_y)
                    p.lineTo(x2, y2)
                    
                else:  # left
                    x1 = x
                    y1 = y
                    x2 = x1
                    y2 = y + height
                    segments = 8
                    p.moveTo(x1, y1)
                    for i in range(1, segments):
                        segment_y = y1 + (y2-y1) * (i/segments)
                        segment_x = x1 + random.uniform(-0.04*inch, 0.04*inch)
                        p.lineTo(segment_x, segment_y)
                    p.lineTo(x2, y2)
            
            c.drawPath(p, stroke=1, fill=0)  # 繪製路徑
            
            # 手繪感細節 - 角落加強
            for corner in [(x, y), (x+width, y), (x, y+height), (x+width, y+height)]:
                cx, cy = corner
                c.setLineWidth(random.uniform(0.7, 1.0))
                c.line(cx-0.05*inch, cy, cx+0.05*inch, cy)
                c.line(cx, cy-0.05*inch, cx, cy+0.05*inch)
            
        else:  # modern
            # 現代藝術相框
            
            # 照片白色底
            c.setFillColorRGB(1, 1, 1, 1.0)
            c.rect(x, y, width, height, fill=True, stroke=False)
            
            # 不對稱設計
            c.setStrokeColorRGB(*self.main_color, 0.8)
            c.setLineWidth(4)
            
            # 只繪製某些邊
            edges = random.sample(["top", "right", "bottom", "left"], random.randint(2, 3))
            
            if "top" in edges:
                c.line(x-0.1*inch, y+height+0.1*inch, x+width+0.1*inch, y+height+0.1*inch)
            if "right" in edges:
                c.line(x+width+0.1*inch, y+height+0.1*inch, x+width+0.1*inch, y-0.1*inch)
            if "bottom" in edges:
                c.line(x+width+0.1*inch, y-0.1*inch, x-0.1*inch, y-0.1*inch)
            if "left" in edges:
                c.line(x-0.1*inch, y-0.1*inch, x-0.1*inch, y+height+0.1*inch)
                
            # 點綴色塊
            c.setFillColorRGB(*self.accent_color, 0.4)
            accent_pos = random.choice(["top-left", "top-right", "bottom-left", "bottom-right"])
            
            if accent_pos == "top-left":
                c.rect(x-0.15*inch, y+height, 0.3*inch, 0.15*inch, fill=True, stroke=False)
            elif accent_pos == "top-right":
                c.rect(x+width-0.15*inch, y+height, 0.3*inch, 0.15*inch, fill=True, stroke=False)
            elif accent_pos == "bottom-left":
                c.rect(x-0.15*inch, y-0.15*inch, 0.3*inch, 0.15*inch, fill=True, stroke=False)
            else:
                c.rect(x+width-0.15*inch, y-0.15*inch, 0.3*inch, 0.15*inch, fill=True, stroke=False)
        
        c.restoreState()
    
    def add_photo_caption(self, c, caption, x, y, width, height):
        """添加藝術風格照片標題"""
        if len(caption) > 20:
            caption = caption[:17] + "..."
            
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩風格標題
            c.setFillColorRGB(*self.main_color, 0.2)
            # 不規則形狀背景
            c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
            
            # 標題文字
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)  # 確保文字不透明
            text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
            caption_x = x + (width - text_width) / 2
            caption_y = y + 0.1*inch
            c.drawString(caption_x, caption_y, caption)
            
        elif self.artistic_style == "oil":
            # 油畫風格標題 - 帶有金色邊框
            c.setFillColorRGB(*self.main_color, 0.8)
            c.rect(x, y, width, self.caption_height, fill=True, stroke=False)
            
            # 金色邊框
            c.setStrokeColorRGB(*self.gold_color, 0.7)
            c.setLineWidth(1)
            c.rect(x+0.05*inch, y+0.05*inch, width-0.1*inch, self.caption_height-0.1*inch, fill=False, stroke=True)
            
            # 標題文字
            c.setFont('Myfont', 12)
            c.setFillColorRGB(1, 1, 1, 1.0)  # 白色文字
            text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
            caption_x = x + (width - text_width) / 2
            caption_y = y + 0.1*inch
            c.drawString(caption_x, caption_y, caption)
            
        elif self.artistic_style == "sketch":
            # 素描風格標題 - 手寫效果
            # 手繪線框
            c.setStrokeColorRGB(*self.text_color, 0.5)
            c.setLineWidth(0.7)
            c.setDash([8, 3])
            c.rect(x+0.05*inch, y+0.05*inch, width-0.1*inch, self.caption_height-0.1*inch, fill=False, stroke=True)
            c.setDash([])
            
            # 標題文字 - 稍微傾斜
            c.saveState()
            c.translate(x + width/2, y + self.caption_height/2)
            rotation = random.uniform(-2, 2)
            c.rotate(rotation)
            
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            text_width = pdfmetrics.stringWidth(caption, 'Myfont', 12)
            c.drawString(-text_width/2, -0.05*inch, caption)
            
            c.restoreState()
            
        else:  # modern
            # 現代藝術標題 - 簡潔強調
            # 用色塊來突出
            c.setFillColorRGB(*self.accent_color, 0.8)
            block_width = 0.2 * inch
            c.rect(x, y, block_width, self.caption_height, fill=True, stroke=False)
            
            # 標題文字
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            caption_x = x + block_width + 0.1*inch
            caption_y = y + 0.1*inch
            c.drawString(caption_x, caption_y, caption)
        
        c.restoreState()

    def add_footer(self, c, page_number, page_width, page_height, margin_bottom, day):
        """添加藝術風格頁腳"""
        footer_y = margin_bottom / 2
        
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩風格頁腳
            c.setFillColorRGB(*self.main_color, 0.15)
            c.rect(page_width/2 - 1*inch, footer_y - 0.15*inch, 2*inch, 0.3*inch, fill=True, stroke=False)
            
            # 頁碼
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            page_text = f"頁 {page_number}"
            text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
            c.drawString((page_width - text_width)/2, footer_y, page_text)
            
        elif self.artistic_style == "oil":
            # 油畫風格頁腳 - 帶有金色裝飾
            # 金色裝飾線
            c.setStrokeColorRGB(*self.gold_color, 0.6)
            c.setLineWidth(2)
            line_width = 3 * inch
            c.line((page_width - line_width)/2, footer_y + 0.2*inch, (page_width + line_width)/2, footer_y + 0.2*inch)
            
            # 頁碼
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            page_text = f"頁 {page_number}"
            text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
            c.drawString((page_width - text_width)/2, footer_y, page_text)
            
            # 小裝飾
            c.setFillColorRGB(*self.gold_color, 0.5)
            c.circle((page_width - line_width)/2 - 0.15*inch, footer_y + 0.2*inch, 0.08*inch, fill=True, stroke=False)
            c.circle((page_width + line_width)/2 + 0.15*inch, footer_y + 0.2*inch, 0.08*inch, fill=True, stroke=False)
            
        elif self.artistic_style == "sketch":
            # 素描風格頁腳
            # 手繪線條
            c.setStrokeColorRGB(*self.text_color, 0.4)
            c.setLineWidth(0.7)
            c.setDash([6, 3])
            c.line(page_width/2 - 1.5*inch, footer_y - 0.05*inch, page_width/2 + 1.5*inch, footer_y - 0.05*inch)
            c.setDash([])
            
            # 頁碼 - 手繪風格
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            page_text = f"頁 {page_number}"
            text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
            
            # 輕微旋轉
            c.saveState()
            c.translate(page_width/2, footer_y)
            rotation = random.uniform(-1.5, 1.5)
            c.rotate(rotation)
            c.drawString(-text_width/2, 0, page_text)
            c.restoreState()
            
        else:  # modern
            # 現代藝術頁腳
            # 簡潔幾何元素
            c.setFillColorRGB(*self.main_color, 0.7)
            rect_width = 0.15 * inch
            rect_height = 0.3 * inch
            c.rect(page_width/2 - rect_width/2, footer_y - rect_height/2, rect_width, rect_height, fill=True, stroke=False)
            
            # 頁碼 - 簡潔明確
            c.setFont('Myfont', 12)
            c.setFillColorRGB(*self.text_color, 1.0)
            page_text = f"{page_number}"
            text_width = pdfmetrics.stringWidth(page_text, 'Myfont', 12)
            c.drawString(page_width/2 + rect_width, footer_y, page_text)
        
        c.restoreState()

    def add_epilogue_page(self, c, title, page_width, page_height):
        """添加藝術風格後記頁"""
        c.showPage()
        
        # 藝術背景
        self.draw_canvas_texture(c, page_width, page_height)
        
        # 藝術框架
        self.draw_artistic_frame(c, page_width, page_height)
        
        c.saveState()
        
        if self.artistic_style == "watercolor":
            # 水彩風格結束頁
            
            # 中央飛濺效果
            for _ in range(40):
                x = page_width/2 + random.uniform(-3, 3) * inch
                y = page_height/2 + random.uniform(-2, 2) * inch
                size = random.uniform(0.1*inch, 0.5*inch)
                
                if random.random() < 0.7:
                    color_choice = self.main_color
                else:
                    color_choice = self.accent_color
                    
                opacity = random.uniform(0.05, 0.15)
                c.setFillColorRGB(*color_choice, opacity)
                c.circle(x, y, size, fill=True, stroke=False)
            
            # 標題區域
            c.setFillColorRGB(*self.main_color, 0.3)
            title_box_width = 6 * inch
            title_box_height = 2 * inch
            c.rect((page_width - title_box_width)/2, 
                  page_height/2 - title_box_height/2,
                  title_box_width, title_box_height, 
                  fill=True, stroke=False)
            
            # 結束語標題
            c.setFont('Myfont', 42)
            c.setFillColorRGB(*self.text_color, 1.0)
            epilogue_text = "藝術旅程的終點"
            text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 42)
            c.drawString((page_width - text_width)/2, page_height/2 + 0.5*inch, epilogue_text)
            
            # 副標題
            c.setFont('Myfont', 18)
            c.setFillColorRGB(*self.text_color, 0.9)
            subtitle = f"{title} · 完"
            text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 18)
            c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
            
        elif self.artistic_style == "oil":
            # 油畫風格結束頁
            
            # 中央裝飾區域
            c.setFillColorRGB(*self.main_color, 0.2)
            c.rect(2*inch, 2*inch, page_width-4*inch, page_height-4*inch, fill=True, stroke=False)
            
            # 金色邊框
            c.setStrokeColorRGB(*self.gold_color, 0.8)
            c.setLineWidth(3)
            c.rect(2.2*inch, 2.2*inch, page_width-4.4*inch, page_height-4.4*inch, stroke=True, fill=False)
            
            # 華麗角花裝飾
            for corner in [(2.2*inch, 2.2*inch), (page_width-2.2*inch, 2.2*inch),
                          (2.2*inch, page_height-2.2*inch), (page_width-2.2*inch, page_height-2.2*inch)]:
                cx, cy = corner
                c.setFillColorRGB(*self.gold_color, 0.7)
                # 繪製華麗角花
                for i in range(4):
                    angle = i * (math.pi/2)
                    if cx > page_width/2 and cy > page_height/2:  # 右上角
                        start_angle = math.pi
                    elif cx < page_width/2 and cy > page_height/2:  # 左上角
                        start_angle = math.pi * 1.5
                    elif cx < page_width/2 and cy < page_height/2:  # 左下角
                        start_angle = 0
                    else:  # 右下角
                        start_angle = math.pi/2
                        
                    petal_size = 0.4 * inch
                    for j in range(3):
                        petal_angle = start_angle + angle + (j-1)*0.2
                        px = cx + math.cos(petal_angle) * petal_size * (j+1)/3
                        py = cy + math.sin(petal_angle) * petal_size * (j+1)/3
                        psize = 0.08*inch * (3-j)/3
                        c.circle(px, py, psize, fill=True, stroke=False)
            
            # 結束語標題
            c.setFont('Myfont', 48)
            c.setFillColorRGB(*self.gold_color, 1.0)
            epilogue_text = "藝術之旅 圓滿落幕"
            text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 48)
            c.drawString((page_width - text_width)/2, page_height/2 + 0.5*inch, epilogue_text)
            
            # 副標題
            c.setFont('Myfont', 20)
            c.setFillColorRGB(1, 1, 1, 1.0)
            subtitle = f"{title} · 完成於 {datetime.now().strftime('%Y年%m月%d日')}"
            text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 20)
            c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
            
        elif self.artistic_style == "sketch":
            # 素描風格結束頁
            
            # 手繪風格邊框
            c.setStrokeColorRGB(*self.text_color, 0.6)
            c.setLineWidth(1.5)
            c.setDash([8, 4])
            margin = 1.5 * inch
            c.rect(margin, margin, page_width-2*margin, page_height-2*margin, stroke=True, fill=False)
            c.setDash([])
            
            # 手繪線條裝飾
            line_count = 15
            for i in range(line_count):
                c.setStrokeColorRGB(*self.text_color, 0.1)
                c.setLineWidth(random.uniform(0.5, 1.5))
                y = margin + (page_height-2*margin) * (i/line_count)
                c.line(margin, y, page_width-margin, y + random.uniform(-0.1*inch, 0.1*inch))
            
            # 中央白色區域
            c.setFillColorRGB(1, 1, 1, 0.8)
            center_margin = 3 * inch
            c.rect(center_margin, center_margin, page_width-2*center_margin, page_height-2*center_margin, fill=True, stroke=False)
            
            # 結束語標題 - 手繪風格
            c.saveState()
            c.translate(page_width/2, page_height/2 + 0.5*inch)
            rotation = random.uniform(-1, 1)
            c.rotate(rotation)
            
            c.setFont('Myfont', 36)
            c.setFillColorRGB(*self.text_color, 1.0)
            epilogue_text = "草稿完成"
            text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 36)
            c.drawString(-text_width/2, 0, epilogue_text)
            c.restoreState()
            
            # 副標題
            c.setFont('Myfont', 16)
            c.setFillColorRGB(*self.text_color, 0.8)
            subtitle = f"{title} · 手繪札記"
            text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 16)
            c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
            
            # 手繪簽名
            c.setStrokeColorRGB(*self.text_color, 0.7)
            c.setLineWidth(1.5)
            signature_x = page_width - 3*inch
            signature_y = 2*inch
            signature_width = 1.5*inch
            
            # 簡單的簽名曲線
            p=PDFPathObject()
            p.moveTo(signature_x, signature_y)
            p.curveTo(signature_x + 0.5*inch, signature_y + 0.2*inch,
                     signature_x + 1*inch, signature_y - 0.1*inch,
                     signature_x + signature_width, signature_y + 0.1*inch)
            c.drawPath(p, stroke=1, fill=0)  # 修改這行，用 drawPath 代替 stroke
            
        else:  # modern
            # 現代藝術風格結束頁
            
            # 幾何分區
            c.setFillColorRGB(*self.main_color, 0.15)
            c.rect(0, 0, page_width/2, page_height, fill=True, stroke=False)
            
            c.setFillColorRGB(*self.accent_color, 0.15)
            c.rect(page_width/2, 0, page_width/2, page_height/2, fill=True, stroke=False)
            
            c.setFillColorRGB(*self.gold_color, 0.15)
            c.rect(page_width/2, page_height/2, page_width/2, page_height/2, fill=True, stroke=False)
            
            # 中央白色區塊
            c.setFillColorRGB(1, 1, 1, 0.9)
            center_width = 6 * inch
            center_height = 3 * inch
            c.rect((page_width - center_width)/2, 
                  (page_height - center_height)/2,
                  center_width, center_height, 
                  fill=True, stroke=False)
            
            # 白色區塊邊框
            c.setStrokeColorRGB(*self.main_color, 0.8)
            c.setLineWidth(3)
            c.rect((page_width - center_width)/2, 
                  (page_height - center_height)/2,
                  center_width, center_height, 
                  fill=False, stroke=True)
            
            # 結束語標題
            c.setFont('Myfont', 42)
            c.setFillColorRGB(*self.main_color, 1.0)
            epilogue_text = "展覽閉幕"
            text_width = pdfmetrics.stringWidth(epilogue_text, 'Myfont', 42)
            c.drawString((page_width - text_width)/2, page_height/2 + 0.5*inch, epilogue_text)
            
            # 副標題
            c.setFont('Myfont', 18)
            c.setFillColorRGB(*self.text_color, 1.0)
            subtitle = f"{title} · 攝影集"
            text_width = pdfmetrics.stringWidth(subtitle, 'Myfont', 18)
            c.drawString((page_width - text_width)/2, page_height/2 - 0.3*inch, subtitle)
            
            # 日期標記
            c.setFont('Myfont', 14)
            c.setFillColorRGB(*self.text_color, 0.7)
            date_text = datetime.now().strftime('%Y/%m/%d')
            text_width = pdfmetrics.stringWidth(date_text, 'Myfont', 14)
            c.drawString((page_width - text_width)/2, page_height/2 - 0.8*inch, date_text)
            
            # 現代標誌
            c.setFillColorRGB(*self.main_color, 0.7)
            c.circle(page_width/2, (page_height - center_height)/2 - 0.5*inch, 0.15*inch, fill=True, stroke=False)
        print(self.artistic_style, "結束頁添加完成")
        c.restoreState()