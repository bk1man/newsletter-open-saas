#!/bin/bash
# Newsletter 生成脚本 - 每天早上 9 点跑
DATE=$(date +%Y-%m-%d)
mkdir -p /root/newsletter/output
LOG=/root/newsletter/cron.log

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"; }

log "Fetching GitHub trending..."
cd /root/newsletter
python3 github_trending_real.py "" 15 > trending_${DATE}.json 2>&1

log "Generating newsletter..."
python3 - << 'PYTHON'
import json, os
from datetime import datetime

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

# 预置高质量解读模板（GitHub Top 15 热门项目的标准解读）
INSIGHTS = {
    "codecrafters-io/build-your-own-x": "通过造轮子学编程 — 从零构建 Redis、Docker、Web服务器，动手理解核心技术的最佳实践。",
    "sindresorhus/awesome": "最大的 awesome 清单聚合 — 收录各编程领域的优质资源，是寻找工具和学习路径的一站式入口。",
    "freeCodeCamp/freeCodeCamp": "免费编程学习平台 — 涵盖前端、后端、数据科学全链路，零基础入门首选的开源学习社区。",
    "public-apis/public-apis": "免费 API 集合 — 收录数千个公共 API，分类清晰，是快速原型开发和小项目的宝藏资源库。",
    "EbookFoundation/free-programming-books": "免费编程书籍聚合 — 整理全球优质技术书籍，涵盖数十种语言，自学 CS 的利器。",
    "kamranahmedse/developer-roadmap": "开发者成长路线图 — 前端/后端/运维/DevOps 等方向的学习路径，职业规划必备指南。",
    "donnemartin/system-design-primer": "系统设计入门 — Amazon/Facebook 工程师整理的大规模系统设计知识，面试和架构学习必看。",
    "jwasham/coding-interview-university": "软件工程师学习计划 — 作者从零基础到入职 Amazon 的完整路径，算法和系统设计全覆盖。",
    "openclaw/openclaw": "你的私人 AI 助手 — 跨平台跨系统的开源 Agent 实现，一行命令跑起来 😄",
    "vinta/awesome-python": "Python 优质资源清单 — 整理 Python 生态最优秀的框架、库和工具，开发者必收藏。",
    "awesome-selfhosted/awesome-selfhosted": "自托管服务列表 — 替代 SaaS 的开源方案，从网盘到邮件全部自建，保护隐私。",
    "996icu/996.ICU": "程序员权益记录 — 记录 996 对开发者健康的影响，是互联网加班文化的标志性事件。",
    "practical-tutorials/project-based-learning": "实战教程精选 — 收录按项目学习的优质教程，通过实战快速上手新技术。",
    "facebook/react": "最流行的 UI 库 — 声明式组件化前端范式，生态最完善，现代前端开发基础技能。",
    "torvalds/linux": "改变世界的内核 — 全球最大开源项目，现代服务器和移动设备的基石，致敬 Linus。",
    "microsoft/vscode": "最受欢迎的编辑器 — 跨平台、插件丰富，是现代程序员的首选开发环境。",
    "tensorflow/tensorflow": "机器学习框架 — Google 开源的 ML 框架，学术和工业界最广泛使用的深度学习工具。",
    "python/cpython": "Python 官方实现 — Python 语言的官方运行时，深入理解 Python 必看源码。",
}

def get_insight(repo):
    name = repo.get("name", "")
    desc = repo.get("description", "")
    lang = repo.get("language", "")
    
    if name in INSIGHTS:
        return INSIGHTS[name]
    
    # Fallback: 用描述生成一句话
    if desc:
        # 清理 emoji 和特殊字符
        desc = desc.replace(":", " ").replace("-", " ").strip()
        if len(desc) > 60:
            desc = desc[:57] + "..."
        return desc
    return f"{lang} 领域的优质项目，值得关注。"

# 生成 newsletter
with open(f'/root/newsletter/output/newsletter_{date}.md', 'w', encoding='utf-8') as f:
    f.write(f"# 📈 GitHub 趋势通讯\n")
    f.write(f"**Turing's Weekly** | {date}\n\n")
    f.write(f"每日追踪 GitHub 热门项目，帮你发现值得关注的开源工具。\n\n")
    f.write("---\n\n")
    
    for r in repos:
        rank = r["rank"]
        stars_k = f'{r["stars"]/1000:.1f}k'
        insight = get_insight(r)
        
        f.write(f"## {rank}. [{r['name']}]({r['url']})\n")
        f.write(f"⭐ {stars_k} | 🐛 {r['language']}\n\n")
        f.write(f"{insight}\n\n")
    
    f.write("---\n\n")
    f.write(f"*由 图灵 (Turing) 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

print(f"Done: newsletter_{date}.md | {len(repos)} repos")
PYTHON

log "Newsletter generated successfully"