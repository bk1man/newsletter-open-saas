#!/usr/bin/env python3
"""Send newsletter via SendGrid"""
import os, sys, json
from datetime import datetime

def load_newsletter(date):
    path = f'/root/newsletter/output/newsletter_{date}.md'
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()

def build_email(content, date):
    """Build HTML email from markdown"""
    projects = []
    in_project = False
    current = {}
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            if current:
                projects.append(current)
            import re
            m = re.search(r'\[([^\]]+)\]', line)
            rm = re.match(r'##\s*(\d+)', line)
            current = {'rank': int(rm.group(1)), 'name': m.group(1) if m else '', 'url': ''}
            url_m = re.search(r'\((https?://[^\)]+)\)', line)
            if url_m:
                current['url'] = url_m.group(1)
        elif line.startswith('⭐ '):
            parts = line.split('|')
            current['stars'] = parts[0].replace('⭐ ', '').strip()
            if len(parts) > 1:
                current['lang'] = parts[1].replace('🐛', '').strip()
        elif line and not line.startswith(('#', '*', '---', '由', '每日')):
            if 'insight' not in current:
                current['insight'] = line
    if current:
        projects.append(current)
    
    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; background: #0d1117; color: #c9d1d9; padding: 40px 20px;">
      <h1 style="color: #f0f6fc; font-size: 24px; margin-bottom: 8px;">📈 GitHub 趋势通讯</h1>
      <p style="color: #8b949e; font-size: 14px; margin-bottom: 32px;">Turing's Weekly | {date}</p>
    """
    
    for p in projects:
        emoji = {'Python':'🐍','JavaScript':'🟨','TypeScript':'🔷','Go':'🐹','Rust':'🦀','C':'🔧','Java':'☕'}
        e = emoji.get(p.get('lang',''),'📦')
        html += f"""
      <div style="background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 16px;">
        <div style="font-size: 16px; font-weight: 600; color: #58a6ff; margin-bottom: 4px;">
          {p.get('rank','')}. <a href="{p.get('url','')}" style="color: #58a6ff;">{p.get('name','')}</a>
        </div>
        <div style="font-size: 13px; color: #8b949e; margin-bottom: 8px;">
          ⭐ {p.get('stars','')} | {e} {p.get('lang','')}
        </div>
        <div style="font-size: 14px; color: #c9d1d9; line-height: 1.6;">
          {p.get('insight','')}
        </div>
      </div>
    """
    
    html += f"""
      <div style="text-align: center; color: #6e7681; font-size: 12px; margin-top: 32px;">
        由 <a href="https://github.com/openclaw/openclaw" style="color: #58a6ff;">图灵 (Turing)</a> 自动生成 | {date}
      </div>
    </div>
    """
    return html

def send_via_sendgrid(api_key, to_email, subject, html_content):
    import urllib.request
    import urllib.parse
    
    data = json.dumps({
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "noreply@turing.news", "name": "Turing's Weekly"},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_content}]
    }).encode()
    
    req = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    api_key = os.environ.get('SENDGRID_API_KEY', '')
    
    content = load_newsletter(date)
    if not content:
        print(f"No newsletter for {date}")
        exit(1)
    
    html = build_email(content, date)
    
    if api_key:
        # Send to all subscribers
        with open('/root/newsletter/subscribe/subscribers.json') as f:
            subs = json.load(f)
        
        for sub in subs.get('subscribers', []):
            email = sub['email']
            try:
                status = send_via_sendgrid(api_key, email, f"📈 GitHub 趋势通讯 | {date}", html)
                print(f"Sent to {email}: {status}")
            except Exception as e:
                print(f"Failed to send to {email}: {e}")
    else:
        print("SENDGRID_API_KEY not set")
        # Just print preview
        print(html[:500])
