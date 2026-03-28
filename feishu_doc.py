#!/usr/bin/env python3
"""创建飞书文档并上传内容"""
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
        return json.loads(resp.read()).get("tenant_access_token", "")

def create_doc(token, title):
    """创建飞书文档"""
    data = {"title": title}
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/docx/v1/documents",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        if result.get("code") == 0:
            return result["data"]["document"]["document_id"]
        raise Exception(f"Create doc failed: {result}")

def upload_image(token, doc_token, file_path):
    """上传图片到文档"""
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    
    with open(file_path, 'rb') as f:
        img_data = f.read()
    
    fname = os.path.basename(file_path)
    
    body = f"--{boundary}\r\n"
    body += f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'
    body += "Content-Type: image/png\r\n\r\n"
    
    parts = [
        body.encode(),
        img_data,
        f"--{boundary}--".encode()
    ]
    
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
        data=b"\r\n".join(parts),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        if result.get("code") == 0:
            return result["data"]["file_token"]
        raise Exception(f"Upload failed: {result}")

def insert_image_to_doc(token, doc_token, image_token):
    """在文档中插入图片"""
    blocks = [{
        "block_type": 6,  # Image block
        "image": {
            "width": 1080,
            "height": 1350,
            "token": image_token
        }
    }]
    
    data = {"children": blocks, "index": 0}
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def append_text_to_doc(token, doc_token, text):
    """向文档追加文本"""
    blocks = [{
        "block_type": 2,  # Text block
        "text": {
            "elements": [{"text_run": {"content": text, "text_element_style": {}}}],
            "style": {}
        }
    }]
    
    data = {"children": blocks}
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')
    
    print("Getting access token...")
    token = get_token()
    
    title = f"📈 GitHub趋势通讯 {date} | 小红书发布素材"
    print(f"Creating doc: {title}")
    doc_id = create_doc(token, title)
    print(f"✅ Doc created: {doc_id}")
    
    # 上传封面图
    cover_path = f"/root/newsletter/social/cover_{date}.png"
    post_path = f"/root/newsletter/social/post_{date}.png"
    
    if os.path.exists(post_path):
        print("Uploading post image...")
        img_token = upload_image(token, doc_id, post_path)
        print(f"✅ Image uploaded: {img_token}")
        result = insert_image_to_doc(token, doc_id, img_token)
        print(f"Image insert result: {result.get('code')}")
    
    if os.path.exists(cover_path):
        print("Uploading cover image...")
        img_token = upload_image(token, doc_id, cover_path)
        print(f"✅ Cover uploaded: {img_token}")
        insert_image_to_doc(token, doc_id, img_token)
    
    # 添加文案
    xhs_path = f"/root/newsletter/social/xiaohongshu_{date}.txt"
    if os.path.exists(xhs_path):
        print("Adding xiaohongshu text...")
        with open(xhs_path) as f:
            content = f.read()
        append_text_to_doc(token, doc_id, "\n\n=== 小红书文案 ===\n")
        append_text_to_doc(token, doc_id, content)
    
    print(f"\n🎉 完成！文档地址：https://.feishu.cn/docx/{doc_id}")
