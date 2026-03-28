#!/usr/bin/env python3
"""发布到微信公众号草稿箱 - HTML+CSS内联+SVG方案"""
import requests, json, io, re, sys
from datetime import datetime

APP_ID = "wx4bf0c5fd794ea6c6"
APP_SECRET = "01fc695af6ecc5c47b021c7a59ba9168"

def md_to_html(md_path):
    """HTML + CSS内联 + SVG图形"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析项目
    projects = []
    current = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            m = re.search(r'\[([^\]]+)\]', line)
            if m:
                if current:
                    projects.append(current)
                current = {'name': m.group(1), 'stars': '', 'lang': '', 'desc': ''}
        elif line.startswith('⭐ '):
            if current:
                parts = line.split('|')
                current['stars'] = parts[0].replace('⭐', '').strip()
                lang_m = re.search(r'🐛\s*(\w+)', line)
                if lang_m:
                    current['lang'] = lang_m.group(1)
        elif line and not line.startswith(('#', '─', '═', '*', '由', '📈', '每日')):
            if current and not current['desc']:
                current['desc'] = line
    if current:
        projects.append(current)
    
    def star_level(s):
        try:
            v = float(s.replace('k','').replace('K',''))
            if v >= 400: return 'HOT', '#ef4444', '#fef2f2'
            elif v >= 200: return 'UP', '#f59e0b', '#fffbeb'
            elif v >= 100: return 'NEW', '#10b981', '#ecfdf5'
            else: return 'NEW', '#10b981', '#ecfdf5'
        except: return 'NEW', '#10b981', '#ecfdf5'
    
    # SVG 顶部装饰
    svg_header = '''<svg viewBox="0 0 680 160" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;display:block;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="680" height="160" rx="16" fill="url(#headerGrad)"/>
  <text x="340" y="60" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13">GitHub 项目太多，跟不过来？</text>
  <text x="340" y="95" text-anchor="middle" fill="#ffffff" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="20" font-weight="700">每日帮你筛选最值得关注的项目</text>
  <text x="340" y="125" text-anchor="middle" fill="rgba(255,255,255,0.6)" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12">每周一更新</text>
</svg>'''
    
    html = f'''<html>
<head>
<meta charset="utf-8">
</head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',sans-serif;max-width:680px;margin:0 auto;padding:16px;background-color:#f5f2ea;">
{svg_header}
'''
    
    # Top 3 项目卡片
    for i, p in enumerate(projects[:3]):
        level_text, level_color, level_bg = star_level(p['stars'])
        
        # SVG排名 + 装饰
        svg_card = f'''<svg viewBox="0 0 680 130" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;display:block;margin:12px 0;">
  <defs>
    <filter id="shadow{i}" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="0.1"/>
    </filter>
  </defs>
  <rect x="4" y="4" width="672" height="122" rx="12" fill="#00000020" filter="url(#shadow{i})"/>
  <rect x="0" y="0" width="672" height="122" rx="12" fill="#ffffff"/>
  <rect x="0" y="12" width="6" height="98" rx="3" fill="{level_color}"/>
  <text x="24" y="32" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="14" font-weight="700" fill="#1a1a2e">TOP{i+1} {p['name']}</text>
  <rect x="580" y="16" width="76" height="24" rx="12" fill="{level_color}"/>
  <text x="618" y="33" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="11" font-weight="600" fill="#ffffff">{level_text}</text>
  <text x="24" y="60" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13" fill="#4b5563">{p['desc'][:50]}</text>
  <rect x="24" y="80" width="80" height="24" rx="4" fill="#fff7e6"/>
  <text x="34" y="97" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{p['stars']}k</text>
  <rect x="112" y="80" width="60" height="24" rx="4" fill="#eef2ff"/>
  <text x="122" y="97" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12" fill="#667eea">{p['lang']}</text>
</svg>'''
        html += svg_card
    
    # 其他项目
    if len(projects) > 3:
        html += '<p style="color:#888;font-size:13px;font-weight:600;margin:20px 0 12px 0;">其他热门项目</p>'
        
        for p in projects[3:]:
            level_text, level_color, level_bg = star_level(p['stars'])
            svg_item = f'''<svg viewBox="0 0 680 75" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;display:block;margin:8px 0;">
  <rect x="0" y="0" width="680" height="75" rx="10" fill="#ffffff"/>
  <rect x="0" y="10" width="4" height="55" rx="2" fill="{level_color}"/>
  <text x="16" y="28" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="14" font-weight="600" fill="#1a1a2e">{p['name'][:35]}</text>
  <text x="16" y="50" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12" fill="#6b7280">{p['desc'][:45]}</text>
  <text x="600" y="28" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{p['stars']}k</text>
  <text x="600" y="50" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="11" fill="#667eea">{p['lang']}</text>
</svg>'''
            html += svg_item
    
    # SVG 页脚
    svg_footer = '''<svg viewBox="0 0 680 80" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;display:block;margin-top:20px;">
  <line x1="16" y1="0" x2="664" y2="0" stroke="#e5e5e5" stroke-width="1"/>
  <text x="340" y="30" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12" fill="#667eea">由图灵(Turing)自动生成</text>
  <text x="340" y="55" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="11" fill="#aaa">每天9:00推送</text>
</svg>'''
    html += svg_footer + '</body></html>'
    
    return html

def get_token():
    r = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token',
        params={'grant_type': 'client_credential', 'appid': APP_ID, 'secret': APP_SECRET},
        timeout=10
    )
    return r.json().get('access_token')

def upload_thumb(token, img_path):
    with open(img_path, 'rb') as f:
        img_data = f.read()
    buffer = io.BytesIO(img_data)
    r = requests.post(
        'https://api.weixin.qq.com/cgi-bin/material/add_material',
        params={'access_token': token, 'type': 'image'},
        files={'media': ('cover.png', buffer, 'image/png')},
        timeout=30
    )
    result = r.json()
    if result.get('media_id'):
        return result['media_id']
    raise Exception(f'Upload failed: {result}')

def create_draft(token, title, html, thumb_media_id):
    json_data = {
        'articles': [{
            'title': title,
            'author': '图灵',
            'digest': '每日帮你筛选最值得关注的GitHub项目',
            'content': html,
            'thumb_media_id': thumb_media_id,
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }]
    }
    json_bytes = json.dumps(json_data, ensure_ascii=False).encode('utf-8')
    r = requests.post(
        'https://api.weixin.qq.com/cgi-bin/draft/add',
        params={'access_token': token},
        data=json_bytes,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=15
    )
    return r.json()

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    
    md_path = f'/root/newsletter/output/newsletter_{date}.md'
    img_path = '/root/newsletter/social/wechat_headline_final.png'
    
    print(f'[{datetime.now()}] Getting token...')
    token = get_token()
    
    print(f'[{datetime.now()}] Uploading cover...')
    thumb_id = upload_thumb(token, img_path)
    print(f'Thumb media_id: {thumb_id}')
    
    print(f'[{datetime.now()}] Creating draft...')
    html = md_to_html(md_path)
    print(f'HTML length: {len(html)}')
    
    result = create_draft(token, f'GitHub趋势通讯 {date}', html, thumb_id)
    
    if result.get('media_id'):
        print(f'✅ 草稿创建成功! media_id: {result["media_id"]}')
    else:
        print(f'❌ 失败: {result}')
