#!/usr/bin/env python3
"""生成小红书完整帖子图片（封面 + 项目详情）"""
import os, sys, re, json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def load_newsletter(date):
    path = f'/root/newsletter/output/newsletter_{date}.md'
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = f.readlines()
    
    projects, current = [], {}
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            if current and 'name' in current:
                projects.append(current)
            m = re.search(r'\[([^\]]+)\]', line)
            rm = re.match(r'##\s*(\d+)', line)
            current = {'rank': int(rm.group(1)) if rm else 0, 'name': m.group(1) if m else ''}
        elif line.startswith('⭐ '):
            parts = line.split('|')
            current['stars'] = parts[0].replace('⭐ ', '').strip()
            if len(parts) > 1:
                current['lang'] = parts[1].replace('🐛', '').strip()
        elif line and not line.startswith(('#', '*', '---', '由')):
            if 'insight' not in current:
                current['insight'] = line[:80]
    if current and 'name' in current:
        projects.append(current)
    return projects

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_cover(date, output_path, projects):
    W = 1080
    card_h = 900 if len(projects) > 10 else 800
    H = card_h + 450
    
    bg = Image.new('RGB', (W, H), (13, 17, 23))
    draw = ImageDraw.Draw(bg)
    
    # 顶部装饰
    draw.rectangle([(0, 0), (W, 6)], fill=(88, 166, 255))
    
    # 主标题
    draw.text((60, 60), "📈 GitHub 趋势通讯", fill=(240, 246, 252))
    draw.text((60, 130), f"Turing's Weekly  ·  {date}", fill=(88, 166, 255))
    draw.text((60, 180), "每日追踪热门开源项目，发现值得关注的技术工具", fill=(139, 148, 158))
    
    # 分隔线
    draw.rectangle([(60, 240), (W-60, 242)], fill=(48, 54, 61))
    
    # 项目卡片背景
    card_padding = 50
    card_top = 270
    draw.rounded_rectangle([(card_padding, card_top), (W-card_padding, H-card_padding-80)], 
                           radius=20, fill=(22, 27, 34))
    
    # 项目列表
    y = card_top + 30
    emoji_map = {'Python':'🐍','JavaScript':'🟨','TypeScript':'🔷','Go':'🐹','Rust':'🦀','C':'🔧','Ruby':'💎','Java':'☕'}
    
    for i, p in enumerate(projects[:9]):
        lang = p.get('lang', '')
        e = emoji_map.get(lang, '📦')
        rank = p.get('rank', i+1)
        
        color = (88, 166, 255) if i < 3 else (180, 190, 200)
        
        # 序号
        draw.text((80, y), f"#{rank}", fill=color)
        # 项目名
        name = p.get('name', '')[:38]
        draw.text((140, y), name, fill=(220, 225, 230))
        # stars
        stars = p.get('stars', '')
        draw.text((W-350, y), f"⭐ {stars}", fill=(139, 148, 158))
        y += 55
        
        # insight
        insight = p.get('insight', '')[:55]
        draw.text((140, y), f"  {insight}...", fill=(99, 110, 123))
        y += 50
    
    # 底部标签
    tags = ["#程序员", "#GitHub", "#开源", "#技术资讯", "#编程学习"]
    tx = 80
    for tag in tags:
        draw.text((tx, H-130), tag, fill=(88, 166, 255))
        tx += 200
    
    # 底部提示
    draw.text((80, H-80), "👇 每天 9:00 自动更新 | 完整数据见评论区", fill=(80, 90, 100))
    
    bg.save(output_path, 'PNG', quality=90)
    print(f"✅ Cover saved: {output_path} ({W}x{H})")

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    projects = load_newsletter(date)
    
    if not projects:
        print(f"No newsletter for {date}")
        exit(1)
    
    print(f"Loaded {len(projects)} projects")
    
    # 生成封面
    output = f'/root/newsletter/social/post_{date}.png'
    create_cover(date, output, projects)
