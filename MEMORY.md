
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
