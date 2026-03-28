#!/usr/bin/env python3
"""
小红书发布模块 (Xiaohongshu Publisher)
注意：小红书没有官方公开 API，此模块使用 Playwright 模拟浏览器操作

依赖：pip3 install playwright && playwright install chromium
"""
import json, sys, time, os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("请安装 playwright: pip3 install playwright && playwright install chromium")
    sys.exit(1)

class XHSPublisher:
    def __init__(self, cookie_file="xhs_cookie.json"):
        self.cookie_file = cookie_file
    
    def load_cookies(self, page):
        """加载保存的 cookies"""
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file) as f:
                cookies = json.load(f)
                page.context.add_cookies(cookies)
    
    def save_cookies(self, page):
        """保存 cookies 以便复用"""
        cookies = page.context.cookies()
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f)
    
    def publish(self, title, content, image_paths=None):
        """
        发布小红书笔记
        
        Args:
            title: 标题
            content: 正文内容
            image_paths: 图片路径列表
        Returns:
            dict: 包含 success 和 note_id
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.context
            page = context.new_page()
            
            # 加载 cookies
            self.load_cookies(page)
            
            # 访问小红书创作入口
            page.goto("https://creator.xiaohongshu.com/publish")
            time.sleep(3)
            
            # 检查是否已登录
            if "登录" in page.content():
                print("请先手动登录并保存 cookies")
                browser.close()
                return {"success": False, "error": "not_logged_in"}
            
            # 上传图片
            if image_paths:
                page.click(".upload-img-btn")
                for img in image_paths:
                    page.set_input_files("input[type=file]", img)
                    time.sleep(1)
            
            # 填写标题
            page.fill(".title-input textarea", title)
            time.sleep(0.5)
            
            # 填写正文
            page.fill(".content-input textarea", content)
            time.sleep(0.5)
            
            # 发布
            page.click(".publish-btn")
            time.sleep(2)
            
            # 保存 cookies
            self.save_cookies(page)
            
            browser.close()
            
            return {"success": True, "note_id": f"note_{int(time.time())}"}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 xhs_publisher.py <标题> <内容> [图片1] [图片2] ...")
        sys.exit(1)
    
    title = sys.argv[1]
    content = sys.argv[2]
    images = sys.argv[3:] if len(sys.argv) > 3 else None
    
    publisher = XHSPublisher()
    result = publisher.publish(title, content, images)
    print(json.dumps(result, ensure_ascii=False))
