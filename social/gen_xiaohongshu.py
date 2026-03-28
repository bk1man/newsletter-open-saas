#!/usr/bin/env python3
"""生成小红书风格内容 - V2版本"""
import json, os, random
from datetime import datetime

DATE = os.environ.get('DATE', datetime.now().strftime('%Y-%m-%d'))

# 读取今日 newsletter 数据
trending_file = f'/root/newsletter/trending_{DATE}.json'
repos = []
if os.path.exists(trending_file):
    with open(trending_file) as f:
        data = json.load(f)
        repos = data.get('repos', [])[:8]

# 项目深度解读（小红书风格）
XIAOHONGSHU_INSIGHTS = {
    "donnemartin/system-design-primer": "🏗️ 系统设计天花板！Amazon工程师整理的面试知识，学会了去大厂横着走~",
    "paperclipai/paperclip": "📝 AI直接生成UI界面！设计师要失业了？用嘴画图的时代来了！",
    "koala73/worldmonitor": "🌍 全球数据一览无余！这个数据可视化工具太炫酷了",
    "public-apis/public-apis": "🔌 程序员必备！收录5000+免费API，做项目再也不用造轮子",
    "EbookFoundation/free-programming-books": "📚 程序员必藏！全网最全的免费编程书籍清单",
    "karpathy/autoresearch": "🚗 无人驾驶的AI大脑！Karpathy新项目，代码开源可学",
    "HKUDS/nanobot": "🧪 香港大学出品！AI纳米机器人研究，学术前沿了解一下",
    "garrytan/gstack": "🚀 一个想法到完整项目！这个框架让开发快10倍",
    "affaan-m/everything-claude-code": "💻 Claude Code 正确用法！不是调API，是真正AI帮你写代码",
    "zeroclaw-labs/zeroclaw": "⚡ Rust写的高性能云工具！云原生新选择",
    "VoltAgent/awesome-openclaw-skills": "🔌 OpenClaw技能库！你的AI助手武装升级",
}

# 今日热词
HOT_TAGS = ["#程序员", "#GitHub", "#开源", "#AI工具", "#编程学习", "#效率神器"]

# 生成小红书内容
with open(f'/root/newsletter/social/xiaohongshu_{DATE}.txt', 'w', encoding='utf-8') as f:
    f.write("📈 GitHub 今日热门精选\n\n")
    f.write("═══════════════════════════════════\n")
    f.write("🗓️ 程序员必看，这些项目今天最火\n\n")
    f.write("═══════════════════════════════════\n\n")
    
    for i, repo in enumerate(repos[:6]):
        name = repo.get("name", "")
        stars = repo.get("stars", 0)
        stars_k = f'{int(stars)/1000:.1f}k' if isinstance(stars, (int, float)) else stars
        lang = repo.get("language", "📦")
        lang_emoji = {"Python": "🐍", "TypeScript": "🔷", "JavaScript": "📜", "Rust": "🦀", "Go": "🐹"}.get(lang, "📦")
        
        repo_short = name.split('/')[-1].replace('-', ' ').replace('_', ' ')
        insight = XIAOHONGSHU_INSIGHTS.get(name, f"🔥 {repo_short.title()}，程序员圈口碑项目，值得一看")
        
        f.write(f"🔴 {i+1}. {name}\n")
        f.write(f"   ⭐{stars_k} {lang_emoji} {lang}\n")
        f.write(f"   {insight}\n\n")
    
    f.write("───────────────────────────────────\n")
    f.write(f"{' '.join(random.sample(HOT_TAGS, 4))}\n\n")
    f.write("👉 关注我，每天发现优质开源项目！\n")

print(f"✅ 小红书内容生成完成: xiaohongshu_{DATE}.txt")
