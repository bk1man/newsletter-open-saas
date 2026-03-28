# newsletter-open-saas

> AI-powered Newsletter & 小红书内容助手 — 开源版

## 功能

- 📊 自动抓取 GitHub Trending
- 📝 生成高质量 Newsletter
- 🎨 AI 封面图生成
- 📤 公众号草稿发布
- 📕 小红书文案 + 配图

## 快速开始

```bash
# 克隆
git clone https://github.com/YOUR_USERNAME/newsletter-open-saas.git
cd newsletter-open-saas

# 安装依赖
pip3 install -r requirements.txt

# 配置
cp config.example.py config.py
# 编辑 config.py 填入你的 API keys

# 运行
bash src/generate_newsletter.sh
```

## 目录结构

```
newsletter-open-saas/
├── src/
│   ├── github_trending_real.py  # GitHub Trending 采集
│   └── generate_newsletter.sh   # 生成脚本
├── templates/                    # 封面图模板
├── docs/                         # 文档
└── examples/                     # 示例输出
```

## 托管版（付费）

需要省心托管服务？访问我们的付费版：
- ¥199/月 — 个人版
- ¥499/月 — 专业版
- ¥999/月 — 团队版

## 许可证

MIT License
