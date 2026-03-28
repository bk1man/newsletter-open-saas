#!/usr/bin/env python3
import re, os, sys
from datetime import datetime

def parse_newsletter(date):
    path = f'/root/newsletter/output/newsletter_{date}.md'
    if not os.path.exists(path):
        return None
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
            current = {'rank': int(rm.group(1)), 'name': m.group(1) if m else ''}
        elif line.startswith('⭐ '):
            parts = line.split('|')
            current['stars'] = parts[0].replace('⭐ ', '').strip()
            if len(parts) > 1:
                current['lang'] = parts[1].replace('🐛', '').strip()
        elif line and not line.startswith(('#', '*', '---', '由')):
            if 'insight' not in current:
                current['insight'] = line
    if current and 'name' in current:
        projects.append(current)
    return projects

def to_xiaohongshu(projects, date):
    emoji = {'Python':'🐍','JavaScript':'🟨','TypeScript':'🔷','Go':'🐹','Rust':'🦀','C':'🔧','Ruby':'💎','Java':'☕'}
    out = [f"📈 GitHub 今日热门 TOP {len(projects)}\n",
           "═"*35, f"🗓️ {date} 程序员技术资讯\n", "═"*35 + "\n"]
    for i, p in enumerate(projects[:9], 1):
        e = emoji.get(p.get('lang',''),'📦')
        out.append(f"{'🔴' if i<=3 else '⚪'} {i}. {p['name']}")
        out.append(f"   ⭐{p.get('stars','')} {e} {p.get('lang','')}")
        out.append(f"   {p.get('insight','')[:55]}...\n")
    out += ["─"*35, "👉 关注我，每天发现优质开源项目！",
            "#程序员 #GitHub #开源 #技术资讯 #编程"]
    return '\n'.join(out)

def to_wechat(projects, date):
    out = [f"📈 GitHub 趋势通讯 | {date}\n", "═"*35 + "\n",
           "今日精选热门 GitHub 项目详细解读。\n"]
    for p in projects:
        out.append(f"{p.get('rank','')}. {p['name']}")
        out.append(f"   ⭐{p.get('stars','')} | 🐛{p.get('lang','')}\n")
        out.append(f"   {p.get('insight','')}\n")
    out += ["─"*35, f"由 图灵 自动生成 | {date}"]
    return '\n'.join(out)

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv)>1 else datetime.now().strftime('%Y-%m-%d')
    projects = parse_newsletter(date)
    if not projects: print("No newsletter"); exit(1)
    
    xhs = to_xiaohongshu(projects, date)
    open(f'/root/newsletter/social/xiaohongshu_{date}.txt','w').write(xhs)
    print("小红书 ✓")
    
    wc = to_wechat(projects, date)
    open(f'/root/newsletter/social/wechat_{date}.txt','w').write(wc)
    print("公众号 ✓")
    print("\n" + xhs)
