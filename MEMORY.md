
## 微信公众号模板规则
- 每天使用不同的 SVG + CSS 模板设计
- 保持：HTML + CSS内联 + SVG内联 结构
- 避免：emoji（可能有兼容性问题）
- 颜色和布局每天可以变化

## Pillow 图片生成注意事项（2026-03-24）
- emoji（⭐📈🐛等）在 NotoSans 字体里没有 glyph，会显示方块
- 解决方案：避免使用 emoji，改用纯文字 + 彩色标签
- Sir 已确认无 emoji 版本"可以看得过去"

## 微信公众号草稿类型（2026-03-25）
- 文章草稿：HTML内容，article_type不填
- 贴图草稿：多张图片，article_type="newspic"，配合image_info.image_list

关键参数：
{
  "article_type": "newspic",
  "image_info": {
    "image_list": [{"image_media_id": "..."}]
  }
}

## 2026-03-28 日常记录

### 今日完成
- [x] 修复语言 Unknown → Markdown（github_trending_real.py 加了 languages_url 回退逻辑）
- [x] 修复微信公众号 AppSecret（40125 → 正常token获取）
- [x] 推送 2026-03-28 公众号草稿（media_id: mIDVEOmq2z1Yy5W9e1RU0r9LoyKRzAtjkfaP5QIP5q1WmIcRdkganc-It6xRsAmZ）
- [x] 准备明天（2026-03-29）小红书内容：social/xiaohongshu_2026-03-29.txt + newsletter_image_2026-03-29.png
- [x] 发现 daily.sh 多次触发（9:00/14:35/15:09），建议优化为每日一次

### Newsletter 版本说明
- V1/V2: 15项目，简版描述
- V3: 8项目，深度中文解读（今日主力版本）
- V4: 带"今日主题/编辑说/本期速览"的新版格式

### 待解决
- [ ] daily.sh 每日多次触发问题（cron配置问题？）
- [ ] 微信公众号草稿推送后的群发（需确认发送时间）
- [ ] B2B AI客服/建站服务案例和报价（需 Sir 提供内容）
