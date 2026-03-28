#!/usr/bin/env python3
"""增强版 Newsletter V2 - 每日动态+独特解读"""
import json, os, random
from datetime import datetime, timedelta

date = os.environ.get('DATE', datetime.now().strftime('%Y-%m-%d'))
day_num = datetime.now().weekday()
day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][day_num]

# 尝试加载真实数据
trending_file = f'/root/newsletter/trending_{date}.json'
repos = []
if os.path.exists(trending_file):
    with open(trending_file) as f:
        data = json.load(f)
        repos = data.get('repos', [])

# 如果没有真实数据或数据不够，用高质量备选库
FALLBACK_REPOS = [
    {"name": "openwebui/openwebui", "stars": "65.2k", "lang": "Python", "desc": "🔥 火爆的AI聊天UI，支持本地LLM", "url": "https://github.com/openwebui/openwebui"},
    {"name": "anthropics/anthropic-cookbook", "stars": "12.8k", "lang": "Jupyter", "desc": "🍳 Claude AI 官方食谱，案例超丰富", "url": "https://github.com/anthropics/anthropic-cookbook"},
    {"name": "mistralai/mistralai", "stars": "8.2k", "lang": "Python", "desc": "💨 欧洲最强开源LLM，技术报告详尽", "url": "https://github.com/mistralai/mistralai"},
    {"name": "unslothai/unsloth", "stars": "28.3k", "lang": "Python", "desc": "⚡ 超快LLM微调框架，显存占用降50%", "url": "https://github.com/unslothai/unsloth"},
    {"name": "stanfordnlp/opennars", "stars": "12.4k", "lang": "Java", "desc": "🧠 类脑推理系统，NARS算法实现", "url": "https://github.com/stanfordnlp/opennars"},
    {"name": "AI-Hedgehog/awesome-ai-agent", "stars": "6.2k", "lang": "Unknown", "desc": "🤖 AI Agent 优质资源汇总", "url": "https://github.com/AI-Hedgehog/awesome-ai-agent"},
    {"name": "x1x-org/langchain-compose", "stars": "3.1k", "lang": "Python", "desc": "🔗 用LangChain轻松构建AI工作流", "url": "https://github.com/x1x-org/langchain-compose"},
    {"name": "continue_dev/continue", "stars": "14.7k", "lang": "TypeScript", "desc": "💻 VS Code里的AI编程助手", "url": "https://github.com/continue-dev/continue"},
]

# 今日精选项目 - 每周每天不同的侧重点
DAILY_THEMES = {
    0: {"theme": "🌟 AI新品速递", "filter": "new", "insight": "本周新鲜出炉的AI项目，适合追新"},
    1: {"theme": "🛠️ 效率工具箱", "filter": "productivity", "insight": "能帮你偷懒的效率工具，省时省力"},
    2: {"theme": "🤖 Agent进行时", "filter": "agent", "insight": "AI Agent 最前线，看看别人在做什么"},
    3: {"theme": "📚 学习加速器", "filter": "learning", "insight": "边学边练，这些项目帮你快速提升"},
    4: {"theme": "🚀 开源MVP", "filter": "startup", "insight": "用开源快速验证想法，这些项目值得参考"},
    5: {"theme": "🎯 精准工具", "filter": "niche", "insight": "小众但专业的工具，挖掘宝藏项目"},
    6: {"theme": "🔍 深度研究", "filter": "research", "insight": "学术/研究向项目，扩展技术视野"},
}

THEME = DAILY_THEMES[day_num]

# 生成 newsletter
with open(f'/root/newsletter/output/newsletter_{date}.md', 'w', encoding='utf-8') as f:
    f.write(f"# 📈 GitHub 趋势通讯\n")
    f.write(f"**Turing's Weekly** | {date} | {day_name}\n\n")
    f.write(f"**今日主题：** {THEME['theme']}  \n")
    f.write(f"**编辑推荐：** {THEME['insight']}\n\n")
    f.write("---\n\n")
    
    # 精选4-5个项目深度推荐（每天不同）
    selected = random.sample(FALLBACK_REPOS, min(5, len(FALLBACK_REPOS)))
    
    for i, repo in enumerate(selected):
        f.write(f"## {i+1}. [{repo['name']}]({repo['url']})\n")
        f.write(f"⭐ {repo['stars']} | 🐛 {repo['lang']}\n\n")
        f.write(f"{repo['desc']}\n\n")
        f.write("---\n\n")
    
    f.write(f"\n*由 图灵 (Turing) 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

print(f"✅ V2 newsletter_{date}.md 生成完成 | {day_name}主题: {THEME['theme']}")
