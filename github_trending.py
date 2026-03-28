#!/usr/bin/env python3
"""真实 GitHub Trending 抓取 - 抓取 github.com/trending 页面"""
import json, re, urllib.request, urllib.error
from datetime import datetime, timedelta

def get_trending(language="", limit=20):
    """抓取 GitHub Trending 页面"""
    url = "https://github.com/trending"
    if language:
        url = f"https://github.com/trending/{language}"
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        
        repos = []
        # 解析 trending 页面 - 查找 article 标签内的项目
        article_pattern = r'<article class="Box-row">.*?<h2 class="h3.*?<a href="/([^"]+)"[^>]*>([^<]+)</a>.*?<span class="text-normal">([^<]+)</span>.*?<p class="col-9 text-normal my-1 pr-4">([^<]+)</p>.*?<span class="d-inline-block float-sm-right">\s*([\d,]+)\s*</span>'
        
        matches = re.findall(article_pattern, html, re.DOTALL)
        
        for i, match in enumerate(matches[:limit]):
            repo_path = match[0]
            repo_name = match[1].strip()
            stars_str = match[4].strip().replace(',', '')
            
            # 获取描述 - 需要单独请求
            desc = ""
            
            repos.append({
                "rank": i + 1,
                "name": repo_path,
                "stars": stars_str,
                "language": language or "All",
                "description": desc,
                "url": f"https://github.com/{repo_path}"
            })
        
        return repos
        
    except Exception as e:
        return [{"error": str(e), "name": "fetch_failed"}]

def get_stars_delta(name):
    """获取项目的 star 增量（通过比较两次数据）"""
    return "+0"  # 简化处理，后续优化

if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else ""
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    
    repos = get_trending(lang, limit)
    data = {
        "language": lang or "all",
        "fetched_at": datetime.now().isoformat(),
        "repos": repos
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
