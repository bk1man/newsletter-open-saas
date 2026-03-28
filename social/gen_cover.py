#!/usr/bin/env python3
"""专业级微信公众号头条封面图 v6 - 间距优化版"""
import os, sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    'primary': '#6366F1',
    'primary_dark': '#4F46E5',
    'accent': '#F59E0B',
    'accent_light': '#FCD34D',
    'bg_dark': '#060B18',
    'white': '#FFFFFF',
    'text_white': '#F8FAFC',
    'text_gray': '#94A3B8',
    'text_light': '#CBD5E1',
    'purple': '#8B5CF6',
    'cyan': '#06B6D4',
}

FONT_REGULAR = '/usr/share/fonts/google-noto-vf/NotoSans-VF.ttf'

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def hex_rgba(h, a=255):
    r, g, b = hex_rgb(h)
    return (r, g, b, a)

def draw_glow_soft(draw, cx, cy, rx, ry, color, intensity=40):
    for i in range(max(rx, ry), 0, -5):
        ratio = 1 - (i / max(rx, ry))
        alpha = int(intensity * ratio * ratio)
        r, g, b = hex_rgb(color)
        draw.ellipse([(cx-i, cy-i*ry//rx), (cx+i, cy+i*ry//rx)], fill=(r, g, b, alpha))

def get_text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def create_v6_headline(date, output_path):
    from PIL import ImageFont
    
    W, H = 900, 383
    SAFE_X, SAFE_Y = 258, 0
    SAFE_W, SAFE_H = 383, 383
    
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # ===== 字体 =====
    font_display = ImageFont.truetype(FONT_REGULAR, 72)   # GitHub
    font_title = ImageFont.truetype(FONT_REGULAR, 38)    # TRENDING
    font_sub = ImageFont.truetype(FONT_REGULAR, 28)      # NOW
    font_data = ImageFont.truetype(FONT_REGULAR, 56)     # 15
    font_data_label = ImageFont.truetype(FONT_REGULAR, 20) # Projects
    font_small = ImageFont.truetype(FONT_REGULAR, 16)     # 日期
    font_tag = ImageFont.truetype(FONT_REGULAR, 15)        # 标签
    
    # ===== 背景层 =====
    draw.rectangle([(0, 0), (W, H)], fill=hex_rgb(COLORS['bg_dark']))
    
    # 垂直渐变
    for y in range(H):
        ratio = y / H
        r = int(6 + ratio * 10)
        g = int(8 + ratio * 12)
        b = int(14 + ratio * 22)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # ===== 光效层 =====
    draw_glow_soft(draw, -80, 60, 350, 250, COLORS['primary'], 55)
    draw_glow_soft(draw, -80, 60, 200, 150, COLORS['purple'], 45)
    draw_glow_soft(draw, W+80, H-40, 250, 200, COLORS['cyan'], 40)
    draw_glow_soft(draw, W+60, H-60, 150, 120, COLORS['accent'], 35)
    
    # ===== 安全区 =====
    draw.rectangle([(SAFE_X, SAFE_Y), (SAFE_X+SAFE_W, SAFE_Y+SAFE_H)], 
                   fill=(5, 10, 20, 200))
    
    # 顶部渐变线
    for x in range(SAFE_W):
        ratio = x / SAFE_W
        r = int(99 + ratio * 20)
        g = int(102 + ratio * 30)
        b = int(241 + ratio * 20)
        draw.line([(SAFE_X+x, SAFE_Y), (SAFE_X+x, SAFE_Y+4)], fill=(r, g, b))
    
    cx = W // 2  # 450
    
    # ===== 日期标签 =====
    date_w = get_text_width(draw, date, font_small)
    tag_w, tag_h = date_w + 50, 34
    tag_x = cx - tag_w // 2
    tag_y = 25
    
    draw.rounded_rectangle([(tag_x, tag_y), (tag_x+tag_w, tag_y+tag_h)], 
                          radius=tag_h//2, fill=hex_rgba(COLORS['primary_dark'], 230))
    draw.text((cx - date_w//2, tag_y + 9), date, font=font_small, fill=hex_rgb(COLORS['text_gray']))
    
    # ===== 主标题 GitHub =====
    title_y = 78
    github_w = get_text_width(draw, "GitHub", font_display)
    draw.text((cx - github_w//2 + 3, title_y + 3), "GitHub", font=font_display, 
              fill=(20, 20, 40, 180))
    draw.text((cx - github_w//2, title_y), "GitHub", font=font_display, 
              fill=hex_rgb(COLORS['white']))
    
    # ===== TRENDING NOW =====
    trending_y = title_y + 85
    
    trending_w = get_text_width(draw, "TRENDING", font_title)
    draw.text((cx - trending_w//2, trending_y), "TRENDING", font=font_title, 
              fill=hex_rgb(COLORS['accent']))
    
    now_y = trending_y + 50
    now_w = get_text_width(draw, "NOW", font_sub)
    draw.text((cx - now_w//2, now_y), "NOW", font=font_sub, 
              fill=hex_rgb(COLORS['accent_light']))
    
    # ===== 分隔线 =====
    line_y = now_y + 55
    line_w = 140
    
    draw.rectangle([(cx - line_w - 15, line_y), (cx - 12, line_y + 2)], 
                   fill=hex_rgb(COLORS['primary']))
    draw.rectangle([(cx + 12, line_y), (cx + line_w + 15, line_y + 2)], 
                   fill=hex_rgb(COLORS['primary']))
    
    # 中心圆点
    draw.ellipse([(cx - 7, line_y - 6), (cx + 7, line_y + 8)], 
                fill=hex_rgb(COLORS['accent']))
    draw.ellipse([(cx - 3, line_y - 2), (cx + 3, line_y + 4)], 
                fill=hex_rgb(COLORS['accent_light']))
    
    # ===== 数据展示 - 间距拉大 =====
    data_y = line_y + 15  # 分隔线和数字的间距
    
    # 15 大数字
    num_text = "15"
    num_w = get_text_width(draw, num_text, font_data)
    draw.text((cx - num_w//2 + 2, data_y + 2), num_text, font=font_data, 
              fill=(20, 20, 40, 150))
    draw.text((cx - num_w//2, data_y), num_text, font=font_data, 
              fill=hex_rgb(COLORS['accent']))
    
    # Projects - 和数字保持舒适间距
    
    # ===== 底部标签 - 和 Projects 保持距离 =====
    tag_y = data_y + 100  # Projects 底部和标签的间距
    
    tags_data = [
        ("#GitHub", COLORS['primary']),
        ("#开源", COLORS['purple']),
        ("#技术", COLORS['cyan']),
    ]
    
    # 计算总宽度居中
    tag_widths = [get_text_width(draw, t, font_tag) + 56 for t, _ in tags_data]
    total_tags_w = sum(tag_widths) + 18 * 2  # 间距
    start_x = cx - total_tags_w // 2
    
    tx = start_x
    for tag_text, tag_color in tags_data:
        text_w = get_text_width(draw, tag_text, font_tag)
        cur_tag_w = text_w + 56
        
        draw.rounded_rectangle([(tx, tag_y), (tx + cur_tag_w, tag_y + 32)], 
                              radius=16, fill=hex_rgba(tag_color, 190))
        draw.rounded_rectangle([(tx+2, tag_y+2), (tx+cur_tag_w-2, tag_y+30)], 
                              radius=14, outline=hex_rgba(COLORS['white'], 25), width=1)
        draw.text((tx + (cur_tag_w - text_w)//2, tag_y + 9), tag_text, font=font_tag, 
                  fill=hex_rgb(COLORS['text_white']))
        tx += cur_tag_w + 18
    
    # ===== 署名 =====
    credit = "Powered by Turing AI"
    credit_w = get_text_width(draw, credit, font_small)
    draw.text((cx - credit_w//2, H - 25), credit, font=font_small, 
              fill=hex_rgba(COLORS['text_gray'], 120))
    
    # ===== 边缘暗角 =====
    for x in range(45):
        alpha = int(80 * (1 - x/45))
        for y in range(H):
            if x < W and y < H:
                current = img.getpixel((x, y))
                img.putpixel((x, y), (
                    max(0, current[0] - 25),
                    max(0, current[1] - 20),
                    max(0, current[2] - 40),
                    255
                ))
                current = img.getpixel((W-1-x, y))
                img.putpixel((W-1-x, y), (
                    max(0, current[0] - 25),
                    max(0, current[1] - 20),
                    max(0, current[2] - 40),
                    255
                ))
    
    img.save(output_path, 'PNG')
    print(f"✅ v6头条封面: {output_path}")

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    create_v6_headline(date, f'/root/newsletter/social/wechat_headline_{date}.png')
