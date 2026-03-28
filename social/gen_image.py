#!/usr/bin/env python3
"""生成小红书风格的技术封面图"""
import os, sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_cover(date, output_path):
    W, H = 1080, 1350
    
    # 背景渐变
    bg = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(bg)
    
    # 深色背景
    for y in range(H):
        ratio = y / H
        r = int(13 + ratio * 20)
        g = int(17 + ratio * 25)
        b = int(23 + ratio * 30)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # 顶部装饰条
    draw.rectangle([(0, 0), (W, 8)], fill=(88, 166, 255))
    
    # GitHub 风格的小图标区域（右上角）
    draw.rounded_rectangle([(W-120, 30), (W-30, 120)], radius=16, fill=(40, 44, 52))
    draw.text((W-90, 60), "GitHub", fill=(255, 255, 255))
    
    # 主标题
    draw.text((60, 180), "📈 GitHub", fill=(240, 246, 252))
    draw.text((60, 260), "趋势通讯", fill=(88, 166, 255))
    
    # 分隔线
    draw.rectangle([(60, 340), (W-60, 342)], fill=(48, 54, 61))
    
    # 副标题
    draw.text((60, 380), "Turing's Weekly", fill=(139, 148, 158))
    draw.text((60, 430), date, fill=(99, 110, 123))
    
    # 项目列表区域背景
    draw.rounded_rectangle([(40, 500), (W-40, 1200)], radius=20, fill=(22, 27, 34))
    
    # 项目列表
    projects = [
        ("1", "codecrafters-io/build-your-own-x", "⭐ 482.8k"),
        ("2", "sindresorhus/awesome", "⭐ 448.3k"),
        ("3", "freeCodeCamp/freeCodeCamp", "⭐ 438.8k"),
        ("4", "public-apis/public-apis", "⭐ 415.2k"),
        ("5", "kamranahmedse/developer-roadmap", "⭐ 351.6k"),
    ]
    
    emoji_map = {'Python':'🐍','JavaScript':'🟨','TypeScript':'🔷','Go':'🐹','Rust':'🦀','C':'🔧'}
    
    y = 530
    for i, (rank, name, stars) in enumerate(projects):
        color = (88, 166, 255) if i < 3 else (180, 190, 200)
        draw.text((70, y), f"#{rank}", fill=color)
        draw.text((120, y), name[:35], fill=(200, 210, 220))
        y += 45
        draw.text((120, y), stars, fill=(139, 148, 158))
        y += 70
    
    # 底部标签
    tags = ["#程序员", "#GitHub", "#开源", "#技术资讯"]
    tag_x = 60
    for tag in tags:
        draw.text((tag_x, 1240), tag, fill=(88, 166, 255))
        tag_x += 200
    
    # 底部提示
    draw.text((60, H-100), "👇 每天 9 点自动更新", fill=(99, 110, 123))
    
    bg.save(output_path, 'PNG', quality=95)
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    output = f'/root/newsletter/social/cover_{date}.png'
    create_cover(date, output)
