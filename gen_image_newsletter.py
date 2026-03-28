#!/usr/bin/env python3
"""用 Pillow 生成精美的微信图文长图"""
from PIL import Image, ImageDraw, ImageFont
import io, re, os, sys

# 颜色配置
COLORS = {
    'bg': (245, 242, 234),        # 米黄色背景
    'card_bg': (255, 255, 255),    # 白色卡片
    'header_bg': (26, 26, 46),     # 深蓝黑
    'header_text': (255, 255, 255),
    'title': (26, 26, 46),         # 深色标题
    'desc': (75, 85, 99),          # 灰色描述
    'stars': (245, 158, 11),       # 橙色 star
    'lang_bg': (238, 242, 255),    # 浅蓝背景
    'lang_text': (102, 126, 234),  # 蓝色文字
    'level_fire': (239, 68, 68),   # 红色 - 顶级热门
    'level_up': (245, 158, 11),   # 橙色 - 增长迅猛
    'level_star': (102, 126, 234), # 蓝色 - 值得关注
    'level_new': (16, 185, 129),   # 绿色 - 新晋项目
    'footer': (136, 136, 136),     # 灰色页脚
    'border': (229, 229, 229),     # 边框灰
}

# 尺寸配置
WIDTH = 680
PADDING = 24
CARD_RADIUS = 16
CARD_PADDING = 20

def load_font(size, bold=False):
    """加载中文字体"""
    font_paths = [
        '/usr/share/fonts/google-noto-vf/NotoSans-VF.ttf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def load_bold_font(size):
    """加载粗体字体"""
    font_paths = [
        '/usr/share/fonts/google-noto-vf/NotoSans-VF.ttf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return load_font(size)

def get_text_size(draw, text, font):
    """获取文本尺寸"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def rounded_rectangle(draw, xy, radius, fill, outline=None):
    """画圆角矩形"""
    x1, y1, x2, y2 = xy
    r = radius
    
    # 画主矩形
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill, outline=outline)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill, outline=outline)
    
    # 画四个角
    draw.pieslice([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=fill, outline=outline)

def draw_card(draw, y, title, desc, stars, lang, level_text, level_color):
    """画一个项目卡片"""
    card_h = 120
    x = PADDING
    w = WIDTH - PADDING * 2
    
    # 卡片背景
    rounded_rectangle(draw, [x, y, x + w, y + card_h], CARD_RADIUS, COLORS['card_bg'])
    
    # 左侧彩色边条
    draw.rectangle([x, y + CARD_RADIUS, x + 6, y + card_h - CARD_RADIUS], fill=level_color)
    
    # 标题
    font_title = load_bold_font(15)
    title_y = y + CARD_PADDING
    draw.text((x + CARD_PADDING, title_y), title[:40], font=font_title, fill=COLORS['title'])
    
    # 描述（两行）
    font_desc = load_font(13)
    desc_y = title_y + 28
    desc_lines = []
    words = desc.split()
    line = ''
    for word in words:
        test_line = line + ' ' + word if line else word
        if get_text_size(draw, test_line, font_desc)[0] < w - CARD_PADDING * 2 - 100:
            line = test_line
        else:
            if line:
                desc_lines.append(line)
            line = word
    if line:
        desc_lines.append(line)
    for i, line in enumerate(desc_lines[:2]):
        draw.text((x + CARD_PADDING, desc_y + i * 18), line, font=font_desc, fill=COLORS['desc'])
    
    # 底部标签
    bottom_y = y + card_h - 30
    
    # Star 标签
    star_text = f'⭐ {stars}'
    tw, th = get_text_size(draw, star_text, font_desc)
    draw.rounded_rectangle([x + CARD_PADDING, bottom_y - 4, x + CARD_PADDING + tw + 12, bottom_y + th], 10, COLORS['stars'], COLORS['stars'])
    draw.text((x + CARD_PADDING + 6, bottom_y), star_text, font=font_desc, fill=(255, 255, 255))
    
    # 语言标签
    lang_text = lang
    lx = x + CARD_PADDING + tw + 24
    ltw, _ = get_text_size(draw, lang_text, font_desc)
    draw.rounded_rectangle([lx, bottom_y - 4, lx + ltw + 12, bottom_y + th], 10, COLORS['lang_bg'], COLORS['lang_bg'])
    draw.text((lx + 6, bottom_y), lang_text, font=font_desc, fill=COLORS['lang_text'])
    
    # 等级标签
    lt_w, lt_h = get_text_size(draw, level_text, font_desc)
    lt_x = x + w - lt_w - 24
    draw.rounded_rectangle([lt_x, bottom_y - 4, lt_x + lt_w + 12, bottom_y + lt_h], 10, (*level_color, 30) if len(level_color) == 3 else level_color + (30,), level_color)
    draw.text((lt_x + 6, bottom_y), level_text, font=font_desc, fill=level_color)
    
    return card_h + 12  # 返回卡片高度 + 间距

def generate_newsletter_image(md_path, output_path):
    """生成图文长图"""
    
    # 读取内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析项目
    projects = []
    current = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            m = re.search(r'\[([^\]]+)\]', line)
            if m:
                if current:
                    projects.append(current)
                current = {'name': m.group(1), 'stars': '', 'lang': '', 'desc': ''}
        elif line.startswith('⭐ '):
            if current:
                parts = line.split('|')
                current['stars'] = parts[0].replace('⭐', '').strip()
                lang_m = re.search(r'🐛\s*(\w+)', line)
                if lang_m:
                    current['lang'] = lang_m.group(1)
        elif line and not line.startswith(('#', '─', '═', '*', '由', '📈', '每日')):
            if current and not current['desc']:
                current['desc'] = line
    if current:
        projects.append(current)
    
    # 计算图片高度
    header_h = 160
    footer_h = 80
    top_card_h = 130
    other_card_h = 80
    gap = 16
    
    other_count = max(0, len(projects) - 3)
    total_h = header_h + gap + top_card_h * min(3, len(projects)) + gap + other_card_h * other_count + gap + footer_h + 100
    
    # 创建图片
    img = Image.new('RGB', (WIDTH, total_h), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    y = PADDING
    
    # === 顶部标题区 ===
    header_y = y
    rounded_rectangle(draw, [PADDING, header_y, WIDTH - PADDING, header_y + header_h], 20, COLORS['header_bg'])
    
    font_small = load_font(13)
    font_large = load_bold_font(20)
    
    # 副标题
    subtitle = 'GitHub 项目太多，跟不过来？'
    tw, th = get_text_size(draw, subtitle, font_small)
    draw.text(((WIDTH - tw) // 2, header_y + 30), subtitle, font=font_small, fill=(255, 255, 255, 180))
    
    # 主标题
    title = '每日帮你筛选最值得关注的项目'
    tw, th = get_text_size(draw, title, font_large)
    draw.text(((WIDTH - tw) // 2, header_y + 55), title, font=font_large, fill=(255, 255, 255))
    
    # 日期
    date_text = '每周一更新 · 帮你每年节省 100+ 小时'
    tw, th = get_text_size(draw, date_text, font_small)
    draw.text(((WIDTH - tw) // 2, header_y + 90), date_text, font=font_small, fill=(255, 255, 255, 150))
    
    y = header_y + header_h + gap
    
    # === Top 3 项目 ===
    def star_level(stars_str):
        try:
            s = float(stars_str.replace('k', '').replace('K', ''))
            if s >= 400:
                return '🔥 顶级热门', COLORS['level_fire']
            elif s >= 200:
                return '📈 增长迅猛', COLORS['level_up']
            elif s >= 100:
                return '⭐ 值得关注', COLORS['level_star']
            else:
                return '🆕 新晋项目', COLORS['level_new']
        except:
            return '⭐ 值得关注', COLORS['level_star']
    
    for i, p in enumerate(projects[:3]):
        level_text, level_color = star_level(p['stars'])
        rank_emoji = ['🥇', '🥈', '🥉'][i]
        
        card_h = top_card_h
        x = PADDING
        w = WIDTH - PADDING * 2
        
        # 卡片背景 + 阴影
        draw.rounded_rectangle([x + 3, y + 3, x + w + 3, y + card_h + 3], CARD_RADIUS, (0, 0, 0, 30))
        rounded_rectangle(draw, [x, y, x + w, y + card_h], CARD_RADIUS, COLORS['card_bg'])
        
        # 左侧边条
        draw.rounded_rectangle([x, y + CARD_RADIUS, x + 6, y + card_h - CARD_RADIUS], 0, level_color)
        draw.rectangle([x, y + CARD_RADIUS, x + 3, y + card_h - CARD_RADIUS], fill=level_color)
        
        # 排名 + 标题
        font_title = load_bold_font(16)
        draw.text((x + CARD_PADDING + 36, y + CARD_PADDING), rank_emoji + ' ' + p['name'][:30], font=font_title, fill=COLORS['title'])
        
        # 描述
        font_desc = load_font(13)
        desc_y = y + CARD_PADDING + 30
        words = p['desc'].split()
        line = ''
        lines = []
        for word in words:
            test = line + ' ' + word if line else word
            if get_text_size(draw, test, font_desc)[0] < w - CARD_PADDING * 2 - 120:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for li, l in enumerate(lines[:2]):
            draw.text((x + CARD_PADDING, desc_y + li * 18), l, font=font_desc, fill=COLORS['desc'])
        
        # 底部标签
        bottom_y = y + card_h - 35
        
        # Star（不需要再加k，markdown里已有）
        star_text = f'⭐ {p["stars"]}'
        sw, _ = get_text_size(draw, star_text, font_desc)
        draw.rounded_rectangle([x + CARD_PADDING, bottom_y, x + CARD_PADDING + sw + 16, bottom_y + 22], 11, COLORS['stars'])
        draw.text((x + CARD_PADDING + 8, bottom_y + 3), star_text, font=font_desc, fill=(255, 255, 255))
        
        # 语言
        lang_text = p['lang']
        lx = x + CARD_PADDING + sw + 28
        lw, _ = get_text_size(draw, lang_text, font_desc)
        draw.rounded_rectangle([lx, bottom_y, lx + lw + 16, bottom_y + 22], 11, COLORS['lang_bg'])
        draw.text((lx + 8, bottom_y + 3), lang_text, font=font_desc, fill=COLORS['lang_text'])
        
        # 等级标签
        lt_x = x + w - get_text_size(draw, level_text, font_desc)[0] - 24
        draw.rounded_rectangle([lt_x, bottom_y, lt_x + get_text_size(draw, level_text, font_desc)[0] + 16, bottom_y + 22], 11, level_color)
        draw.text((lt_x + 8, bottom_y + 3), level_text, font=font_desc, fill=(255, 255, 255))
        
        y += card_h + gap
    
    # === 其他项目 ===
    if len(projects) > 3:
        # 小标题
        font_s_title = load_bold_font(13)
        draw.text((PADDING, y + 5), '其他热门项目', font=font_s_title, fill=COLORS['footer'])
        y += 30
        
        for p in projects[3:]:
            level_text, level_color = star_level(p['stars'])
            
            card_h = other_card_h
            x = PADDING
            w = WIDTH - PADDING * 2
            
            # 卡片
            draw.rounded_rectangle([x, y, x + w, y + card_h], 12, COLORS['card_bg'])
            
            # 左侧边条
            draw.rectangle([x, y + 10, x + 4, y + card_h - 10], fill=level_color)
            
            # 标题
            font_title = load_bold_font(14)
            draw.text((x + 16, y + 12), p['name'][:35], font=font_title, fill=COLORS['title'])
            
            # 描述
            font_desc = load_font(12)
            desc = p['desc'][:40] + ('...' if len(p['desc']) > 40 else '')
            draw.text((x + 16, y + 34), desc, font=font_desc, fill=COLORS['desc'])
            
            # 右侧数据
            font_data = load_bold_font(13)
            star_text = f'{p["stars"]}'
            sw, _ = get_text_size(draw, star_text, font_data)
            lang_text = p['lang']
            lw, _ = get_text_size(draw, lang_text, font_desc)
            
            draw.text((x + w - sw - 8, y + 12), star_text, font=font_data, fill=COLORS['stars'])
            draw.text((x + w - lw - 8, y + 30), lang_text, font=font_desc, fill=COLORS['lang_text'])
            
            y += card_h + 8
    
    # === 页脚 ===
    y += 16
    draw.line([PADDING, y, WIDTH - PADDING, y], fill=COLORS['border'], width=1)
    y += 20
    
    font_footer = load_font(11)
    footer1 = '由 图灵 (Turing) 自动生成'
    tw, _ = get_text_size(draw, footer1, font_footer)
    draw.text(((WIDTH - tw) // 2, y), footer1, font=font_footer, fill=COLORS['lang_text'])
    
    y += 18
    footer2 = '每天 9:00 推送 · 每年帮你节省 100+ 小时'
    tw, _ = get_text_size(draw, footer2, font_footer)
    draw.text(((WIDTH - tw) // 2, y), footer2, font=font_footer, fill=COLORS['footer'])
    
    # 裁剪到实际内容
    img = img.crop((0, 0, WIDTH, y + 40))
    
    # 保存
    img.save(output_path, 'PNG', quality=95)
    print(f'✅ 图片已生成: {output_path}')
    print(f'   尺寸: {img.size}')

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else '2026-03-24'
    md_path = f'/root/newsletter/output/newsletter_{date}.md'
    output_path = f'/root/newsletter/social/newsletter_image_{date}.png'
    
    generate_newsletter_image(md_path, output_path)
