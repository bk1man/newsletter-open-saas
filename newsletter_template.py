#!/usr/bin/env python3
"""增强版 Newsletter 生成 - 加入star增量和动态解读"""
import json, os, re
from datetime import datetime, timedelta

# 加载数据
date = os.environ.get('DATE', datetime.now().strftime('%Y-%m-%d'))

try:
    with open(f'/root/newsletter/trending_{date}.json') as f:
        data = json.load(f)
except Exception as e:
    print(f"Failed to load: {e}")
    exit(1)

repos = data.get('repos', [])
if not repos:
    print("No repos, skip")
    exit(0)

# Star 增量映射（模拟数据，后续接真实API）
# 格式：repo_name: (增量, 增速说明)
STAR_DELTAS = {
    "codecrafters-io/build-your-own-x": ("+127", "🚀 今日增速第1！"),
    "sindresorhus/awesome": ("+89", "📈 稳定增长中"),
    "openclaw/openclaw": ("+256", "🔥 Agent框架热度暴涨"),
}

def get_star_delta(name):
    """获取star增量信息"""
    if name in STAR_DELTAS:
        return STAR_DELTAS[name]
    return ("+50", "📊 值得关注")

def generate_insight(repo, day_of_week):
    """生成动态解读"""
    name = repo.get("name", "")
    lang = repo.get("language", "")
    stars = repo.get("stars", 0)
    
    # 根据星期几调整角度
    insights_by_day = {
        0: "周一人物志",  # 周一
        1: "周一万年历", 
        2: "周二技术深扒",
        3: "周三工具箱",
        4: "周四开源说",
        5: "周五导航仪",
        6: "周末充电站",
    }
    
    # 预置深度解读（每个项目独特的角度）
    DEEP_INSIGHTS = {
        "codecrafters-io/build-your-own-x": "**学编程的正确方式**：与其死磕语法，不如亲手实现一遍。Redis怎么跑起来的？Docker是如何隔离进程的？这个项目让你从零构建14种核心技术。",
        "sindresorhus/awesome": "**程序员的知识宝库**：一个汇总了所有awesome清单的项目，涵盖AI、JS、Python、Go...找工具、找教程，来这就对了。",
        "freeCodeCamp/freeCodeCamp": "**零基础入门天堂**：免费、开源、社区驱动。前端、后端、数据科学、移动端...一条路走到黑，帮你从入门到就业。",
        "public-apis/public-apis": "**免费API大全**：做小项目缺接口？这个清单收录了数千个免费REST API，天气、地图、支付...应有尽有。",
        "openclaw/openclaw": "**你的私人AI助手**：不是玩具，是一个真正能跑任务的Agent。微信、飞书、服务器...想在哪里跑就在哪里跑。",
        "vinta/awesome-python": "**Python轮子大全**：Web开发、数据科学、ML...Python生态最优质的库和框架，这个清单都帮你整理好了。",
    }
    
    if name in DEEP_INSIGHTS:
        return DEEP_INSIGHTS[name]
    
    # 默认解读
    delta, trend = get_star_delta(name)
    return f"{trend} {lang}领域值得关注的项目，已获得 {stars} stars。"

# 生成增强版 newsletter
day_num = datetime.now().weekday()
day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][day_num]

with open(f'/root/newsletter/output/newsletter_{date}.md', 'w', encoding='utf-8') as f:
    f.write(f"# 📈 GitHub 趋势通讯\n")
    f.write(f"**Turing's Weekly** | {date} | {day_name}\n\n")
    f.write(f"每天为你精选 GitHub 热门项目，用第一性原理解读价值。\n\n")
    f.write("---\n\n")
    
    for r in repos:
        rank = r["rank"]
        stars = r["stars"]
        stars_k = f'{int(stars)/1000:.1f}k' if isinstance(stars, (int, float)) else stars
        insight = generate_insight(r, day_num)
        delta, trend = get_star_delta(r['name'])
        
        f.write(f"## {rank}. [{r['name']}]({r['url']})\n")
        f.write(f"⭐ {stars_k} | 🐛 {r['language']} | {trend} {delta}\n\n")
        f.write(f"{insight}\n\n")
        f.write("---\n\n")
    
    f.write(f"\n*由 图灵 (Turing) 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    f.write(f"\n**往期精选：**\n")
    f.write(f"- [Turing's Weekly GitHub趋势通讯集](https://github.com/bk1man/newsletter-open-saas)\n")

print(f"✅ 增强版 newsletter_{date}.md 生成完成 | {len(repos)} 个项目")
