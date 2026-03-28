#!/usr/bin/env python3
"""
Newsletter V4 - 提升内容质量的每日动态生成器
优化方向：
- 每天选择不同的项目（避免重复）
- 项目解读要有独特角度（不是翻译description）
- 加入"为什么值得关注"、"适合谁用"、"使用场景"
- 优化小红书文案生成
"""
import json, os, random, urllib.request
from datetime import datetime

DATE = os.environ.get('DATE', datetime.now().strftime('%Y-%m-%d'))
DAY_NUM = datetime.now().weekday()
DAY_NAME = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][DAY_NUM]

# ========== 数据源 ==========

def load_trending_data():
    """加载今日趋势数据"""
    trending_file = f'/root/newsletter/trending_{DATE}.json'
    if os.path.exists(trending_file):
        with open(trending_file) as f:
            data = json.load(f)
            return data.get('repos', [])
    return []

def fetch_new_hot_projects():
    """获取新晋热门项目（2026年创建 + 高stars）"""
    try:
        url = "https://api.github.com/search/repositories"
        params = "q=created:>2026-01-01+stars:>2000&sort=stars&order=desc&per_page=15"
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
            } for r in data.get("items", [])[:15]]
    except:
        return []

def fetch_lang_trending(lang, min_stars=5000):
    """获取特定语言的热门项目"""
    try:
        url = "https://api.github.com/search/repositories"
        params = f"q=language:{lang}+stars:>{min_stars}&sort=stars&order=desc&per_page=8"
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
            } for r in data.get("items", [])[:8]]
    except:
        return []

# ========== 每日主题 ==========
DAILY_FOCUS = {
    0: ("🎨 AI创作工具", "让AI成为你的创意伙伴，而不是替代品"),
    1: ("🛠️ 效率工具", "选对工具，每天多出2小时属于自己的时间"),
    2: ("🤖 AI Agent", "LLM元年开始，看Agent如何重塑工作流"),
    3: ("📱 开源APP", "把数据主权掌握在自己手里"),
    4: ("☁️ 云原生", "现代化架构的正确打开方式"),
    5: ("🧠 技术成长", "高效学习路径 vs 低效踩坑指南"),
    6: ("🚀 新兴项目", "早期参与，下一个独角兽的共建者"),
}

THEME_NAME, THEME_DESC = DAILY_FOCUS[DAY_NUM]

# ========== 精选解读库 V4 ==========
# 每个项目包含：独特角度、为什么值得关注、适合谁用、使用场景
DEEP_INIGHTS_V4 = {
    "codecrafters-io/build-your-own-x": {
        "angle": "不是学语法，是理解本质",
        "why": "看10遍教程不如自己实现一遍。这个项目教你从零构建Redis/Docker/Web服务器，真正搞懂底层原理。",
        "for_who": "想深入理解系统原理的开发者、准备技术面试的人、已经会用但想知道为什么的人",
        "scenario": "学习新技术时先看实现原理 / 面试前系统复习 / 想对某个系统有深入理解"
    },
    "sindresorhus/awesome": {
        "angle": "程序员的知识搜索引擎",
        "why": "awesome清单是业界公认的高质量资源汇总，比百度搜索靠谱100倍。",
        "for_who": "需要找工具/库/学习资源的任何开发者",
        "scenario": "接手新项目不知道用什么库 / 想学新领域不知道从哪里入门 / 找轮子时的第一站"
    },
    "freeCodeCamp/freeCodeCamp": {
        "angle": "零基础到就业，一条免费的路",
        "why": "课程体系完整，实战项目丰富，社区支持强。无数人靠它转行成功。",
        "for_who": "零基础想入门编程 / 想系统学习前端/后端/数据科学",
        "scenario": "每天2小时跟着课程做项目 / 用它来补足CS基础知识 / 作为简历上的实战项目"
    },
    "public-apis/public-apis": {
        "angle": "做小项目缺接口？这个清单救过你",
        "why": "收录5000+免费API，分类清晰，质量有筛选。做原型/POC必备。",
        "for_who": "独立开发者、正在做Side Project的人、想快速验证想法的学生",
        "scenario": "周末hackathon快速出原型 / 学习某个API时查文档 / 毕业设计缺数据源"
    },
    "EbookFoundation/free-programming-books": {
        "angle": "计算机经典书籍的免费版本汇总",
        "why": "很多经典书籍有免费英文版/中文翻译版，这个清单帮你找到它们。省下买书钱。",
        "for_who": "自学CS的学生、想系统提升的人、买书前想先看看电子版的人",
        "scenario": "想读某本经典但不想花钱 / 找某主题的最佳入门书籍 / 在地铁上用手机看"
    },
    "kamranahmedse/developer-roadmap": {
        "angle": "知道自己该学什么，比学什么更重要",
        "why": "技术路线图清晰标注了每个方向的学习顺序，避免盲目学了很多用不上的东西。",
        "for_who": "刚毕业或刚转行的开发者、想清晰规划学习路径的人",
        "scenario": "刚入职不知道该往哪个方向深耕 / 面试前想确认自己知识体系的完整性"
    },
    "donnemartin/system-design-primer": {
        "angle": "大厂面试题库，但更是架构设计教材",
        "why": "系统设计是中级开发者向高级跃迁的关键。这份资料帮你建立完整的大系统思维。",
        "for_who": "准备跳槽大厂的开发者、想学习分布式系统设计的人",
        "scenario": "准备系统设计面试 / 学习如何设计高并发系统 / 理解主流网站的架构思路"
    },
    "jwasham/coding-interview-university": {
        "angle": "非科班进Amazon的学习路径，可复制",
        "why": "作者用这个计划从零基础到入职Amazon。CS核心知识+算法+系统设计，路径清晰可执行。",
        "for_who": "非科班出身想进大厂的人、想系统补足CS基础的人",
        "scenario": "每天按计划执行学习任务 / 用Anki卡片刷算法 / 照着项目列表做实战"
    },
    "openclaw/openclaw": {
        "angle": "你的私人AI助手，想跑哪里跑哪里",
        "why": "开源AI Agent方案，跨平台支持，不是玩具而是真正能跑任务的生产力工具。",
        "for_who": "想用AI自动化任务的技术人员、想搭建自己AI助手的人",
        "scenario": "自动化日常重复工作 / 搭建团队内部的AI工作流 / 研究Agent架构"
    },
    "vinta/awesome-python": {
        "angle": "Python生态的精选导航",
        "why": "Python库太多，不知道哪个好？这个清单帮你筛选出最优选择，省去踩坑时间。",
        "for_who": "Python开发者、特别是不知道该选哪个框架的人",
        "scenario": "做Python项目不知道用什么库 / 想了解某个领域的最佳实践 / 快速概览Python生态"
    },
    "awesome-selfhosted/awesome-selfhosted": {
        "angle": "SaaS的免费替代方案，保护隐私",
        "why": "不想把数据交给大公司？这个清单收录了大量可自建的替代方案，从网盘到邮箱到笔记。",
        "for_who": "隐私优先的开发者、技术博主、想减少订阅费用的人",
        "scenario": "搭建自己的云服务 / 保护个人数据隐私 / 省钱（取消各种SaaS订阅）"
    },
    "996icu/996.ICU": {
        "angle": "互联网加班文化的里程碑事件",
        "why": "这个项目曾是GitHub上star增长最快的项目之一，见证了程序员权益意识的觉醒。",
        "for_who": "所有经历过或关心996问题的开发者",
        "scenario": "了解行业黑历史 / 作为程序员权益问题的讨论素材"
    },
    "practical-tutorials/project-based-learning": {
        "angle": "边做边学，比看教程有效10倍",
        "why": "每个教程都是围绕一个完整项目展开，学完就能做出真实可用的东西。",
        "for_who": "觉得看视频/文档太无聊的学习者、想快速出成果的人",
        "scenario": "选一个感兴趣的项目跟着做 / 用实战项目驱动学习 / 面试前快速过一遍某技术"
    },
    "facebook/react": {
        "angle": "前端开发的现代范式，生态最完善",
        "why": "不仅是库，更是现代前端开发的思维方式。掌握React就掌握了前端就业市场的硬通货。",
        "for_who": "前端开发者、想转行做前端的工程师",
        "scenario": "做React项目 / 理解组件化开发思想 / 学习现代前端工程化"
    },
    "torvalds/linux": {
        "angle": "一个人开始的传奇，现在运行着全球90%的服务器",
        "why": "向Linus Torvalds致敬。这个项目是现代互联网的基石，每一个程序员都在使用它。",
        "for_who": "所有程序员（都应该知道这个项目）",
        "scenario": "了解开源历史 / 学习内核设计思想 / 服务器开发必修"
    },
    "rust-lang/rust": {
        "angle": "让C/C++开发者既能保持性能，又能避免内存安全问题",
        "why": "连续多年被评为最受开发者喜爱的语言。Mozilla、Google、Microsoft都在用，Linux内核也开始支持Rust。",
        "for_who": "系统程序员、对性能和内存安全有要求的开发者、想学底层技术的人",
        "scenario": "重写系统工具 / WebAssembly开发 / 嵌入式开发 / 追求极致性能"
    },
    "EbookFoundation/free-programming-books": {
        "angle": "计算机经典书籍的免费版本汇总",
        "why": "很多经典书籍有免费英文版/中文翻译版，这个清单帮你找到它们。省下买书钱。",
        "for_who": "自学CS的学生、想系统提升的人、买书前想先看看电子版的人",
        "scenario": "想读某本经典但不想花钱 / 找某主题的最佳入门书籍 / 在地铁上用手机看"
    },
    "rustdesk/rustdesk": {
        "angle": "开源版TeamViewer，可以自己搭建的远程桌面",
        "why": "不想用收费的远程控制软件？自己部署，数据完全自主。Rust实现，延迟低，体验好。",
        "for_who": "需要远程控制的技术人员、注重隐私的用户、IT运维人员",
        "scenario": "远程办公 / 帮家人修电脑 / 自建远程桌面服务替代商业软件"
    },
    "garrytan/gstack": {
        "angle": "用好Claude Code的15个最佳实践，来自YC CEO Garry Tan",
        "why": "不是教你调API，而是教你如何真正用AI辅助编程。YC CEO的私人工作流，首次公开。",
        "for_who": "想用Claude Code提效的开发者、想了解AI编程最佳实践的人",
        "scenario": "刚装Claude Code不知道从哪开始 / 想提升AI编程效率 / 了解CEO级别的工具使用"
    },
    "koala73/worldmonitor": {
        "angle": "实时全球情报仪表盘，AI聚合全球资讯",
        "why": "把全球新闻用AI聚合，实时可视化。做舆情监控、市场调研的同学有福了。",
        "for_who": "做市场研究的人、舆情监控需求、新闻聚合爱好者",
        "scenario": "追踪行业动态 / 舆情监控系统搭建参考 / 数据可视化学习案例"
    },
    "karpathy/autoresearch": {
        "angle": "Karpathy新作：让AI agent自己搞研究",
        "why": "Andrej Karpathy（李飞飞学生、前Tesla AI总监）的新方向。AI agents自主做research，单GPU可跑。",
        "for_who": "AI研究员、对Agent架构感兴趣的人、想了解AI前沿方向的人",
        "scenario": "了解AI Agent最新研究方向 / 复现论文实验 / 学习自主AI系统设计"
    },
    "affaan-m/everything-claude-code": {
        "angle": "Claude Code性能优化系统，让AI真正帮你写代码",
        "why": "不是简单调用API，而是让Claude Code真正融入开发流程。包含skills、instincts等高级用法。",
        "for_who": "想深度使用Claude Code的开发者、正在搭建AI编程工作流的人",
        "scenario": "提升AI编程效率 / 学习Claude Code高级用法 / 搭建自己的AI coding助手"
    },
    "VoltAgent/awesome-openclaw-skills": {
        "angle": "OpenClaw技能库：5400+ skills，让你的Agent更强大",
        "why": "开源Agent框架OpenClaw的技能集合。涵盖各领域的AI操作能力，装机必备。",
        "for_who": "使用OpenClaw的用户、想扩展AI助手能力的人",
        "scenario": "给AI助手增加新技能 / 了解Agent能做到什么 / 找到某个具体任务的解决方案"
    },
}

# 通用解读生成器（当项目不在精选库中时）
def generate_generic_insight(repo):
    """为未知项目生成高质量通用解读"""
    name = repo.get("name", "")
    desc = repo.get("desc", "")
    lang = repo.get("lang", "")
    stars = repo.get("stars", 0)
    
    # 项目名简称
    short_name = name.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
    
    # 基于语言的特点描述
    lang_characteristics = {
        "Python": "Python生态",
        "TypeScript": "TypeScript技术栈",
        "JavaScript": "JavaScript技术栈",
        "Rust": "Rust系统编程",
        "Go": "Go云原生开发",
        "Java": "Java企业级开发",
        "C": "C系统底层",
        "C++": "C++高性能计算",
        "Swift": "SwiftApple生态",
        "Kotlin": "KotlinJVM开发",
        "多种技术": "跨技术栈",
    }
    
    char = lang_characteristics.get(lang, f"{lang}技术")
    
    # 清理描述（去除多余空格，截断到句子或合理长度）
    def clean_desc(d):
        if not d or d == "null":
            return ""
        d = d.strip()
        if len(d) > 60:
            # 尝试在自然断点截断
            for sep in ['. ', ' —', ' - ', ': ', '，', '。', ', ']:
                if sep in d[40:]:
                    cut = d[:40 + d[40:].index(sep) + len(sep)]
                    if len(cut) > 30:
                        return cut.strip()
            # 如果是长单词，在空格处截断
            if ' ' in d[50:60]:
                space_pos = d[50:60].index(' ') + 50
                return d[:space_pos].strip() + "..."
            return d[:57].strip() + "..."
        return d.strip()
    
    clean_d = clean_desc(desc)
    
    # 生成推荐理由
    why_keywords = []
    if stars > 100000:
        why_keywords.append("GitHub超级明星项目，社区活跃，值得深入研究")
    elif stars > 30000:
        why_keywords.append("高人气项目，经过大量开发者验证")
    else:
        why_keywords.append("增长迅速的新兴项目，可能有惊喜")
    
    desc_lower = desc.lower() if desc else ""
    if any(k in desc_lower for k in ["ai", "llm", "model", "agent", "gpt", "neural"]):
        why_keywords.append("涉及AI/ML领域，当前最热门方向之一")
    if any(k in desc_lower for k in ["tool", "cli", "util", "manage", "system"]):
        why_keywords.append("工具类项目，解决实际痛点")
    if any(k in desc_lower for k in ["open", "source", "free", "self-host"]):
        why_keywords.append("开源/免费，降低使用门槛")
    
    why_text = "；".join(why_keywords) if why_keywords else "有特色的技术项目，建议了解"
    
    # 适合谁
    if "python" in desc_lower or lang == "Python":
        for_who = "Python开发者、数据科学从业者、AI/ML工程师"
    elif "typescript" in desc_lower or "javascript" in desc_lower:
        for_who = "前端/全栈开发者、Node.js用户"
    elif "rust" in desc_lower or lang == "Rust":
        for_who = "系统程序员、对性能和安全性有要求的开发者"
    elif "go" in desc_lower or lang == "Go":
        for_who = "后端开发者、云原生工程师"
    else:
        for_who = f"{lang}技术栈开发者" if lang else "各类开发者"
    
    # 使用场景
    if stars > 100000:
        scenario = "作为技术选型的首选参考 / 面试技术深度时展开讨论 / 想了解某个领域最佳实践"
    elif "tool" in desc_lower or "cli" in desc_lower:
        scenario = "日常开发提效 / 自动化重复任务 / 快速搭建项目"
    else:
        scenario = "技术调研时的参考项目 / 学习某技术的实现思路 / 找灵感"
    
    return {
        "angle": f"{char}优质项目：{clean_d}" if clean_d else f"{char}领域的值得关注项目",
        "why": why_text,
        "for_who": for_who,
        "scenario": scenario
    }

def get_deep_insight_v4(repo):
    """获取V4版本的深度解读"""
    name = repo.get("name", "")
    if name in DEEP_INIGHTS_V4:
        return DEEP_INIGHTS_V4[name]
    return generate_generic_insight(repo)

# ========== 格式化输出 ==========

def format_stars(stars):
    """格式化stars数量"""
    if isinstance(stars, (int, float)):
        if stars >= 1000000:
            return f"{stars/1000000:.1f}M"
        elif stars >= 1000:
            return f"{stars/1000:.1f}k"
        return str(int(stars))
    return str(stars)

def format_newsletter_v4(repos, output_path):
    """生成V4版本的Newsletter"""
    with open(output_path, 'w', encoding='utf-8') as f:
        # 头部
        f.write(f"# 📈 GitHub 趋势通讯\n\n")
        f.write(f"**Turing's Weekly** | {DATE} | {DAY_NAME}\n\n")
        f.write(f"> **今日主题：** {THEME_NAME}  \n")
        f.write(f"> **编辑说：** {THEME_DESC}\n\n")
        f.write("---\n\n")
        
        # 导语
        f.write(f"## 🎯 本期速览\n\n")
        f.write(f"本期精选 **{len(repos)}** 个项目，涵盖 ")
        langs = set(r.get("lang", "") for r in repos if r.get("lang"))
        f.write(f"**{', '.join(sorted(l for l in langs if l))}** 等技术栈。\n")
        f.write(f"按阅读顺序，本期重点推荐：**{repos[0]['name'].split('/')[-1]}**、")
        f.write(f"**{repos[1]['name'].split('/')[-1]}**、**{repos[2]['name'].split('/')[-1]}**。\n\n")
        f.write("---\n\n")
        
        for i, repo in enumerate(repos):
            name = repo.get("name", "")
            stars = repo.get("stars", 0)
            lang = repo.get("lang", "📦")
            desc = repo.get("desc", "")
            url = repo.get("url", "")
            
            stars_str = format_stars(stars)
            insight = get_deep_insight_v4(repo)
            
            # 项目名称和基本信息
            f.write(f"## {i+1}. [{name}]({url})\n\n")
            f.write(f"⭐ **{stars_str}** | 🏷️ **{lang}**\n\n")
            
            # 核心解读（独特角度）
            f.write(f"**💡 怎么看：** {insight['angle']}\n\n")
            
            # 为什么值得关注
            f.write(f"**✨ 为什么值得关注：**\n{insight['why']}\n\n")
            
            # 适合谁用
            f.write(f"**🎯 适合谁：** {insight['for_who']}\n\n")
            
            # 使用场景
            f.write(f"**📍 常见场景：** {insight['scenario']}\n\n")
            
            f.write("---\n\n")
        
        # 底部
        f.write(f"\n## 📬 订阅与投稿\n\n")
        f.write(f"- 订阅：**Turing's Weekly**  \n")
        f.write(f"- 官网：https://github.com/bk1man/newsletter-open-saas  \n")
        f.write(f"- 投稿：在 GitHub 提交 Issue 或 PR\n\n")
        f.write(f"---\n\n")
        f.write(f"*由 图灵 (Turing) 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return output_path

# ========== 小红书文案生成 V4 ==========

XIAOHONGSHU_TEMPLATES = {
    "hook": [
        "程序员必看！GitHub今天最火的项目，第{}个太绝了",
        "收藏！GitHub高分项目清单，今天这{}个必须知道",
        "吐血整理！这{}个GitHub项目，我不允许你不知道",
        "程序员圈都在传！这个清单价值一套房",
        "GitHub今日热榜！这{}个项目，用过都说香",
    ],
    "repo_intro": [
        "{}，简直是{}的瑞士军刀！",
        "{}，用完再也回不去了😭",
        "{}，程序员必须了解的神器！",
        "{}，我已经用了一年了，真的香",
    ],
    "cta": [
        "👉 关注我，每天发现优质开源项目！",
        "🚀 关注我，带你发现更多宝藏项目",
        "⭐ 收藏起来慢慢看",
        "💬 评论区告诉我你最常用哪个？",
    ]
}

def generate_xiaohongshu_v4(repos, output_path):
    """生成小红书风格内容 V4"""
    with open(output_path, 'w', encoding='utf-8') as f:
        # 标题
        hook_template = random.choice(XIAOHONGSHU_TEMPLATES["hook"])
        f.write(f"📈 GitHub 今日热门精选\n\n")
        f.write(f"{'═' * 40}\n")
        f.write(f"{hook_template.format(len(repos[:6]))}\n")
        f.write(f"{'═' * 40}\n\n")
        
        f.write("▍ 程序员必藏 ⬇️\n\n")
        
        # 项目列表
        for i, repo in enumerate(repos[:6]):
            name = repo.get("name", "")
            stars = repo.get("stars", 0)
            lang = repo.get("lang", "")
            
            stars_str = format_stars(stars)
            lang_emoji = {"Python": "🐍", "TypeScript": "🔷", "JavaScript": "📜", 
                         "Rust": "🦀", "Go": "🐹", "Java": "☕", "C": "🔧",
                         "C++": "⚙️", "Swift": "🍎", "Kotlin": "🟣"}.get(lang, "📦")
            
            short_name = name.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
            insight = get_deep_insight_v4(repo)
            
            # 项目名
            f.write(f"🔴 {i+1}. {short_name}\n")
            f.write(f"   ⭐{stars_str} {lang_emoji}\n")
            
            # 核心价值（直接用angle，简洁有力）
            angle_short = insight['angle'][:40] + "..." if len(insight['angle']) > 40 else insight['angle']
            f.write(f"   💡 {angle_short}\n")
            
            # 适合谁/使用场景（二选一随机展示）
            if i % 2 == 0:
                for_who_short = insight['for_who'][:30] + "..." if len(insight['for_who']) > 30 else insight['for_who']
                f.write(f"   ✓ 适合：{for_who_short}\n")
            else:
                scenario_short = insight['scenario'][:30] + "..." if len(insight['scenario']) > 30 else insight['scenario']
                f.write(f"   ✓ 场景：{scenario_short}\n")
            
            f.write("\n")
        
        # 分隔
        f.write(f"{'─' * 40}\n\n")
        
        # 标签
        tags = ["#程序员", "#GitHub", "#开源", "#AI工具", "#编程学习", 
                "#效率神器", "#独立开发者", "#技术成长", "#宝藏网站", "#转码"]
        selected_tags = random.sample(tags, 5)
        f.write(f"{' '.join(selected_tags)}\n\n")
        
        # CTA
        cta = random.choice(XIAOHONGSHU_TEMPLATES["cta"])
        f.write(f"{cta}\n")

    return output_path

# ========== 主逻辑 ==========

print(f"📡 开始生成 V4 Newsletter...")
print(f"   日期: {DATE} | 星期: {DAY_NAME}")
print(f"   今日主题: {THEME_NAME} - {THEME_DESC}")

# 加载数据
all_repos = []
trending_repos = load_trending_data()
print(f"   加载到 {len(trending_repos)} 条趋势数据")

# 获取新项目
new_projects = fetch_new_hot_projects()
existing_names = {r["name"] for r in all_repos}
new_projects = [p for p in new_projects if p["name"] not in existing_names][:5]
all_repos.extend(new_projects)
print(f"   获取到 {len(new_projects)} 个新项目")

# 补充语言趋势（每周不重复的语言组合）
lang_combos = [
    ["Rust", "Go", "Python"],
    ["TypeScript", "Rust", "Go"],
    ["Python", "TypeScript", "JavaScript"],
    ["Go", "Python", "Rust"],
    ["JavaScript", "TypeScript", "Python"],
    ["Rust", "Python", "Go"],
    ["TypeScript", "Go", "Rust"],
]
langs = lang_combos[DAY_NUM]
for lang in langs[:2]:
    lang_projects = fetch_lang_trending(lang)
    existing_names = {r["name"] for r in all_repos}
    lang_projects = [p for p in lang_projects if p["name"] not in existing_names][:2]
    all_repos.extend(lang_projects)
    print(f"   补充 {len(lang_projects)} 个 {lang} 项目")

# 如果数据不够，补充trending数据
if len(all_repos) < 6:
    existing_names = {r["name"] for r in all_repos}
    for repo in trending_repos:
        if repo["name"] not in existing_names:
            all_repos.append(repo)
            if len(all_repos) >= 8:
                break

# 打乱顺序
random.shuffle(all_repos)
all_repos = all_repos[:8]

print(f"\n📝 最终选取 {len(all_repos)} 个项目：")
for r in all_repos:
    print(f"   - {r['name']} ({r.get('lang','?')}) ⭐{r.get('stars',0)}")

# 生成 newsletter
output_dir = '/root/newsletter/output'
os.makedirs(output_dir, exist_ok=True)
newsletter_path = f'{output_dir}/newsletter_{DATE}.md'
format_newsletter_v4(all_repos, newsletter_path)
print(f"\n✅ Newsletter 生成完成: {newsletter_path}")

# 生成小红书文案
social_dir = '/root/newsletter/social'
os.makedirs(social_dir, exist_ok=True)
xiaohongshu_path = f'{social_dir}/xiaohongshu_{DATE}.txt'
generate_xiaohongshu_v4(all_repos, xiaohongshu_path)
print(f"✅ 小红书文案生成完成: {xiaohongshu_path}")

print(f"\n📊 V4 Newsletter 生成完毕 | {len(all_repos)} 个项目 | 主题: {THEME_NAME}")
