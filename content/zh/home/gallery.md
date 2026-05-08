---
# 野外条带 — 自动从 content/zh/fieldwork/*/index.md 拉取页面渲染卡片
# 新增故事：在 content/zh/fieldwork/ 下新建一个文件夹，放 featured.jpg 和 index.md
widget: blank
headless: true
active: true

weight: 85

title: 野外
subtitle: 模型之外，野外更有故事。

design:
  columns: '1'
---

{{< fieldwork-gallery sort="date" order="desc" resize="900x900" >}}
