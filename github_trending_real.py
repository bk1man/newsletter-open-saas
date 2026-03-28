#!/usr/bin/env python3
"""真实 GitHub Trending 获取"""
import json, sys, urllib.request, urllib.parse
from datetime import datetime

def fetch_language_from_url(languages_url):
    """对于 language 为空的 repo，从 languages_url 获取实际语言分布，返回占比最大的"""
    req = urllib.request.Request(languages_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            langs = json.loads(resp.read())
            if langs:
                return max(langs, key=langs.get)
    except Exception:
        pass
    return "Unknown"

def get_trending(language="", limit=20):
    query = "stars:>100"
    if language:
        query += f" language:{language}"
    
    params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": limit})
    url = f"https://api.github.com/search/repositories?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            repos = []
            for i, r in enumerate(data.get("items", [])[:limit]):
                lang = r.get("language")
                if not lang:  # None or empty — 从 languages_url 补充
                    lang = fetch_language_from_url(r.get("languages_url", ""))
                if lang == "Unknown":  # languages_url 也是空的，认定为纯文档项目
                    lang = "Markdown"
                repos.append({
                    "rank": i+1, "name": r["full_name"], "stars": r["stargazers_count"],
                    "language": lang or "Unknown",
                    "description": r.get("description") or "",
                    "url": r["html_url"]
                })
            return repos
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else ""
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    data = get_trending(lang, limit)
    print(json.dumps({"language": lang or "all", "fetched_at": datetime.now().isoformat(), "repos": data}, ensure_ascii=False, indent=2))
