from reportlab.lib.units import inch
# 基礎風格類
class BaseStyle:
    def __init__(self):
        self.photos_per_page = 4
        self.frame_padding = 0.1 * inch
        self.caption_height = 0.3 * inch
        
    def get_photo_position(self, photo_index, margin_left, margin_top, page_height, grid_width, grid_height, inner_margin, usable_width=None, usable_height=None, page_width=None, margin_right=None, margin_bottom=None):
        """計算照片位置 - 默認2x2網格佈局"""
        row = photo_index // 2
        col = photo_index % 2
        
        x = margin_left + col * grid_width + inner_margin
        y = page_height - margin_top - (row + 1) * grid_height + inner_margin
        
        return x, y, grid_width - 2*inner_margin, grid_height - 2*inner_margin
    
    def draw_error_placeholder(self, c, x, y, width, height, title):
        """繪製圖片載入錯誤時的預留位置"""
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(x, y, width, height, fill=True, stroke=False)
        c.setFont('Myfont', 12)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(x + width/2, y + height/2, "圖片載入錯誤")
        c.drawCentredString(x + width/2, y + height/2 - 20, title)