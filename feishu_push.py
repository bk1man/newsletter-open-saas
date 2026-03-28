#!/usr/bin/env python3
"""每日飞书推送 - 将newsletter推送到用户"""
import json, urllib.request, urllib.parse, os, sys
from datetime import datetime

APP_ID = "cli_a91fd2195578dcc6"
APP_SECRET = "POSPeNTc1BTfEP9D5axPfeuZh8kG77wA"
USER_OPEN_ID = "ou_d0142c3276f28f0bdea6f604fac0c1e1"

def get_token():
    data = urllib.parse.urlencode({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        return result.get("tenant_access_token", "")

def send_text(token, open_id, content):
    data = {
        "receive_id": open_id,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def load_newsletter(date):
    path = f'/root/newsletter/output/newsletter_{date}.md'
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()

def format_for_feishu(content):
    import re
    lines = content.split('\n')
    msg_parts = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            m = re.search(r'\[([^\]]+)\]', line)
            rm = re.match(r'##\s*(\d+)\.', line)
            if m and rm:
                rank = rm.group(1)
                name = m.group(1)
                msg_parts.append(f"\n{'='*30}\n🔹 {rank}. {name}")
        elif line.startswith('⭐ '):
            parts = line.split('|')
            stars = parts[0].replace('⭐', '⭐').strip()
            lang = parts[1].replace('🐛', '').strip() if len(parts) > 1 else ''
            msg_parts.append(f"{stars} | 🐛 {lang}")
        elif line and not line.startswith(('#', '*', '---', '由', '每日', '📈')):
            if len(line) > 5:
                msg_parts.append(line[:80])
    
    header = "📈 **GitHub 趋势通讯**\nTuring's Weekly\n" + "="*30
    footer = "\n" + "="*30 + "\n由 图灵 自动生成 | 每天 9:00 推送"
    return header + '\n'.join(msg_parts) + footer

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    open_id = sys.argv[2] if len(sys.argv) > 2 else USER_OPEN_ID
    
    content = load_newsletter(date)
    if not content:
        print(f"[{datetime.now()}] No newsletter for {date}")
        exit(1)
    
    feishu_text = format_for_feishu(content)
    
    try:
        token = get_token()
        result = send_text(token, open_id, feishu_text)
        if result.get("code") == 0:
            print(f"[{datetime.now()}] ✅ Feishu push success to {open_id}")
        else:
            print(f"[{datetime.now()}] ❌ Feishu push failed: {result.get('msg')}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {e}")
