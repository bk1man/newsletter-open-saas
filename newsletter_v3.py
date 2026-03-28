#!/usr/bin/env python3
"""Newsletter V3 - 每日动态内容生成器"""
import json, os, urllib.request, random
from datetime import datetime

DATE = os.environ.get('DATE', datetime.now().strftime('%Y-%m-%d'))
DAY_NUM = datetime.now().weekday()
DAY_NAME = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][DAY_NUM]

# ========== 数据源 ==========

def fetch_new_hot_projects():
    """获取新晋热门项目（2026年创建 + 高stars）"""
    try:
        url = "https://api.github.com/search/repositories"
        params = "q=created:>2026-01-01+stars:>5000&sort=stars&order=desc&per_page=8"
        req = urllib.request.Request(f"{url}?{params}", 
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return [{
                "name": r["full_name"],
                "stars": r["stargazers_count"],
                "lang": r.get("language") or "多种技术",
                "desc": r.get("description") or "优质开源项目",
                "url": r["html_url"],
                "created": r.get("created_at", "")[:10]
            } for r in data.get("items", [])[:8]]
    except Exception as e:
        return []

def fetch_lang_trending(lang):
    """获取特定语言的热门项目"""
    try:
        url = "https://api.github.com/search/repositories"
        params = f"q=language:{lang}+stars:>10000&sort=stars&order=desc&per_page=5"
        req = urllib.request.Request(f"{url}?{params}",
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return [{
                "name": r["full_name"],
                "stars": r["stargazers_count"],
                "lang": r.get("language") or lang,
                "desc": r.get("description") or "",
                "url": r["html_url"]
            } for r in data.get("items", [])[:5]]
    except:
        return []

# ========== 每日主题 ==========
DAILY_FOCUS = {
    0: ("🎨 AI创作", "探讨AI如何助力创意工作"),
    1: ("🛠️ 效率工具", "这些工具帮你每天省2小时"),
    2: ("🤖 Agent前沿", "看看AI Agent现在能做什么"),
    3: ("📱 开源APP", "把数据掌握在自己手里"),
    4: ("☁️ 云原生", "现代化部署和架构方案"),
    5: ("🧠 AI学习", "边学边练，加速成长"),
    6: ("🚀 新兴项目", "发现下一个独角兽"),
}

THEME_NAME, THEME_DESC = DAILY_FOCUS[DAY_NUM]

# ========== 精选解读 ==========
DEEP_INIGHTS = {
    "affaan-m/everything-claude-code": "**Claude Code 全攻略**：不是简单调用API，而是让AI真正帮你写代码。这个项目教你如何用好 Claude Code。",
    "karpathy/autoresearch": "**自动驾驶的AI大脑**：Andrej Karpathy 的新项目，探索自动驾驶感知系统的新范式。",
    "garrytan/gstack": "**开发栈一站式**：从一个点子到完整项目，这个框架帮你快速搭建现代应用。",
    "koala73/worldmonitor": "🌍 **全球数据监控**：实时追踪全球各类指标，数据可视化做得很炫酷。",
    "VoltAgent/awesome-openclaw-skills": "🔌 **OpenClaw技能库**：为OpenClaw量身定制的技能集合，让你的Agent更强大。",
    "HKUDS/nanobot": "🧪 **纳米机器人**：香港大学的研究项目，探索AI在微观尺度的应用。",
    "paperclipai/paperclip": "📝 **下一代UI设计**：用自然语言描述界面，AI帮你生成可交互的UI原型。",
    "zeroclaw-labs/zeroclaw": "⚡ **Rust新贵**：用Rust写的高性能云原生工具，值得关注。",
    # 补全其他常见项目
    "public-apis/public-apis": "🔌 **免费API大全**：收录数千个免费REST API，做小项目缺接口？来这就对了。",
    "EbookFoundation/free-programming-books": "📚 **编程书籍宝库**：整理全球优质技术书籍，涵盖数十种语言，自学CS的利器。",
    "donnemartin/system-design-primer": "🏗️ **系统设计入门**：Amazon/Facebook工程师整理的大规模系统设计知识，面试和架构学习必看。",
    "vinta/awesome-python": "🐍 **Python优质资源清单**：Web开发、数据科学、ML...Python生态最优秀的库和框架都帮你整理好了。",
    "awesome-selfhosted/awesome-selfhosted": "🖥️ **自托管服务列表**：替代SaaS的开源方案，从网盘到邮件全部自建，保护隐私。",
    "996icu/996.ICU": "⚠️ **程序员权益记录**：记录996对开发者健康的影响，是互联网加班文化的标志性事件。",
    "practical-tutorials/project-based-learning": "🎯 **实战教程精选**：收录按项目学习的优质教程，通过实战快速上手新技术。",
    "facebook/react": "⚛️ **最流行的UI库**：声明式组件化前端范式，生态最完善，现代前端开发基础技能。",
    "microsoft/vscode": "💻 **最受欢迎的编辑器**：跨平台、插件丰富，是现代程序员的首选开发环境。",
    "tensorflow/tensorflow": "🧮 **机器学习框架**：Google开源的ML框架，学术和工业界最广泛使用的深度学习工具。",
    "torvalds/linux": "🐧 **改变世界的内核**：全球最大开源项目，现代服务器和移动设备的基石。",
    "openclaw/openclaw": "🤖 **你的私人AI助手**：不是玩具，是一个真正能跑任务的Agent。跨平台跨系统，想在哪里跑就在哪里跑。",
    "codecrafters-io/build-your-own-x": "🔨 **学编程的正确方式**：与其死磕语法，不如亲手实现一遍。从零构建14种核心技术。",
    "sindresorhus/awesome": "📋 **程序员的知识宝库**：汇总了所有awesome清单，涵盖AI、JS、Python...找工具、找教程，来这就对了。",
    "freeCodeCamp/freeCodeCamp": "🎓 **零基础入门天堂**：免费、开源、社区驱动。前端、后端、数据科学...一条路走到黑。",
}

def get_deep_insight(name, desc):
    """获取深度解读，没有则生成通用中文"""
    if name in DEEP_INIGHTS:
        return DEEP_INIGHTS[name]
    # 生成通用中文描述
    if desc and desc != "null":
        # 清理英文描述，转成中文风格
        desc = desc.replace("A ", "").replace("An ", "").replace("The ", "")
        if len(desc) > 50:
            desc = desc[:47] + "..."
        return f"📌 {desc}"
    return "💡 值得关注的好项目，不妨一看。"

# ========== 主逻辑 ==========
print(f"📡 获取今日数据...")
all_repos = []

# 今天的新热门项目
new_projects = fetch_new_hot_projects()
all_repos.extend(new_projects)
print(f"  获取到 {len(new_projects)} 个新热门项目")

# 根据星期添加不同语言的趋势
langs = ["Python", "TypeScript", "Rust", "Go", "JavaScript"]
lang = langs[DAY_NUM % len(langs)]
lang_projects = fetch_lang_trending(lang)
# 去重
existing_names = {r["name"] for r in all_repos}
lang_projects = [p for p in lang_projects if p["name"] not in existing_names][:3]
all_repos.extend(lang_projects)
print(f"  补充 {len(lang_projects)} 个 {lang} 项目")

# 打乱顺序，保持新鲜感
random.shuffle(all_repos)
all_repos = all_repos[:8]

# 生成 newsletter
output_path = f'/root/newsletter/output/newsletter_{DATE}.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# 📈 GitHub 趋势通讯\n")
    f.write(f"**Turing's Weekly** | {DATE} | {DAY_NAME}\n\n")
    f.write(f"> **今日主题：** {THEME_NAME}  \n")
    f.write(f"> **编辑说：** {THEME_DESC}\n\n")
    f.write("---\n\n")
    
    for i, repo in enumerate(all_repos):
        stars_str = f'{repo["stars"]/1000:.1f}k' if repo["stars"] > 999 else str(repo["stars"])
        insight = get_deep_insight(repo["name"], repo.get("desc", ""))
        
        f.write(f"## {i+1}. [{repo['name']}]({repo['url']})\n")
        f.write(f"⭐ {stars_str} | 🐛 {repo['lang']}\n\n")
        f.write(f"{insight}\n\n")
        f.write("---\n\n")
    
    f.write(f"\n*由 图灵 (Turing) 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    f.write(f"\n📬 订阅 [Turing's Weekly](https://github.com/bk1man/newsletter-open-saas) | 🐙 投稿 [GitHub](https://github.com/bk1man/newsletter-open-saas)\n")

print(f"✅ V3 newsletter_{DATE}.md 生成完成 | {len(all_repos)} 个项目 | 主题: {THEME_NAME}")
