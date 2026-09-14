# 个人学术主页维护指南

本文档说明如何维护和更新你的个人学术主页，以及如何使用配套的自动化脚本。

## 📋 目录

1. [关键维护内容](#关键维护内容)
2. [维护脚本使用](#维护脚本使用)
3. [日常工作流程](#日常工作流程)
4. [配置文件说明](#配置文件说明)
5. [相关文档](#相关文档)

---

## 🔑 关键维护内容

### 1. 出版物管理（最重要）

**位置**: `content/en/publication/` 和 `content/zh/publication/`

**内容**:
- 每篇论文一个文件夹（文件夹名为 citation key）
- `index.md`: 论文元数据和摘要
- `cite.bib`: BibTeX 引用
- `*.pdf`: 论文 PDF 文件（可选）
- `featured.jpg/png`: 论文配图（可选）

**更新频率**: 每次发表新论文时

**维护脚本**:
```bash
# 1. 从 Zotero 导出 BibTeX 文件到根目录的 My-Publications.bib
# 2. 检查哪些论文还没有添加到网站
python scripts/check_missing_publications_enhanced.py My-Publications.bib --check-pdf

# 3. 为缺失的论文创建模板
python scripts/create_publication_template.py My-Publications.bib --dry-run  # 先预览
python scripts/create_publication_template.py My-Publications.bib             # 实际创建

# 4. 自动从 PDF 提取摘要（需要 OpenAI API Key）
python scripts/extract_abstract_from_pdf.py --max-publications 5  # 先测试几篇
python scripts/extract_abstract_from_pdf.py                       # 批量处理
```

**详细说明**: 参见 `scripts/README.md`

---

### 2. 个人信息

**位置**: `content/*/authors/admin/`

**文件**:
- `_index.md`: 个人简介、教育背景、研究兴趣、联系方式
- `avatar.jpg`: 头像照片

**更新频率**: 职位变动、新增荣誉、更新研究方向时

**示例内容**:
```yaml
---
title: Your Name
role: Your Position
organizations:
  - name: Your Institution
    url: "https://institution.edu"
bio: Short bio here
interests:
  - Research Area 1
  - Research Area 2
education:
  - course: PhD in Field
    institution: University
    year: 2020
social:
  - icon: envelope
    icon_pack: fas
    link: 'mailto:your@email.com'
  - icon: twitter
    icon_pack: fab
    link: https://twitter.com/yourhandle
---

Full biography here...
```

---

### 3. 首页内容

**位置**: `content/*/home/*.md`

**关键模块**:
- `hero.md`: 首页横幅
- `about.md`: 个人介绍卡片
- `experience.md`: 工作经历
- `skills.md`: 技能展示
- `accomplishments.md`: 荣誉奖项
- `publications.md`: 精选论文（自动从 publication 文件夹读取）
- `posts.md`: 博客文章列表
- `projects.md`: 研究项目展示
- `contact.md`: 联系方式

**更新频率**: 
- 工作经历: 职位变动时
- 荣誉奖项: 获奖时
- 其他: 根据需要

**提示**: 每个模块可以通过 `active: true/false` 控制是否显示

---

### 4. 博客文章

**位置**: `content/*/post/`

**结构**:
```
content/en/post/
├── my-first-post/
│   ├── index.md
│   ├── featured.jpg
│   └── other-images.jpg
```

**创建新博客**:
```bash
hugo new --kind post post/my-new-post
```

**更新频率**: 根据个人写作计划

---

### 5. 研究项目

**位置**: `content/*/project/`

**结构**:
```
content/en/project/
├── project-name/
│   ├── index.md
│   └── featured.jpg
```

**关键元数据**:
```yaml
---
title: Project Title
summary: Short description
tags:
  - Tag1
  - Tag2
date: "2024-01-01"
external_link: ""  # 或填写项目外部链接

# Optional
image:
  caption: Photo credit
  focal_point: Smart
links:
  - icon: github
    icon_pack: fab
    name: Code
    url: https://github.com/user/repo
---
```

**更新频率**: 启动新项目或项目完成时

---

### 6. 网站配置

**位置**: `config/_default/`

**关键文件**:
- `config.yaml`: 网站基本配置（标题、URL、主题等）
- `params.yaml`: 功能参数（评论系统、地图、统计等）
- `menus.yaml`: 导航菜单
- `languages.yaml`: 多语言设置

**常见修改**:
```yaml
# config.yaml
title: Your Name
baseURL: 'https://yourname.com/'

# params.yaml
theme: minimal  # 主题风格
day_night: true  # 日夜模式切换
highlight: true  # 代码高亮

# menus.yaml
main:
  - name: Home
    url: '#about'
    weight: 10
  - name: Publications
    url: '#publications'
    weight: 20
```

**更新频率**: 初始设置后很少修改

---

### 7. 静态资源

**位置**: 
- `assets/media/`: 网站图片（图标、背景等）
- `static/uploads/`: 用户上传的文件（PDF、数据等）

**常见文件**:
- `assets/media/icon.png`: 网站图标
- `static/uploads/pubs.pdf`: 完整发表列表（由 `make update-publist` 生成，勿手工替换）
- `static/uploads/SongshGeo_fullCV.pdf`: 完整学术简历（由 `make update-cv` 生成，勿手工替换）
- `static/uploads/Song_CV_2pages.pdf`: 两页精简版简历（手工维护，仓库内没有源文件）

前两个 PDF 的 LaTeX 源码分别在 `publist/` 和 `cv/`，共用根目录的 `My-Publications.bib`。
要改内容请改 `.tex` 再重新编译，直接替换 PDF 会在下次编译时被覆盖。

**更新频率**: 根据需要

---

## 🛠️ 维护脚本使用

本项目提供了一套自动化脚本来简化出版物管理。所有脚本位于 `scripts/` 目录。

### 安装依赖

```bash
# 使用 Poetry（推荐）
poetry install

# 安装 PDF 提取功能的额外依赖
poetry install --extras pdf-extraction

# 或使用 pip
pip install PyYAML
pip install langchain langchain-community langchain-openai openai pypdf python-dotenv
```

### 脚本概览

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `check_missing_publications_enhanced.py` | 检查缺失的论文，支持标题匹配和 PDF 检查 | 更新网站前 |
| `create_publication_template.py` | 自动创建论文页面模板 | 添加新论文 |
| `extract_abstract_from_pdf.py` | 从 PDF 自动提取摘要 | 批量补充摘要 |
| `check_missing_publications.py` | 基础版检查脚本 | 快速检查 |
| `check_site_integrity.py` | 本仓库自有代码的完整性检查 | `make test` / `make test-full`，CI 每个 PR 自动跑 |

### 详细使用方法

#### 1. 检查缺失的论文

```bash
# 基本检查
python scripts/check_missing_publications_enhanced.py My-Publications.bib

# 同时检查哪些论文没有 PDF
python scripts/check_missing_publications_enhanced.py My-Publications.bib --check-pdf

# 检查中文版本
python scripts/check_missing_publications_enhanced.py My-Publications.bib --lang zh

# 预览文件重命名（标准化 citation key）
python scripts/check_missing_publications_enhanced.py My-Publications.bib --renaming --dry-run

# 实际重命名文件
python scripts/check_missing_publications_enhanced.py My-Publications.bib --renaming
```

**输出说明**:
- ✅ **精确匹配**: citation key 完全匹配的论文
- ⚠️ **标题相似**: 可能是同一篇论文但 citation key 不同
- ❌ **真正缺失**: 需要创建页面的论文
- 📄 **缺少 PDF**: 已有页面但没有 PDF 文件

#### 2. 创建论文模板

```bash
# 先预览会创建什么（推荐）
python scripts/create_publication_template.py My-Publications.bib --dry-run

# 创建真正缺失的论文（默认行为）
python scripts/create_publication_template.py My-Publications.bib

# 创建所有缺失的论文（包括标题匹配的）
python scripts/create_publication_template.py My-Publications.bib --all

# 为中文版本创建
python scripts/create_publication_template.py My-Publications.bib --lang zh

# 强制覆盖已存在的文件夹（谨慎使用）
python scripts/create_publication_template.py My-Publications.bib --force
```

**生成的文件**:
```
content/en/publication/citation_key/
├── index.md     # 包含标题、作者、年份、DOI、摘要等
└── cite.bib     # 原始 BibTeX 引用
```

#### 3. 从 PDF 提取摘要

**准备工作**:
```bash
# 设置 OpenAI API Key
export OPENAI_API_KEY='sk-your-key-here'

# 或创建 .env 文件
echo 'OPENAI_API_KEY=sk-your-key-here' > .env
```

**使用方法**:
```bash
# 先测试单个论文
python scripts/extract_abstract_from_pdf.py --key wang2025g --dry-run

# 实际处理
python scripts/extract_abstract_from_pdf.py --key wang2025g

# 批量处理（建议先限制数量）
python scripts/extract_abstract_from_pdf.py --max-publications 5

# 处理所有论文
python scripts/extract_abstract_from_pdf.py

# 强制重新提取（覆盖已有摘要）
python scripts/extract_abstract_from_pdf.py --force

# 使用更好的模型
python scripts/extract_abstract_from_pdf.py --model gpt-4o
```

**费用参考**:
- `gpt-4o-mini` (默认): ~$0.0001-0.0003/篇
- `gpt-4o`: ~$0.001-0.003/篇
- `gpt-3.5-turbo`: ~$0.00005/篇

**更多细节**: 参见 `scripts/README.md`

---

## 🔄 日常工作流程

### 场景 1: 发表新论文

```bash
# 1. 在 Zotero 中添加新论文
# 2. 导出 BibTeX
#    File -> Export Library -> Format: BibTeX -> Save as My-Publications.bib

# 3. 检查缺失
python scripts/check_missing_publications_enhanced.py My-Publications.bib --check-pdf

# 4. 创建模板
python scripts/create_publication_template.py My-Publications.bib --dry-run
python scripts/create_publication_template.py My-Publications.bib

# 5. 添加 PDF 文件
#    将 PDF 复制到 content/en/publication/citation_key/ 目录

# 6. 提取摘要（如果有 PDF）
python scripts/extract_abstract_from_pdf.py --key citation_key

# 7. 完善信息
#    - 检查并编辑 index.md
#    - 添加 featured.jpg（可选）
#    - 设置 tags 和 categories

# 8. 预览
hugo server

# 9. 提交
git add content/en/publication/citation_key/
git commit -m "Add new publication: Citation Key"
git push
```

### 场景 2: 批量补充摘要

```bash
# 1. 确保 PDF 文件都已添加
python scripts/check_missing_publications_enhanced.py My-Publications.bib --check-pdf

# 2. 设置 API Key
export OPENAI_API_KEY='sk-your-key-here'

# 3. 先测试几篇
python scripts/extract_abstract_from_pdf.py --max-publications 3 --dry-run

# 4. 批量处理（建议分批）
python scripts/extract_abstract_from_pdf.py --max-publications 10

# 5. 检查结果
git diff content/en/publication/

# 6. 如果满意，继续处理剩余的
python scripts/extract_abstract_from_pdf.py

# 7. 提交
git add content/en/publication/
git commit -m "Auto-extract abstracts from PDFs"
git push
```

### 场景 3: 更新个人信息

```bash
# 1. 编辑个人信息
vim content/en/authors/admin/_index.md
vim content/zh/authors/admin/_index.md

# 2. 更新首页模块（如果需要）
vim content/en/home/experience.md
vim content/en/home/accomplishments.md

# 3. 预览
hugo server

# 4. 提交
git add content/*/authors/admin/ content/*/home/
git commit -m "Update personal information"
git push
```

### 场景 4: 发布新博客

```bash
# 1. 创建新博客
hugo new --kind post post/my-new-post

# 2. 编辑内容
vim content/en/post/my-new-post/index.md

# 3. 添加图片（可选）
cp ~/Downloads/image.jpg content/en/post/my-new-post/featured.jpg

# 4. 预览
hugo server

# 5. 提交
git add content/en/post/my-new-post/
git commit -m "Add new blog post: My New Post"
git push
```

---

## 📁 配置文件说明

### 网站配置层次结构

```
config/
└── _default/
    ├── config.yaml      # 核心配置（站点标题、URL、主题）
    ├── params.yaml      # 功能参数（评论、地图、统计、SEO）
    ├── menus.yaml       # 导航菜单
    └── languages.yaml   # 多语言设置
```

### 常用配置项

#### 1. 站点基本信息 (`config.yaml`)

```yaml
title: 'Your Name'
baseURL: 'https://yourname.com/'
copyright: '© {year} Your Name'
defaultContentLanguage: en
defaultContentLanguageInSubdir: false
```

#### 2. 主题和外观 (`params.yaml`)

```yaml
appearance:
  theme_day: minimal
  theme_night: minimal
  font: minimal
  font_size: L

features:
  syntax_highlighter:
    enable: true
    theme_light: github-light
    theme_dark: dracula
```

#### 3. 导航菜单 (`menus.yaml`)

```yaml
main:
  - name: Home
    url: '#about'
    weight: 10
  - name: Publications
    url: '#publications'
    weight: 20
  - name: Posts
    url: '#posts'
    weight: 30
```

#### 4. 多语言设置 (`languages.yaml`)

```yaml
en:
  languageCode: en-us
  title: Your Name
zh:
  languageCode: zh-Hans
  title: 你的名字
```

---

## 📚 相关文档

### 项目文档（`docs/` 目录）

| 文档 | 说明 |
|------|------|
| `MAINTENANCE_GUIDE.md` | 本文档，维护指南 |
| `QUICKSTART.md` | 快速开始指南 |
| `WORKFLOW.md` | 开发工作流程 |
| `DEPLOYMENT.md` | 部署说明 |
| `SETUP_COMPLETE.md` | 初始设置完成清单 |
| `README_check_publications.md` | 出版物检查脚本详细说明 |
| `SCRIPTS_CHANGELOG.md` | 脚本更新日志 |
| `LICENSE.md` | 许可证 |

### 脚本文档

| 文档 | 说明 |
|------|------|
| `scripts/README.md` | 脚本详细使用说明（推荐阅读） |

### 外部资源

- [Hugo Blox 官方文档](https://docs.hugoblox.com/)
- [Hugo 文档](https://gohugo.io/documentation/)
- [Academic CLI 工具](https://github.com/wowchemy/hugo-blox-builder)

---

## ⚙️ 维护清单

### 每次发表新论文
- [ ] 更新 `My-Publications.bib`
- [ ] 运行检查脚本
- [ ] 创建论文页面
- [ ] 添加 PDF 文件
- [ ] 提取或填写摘要
- [ ] 添加配图（可选）
- [ ] 提交并推送

### 每月检查
- [ ] 检查缺失的 PDF
- [ ] 更新个人简介（如有变化）
- [ ] 检查博客文章（如计划定期更新）
- [ ] 检查网站是否正常运行

### 每季度检查
- [ ] 更新工作经历
- [ ] 更新荣誉奖项
- [ ] 更新研究项目进展
- [ ] 检查并更新研究兴趣

### 每年检查
- [ ] 全面检查所有内容
- [ ] 更新头像和照片
- [ ] 审查并归档旧内容
- [ ] 备份整个网站

---

## 🆘 常见问题

### Q: 为什么有些论文显示但有些不显示？

A: 检查 `index.md` 中的 `draft: false` 和 `featured: true/false` 设置。

### Q: 如何修改首页显示的论文数量？

A: 编辑 `content/*/home/publications.md`，修改 `count` 参数。

### Q: 网站构建失败怎么办？

A: 
1. 检查 Hugo 版本: `hugo version`
2. 查看错误信息: `hugo server --verbose`
3. 检查 YAML 格式是否正确
4. 确保所有必需字段都已填写

### Q: 脚本运行出错怎么办？

A:
1. 确认依赖已安装: `poetry install`
2. 检查 Python 版本: `python --version` (需要 3.8+)
3. 查看日志: `logs/publications.log`
4. 使用 `-v` 或 `--verbose` 参数查看详细信息

### Q: PDF 提取摘要不准确？

A:
1. 尝试更好的模型: `--model gpt-4o`
2. 手动检查并编辑生成的摘要
3. 如果 PDF 是扫描版，建议手动输入

---

## 💡 最佳实践

1. **定期备份**: 使用 Git 版本控制，定期推送到远程仓库
2. **先预览后提交**: 使用 `hugo server` 本地预览，确认无误后再推送
3. **使用脚本**: 充分利用自动化脚本，减少手动操作
4. **保持一致性**: 遵循命名规范和文件结构
5. **文档先行**: 修改前先查阅相关文档
6. **小步提交**: 每次只修改一个功能，及时提交
7. **测试充分**: 使用 `--dry-run` 参数测试脚本
8. **监控成本**: 使用 OpenAI API 时注意费用

---

## 📞 需要帮助？

- 查看 `scripts/README.md` 了解脚本详细用法
- 查看 Hugo Blox 官方文档
- 查看项目 Git 历史了解修改示例
- 在 GitHub Issues 中搜索类似问题

---

**最后更新**: 2025-10-19

