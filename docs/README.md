# 项目文档索引

本目录包含个人学术主页项目的所有文档。

## 📖 主要文档

### 🔧 维护和使用

| 文档 | 说明 | 推荐阅读顺序 |
|------|------|-------------|
| **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** | **维护指南（最重要）** - 日常维护、脚本使用、工作流程 | ⭐ 第一篇 |
| [QUICKSTART.md](QUICKSTART.md) | 快速开始 - 从零搭建网站 | 初次安装时 |
| [WORKFLOW.md](WORKFLOW.md) | 开发工作流程 - Git 工作流、分支策略 | 贡献代码时 |

### 📚 参考文档

| 文档 | 说明 |
|------|------|
| [README_check_publications.md](README_check_publications.md) | 出版物检查脚本的详细说明 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 部署指南 - 如何发布到生产环境 |
| [DOCS_DEPLOYMENT.md](DOCS_DEPLOYMENT.md) | 文档发布指南 - 如何发布文档到 GitHub Pages |
| [SETUP_COMPLETE.md](SETUP_COMPLETE.md) | 初始设置完成清单 |
| [SCRIPTS_CHANGELOG.md](SCRIPTS_CHANGELOG.md) | 脚本更新日志 |

### 📜 其他

| 文档 | 说明 |
|------|------|
| [LICENSE.md](LICENSE.md) | 项目许可证 |

## 🚀 快速链接

### 新手入门

如果你是第一次使用这个项目：

1. 阅读 [QUICKSTART.md](QUICKSTART.md) - 了解如何安装和初始化
2. 阅读 [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) - 了解如何日常维护
3. 查看 `../scripts/README.md` - 了解自动化脚本的详细用法

### 日常维护

如果你需要更新网站内容：

1. **添加新论文** → 参见 [MAINTENANCE_GUIDE.md - 场景 1](MAINTENANCE_GUIDE.md#场景-1-发表新论文)
2. **批量补充摘要** → 参见 [MAINTENANCE_GUIDE.md - 场景 2](MAINTENANCE_GUIDE.md#场景-2-批量补充摘要)
3. **更新个人信息** → 参见 [MAINTENANCE_GUIDE.md - 场景 3](MAINTENANCE_GUIDE.md#场景-3-更新个人信息)
4. **发布新博客** → 参见 [MAINTENANCE_GUIDE.md - 场景 4](MAINTENANCE_GUIDE.md#场景-4-发布新博客)

### 脚本使用

详细的脚本使用说明请查看：

- **脚本总览** → `../scripts/README.md`
- **维护指南中的脚本章节** → [MAINTENANCE_GUIDE.md - 维护脚本使用](MAINTENANCE_GUIDE.md#维护脚本使用)

## 📁 项目结构概览

```
SongshGeo-CV-site/
├── README.md                    # 项目主 README（在根目录）
├── docs/                        # 📚 本目录 - 所有文档
│   ├── README.md               # 本文件 - 文档索引
│   ├── MAINTENANCE_GUIDE.md    # ⭐ 维护指南（必读）
│   ├── QUICKSTART.md           # 快速开始
│   ├── WORKFLOW.md             # 开发工作流程
│   ├── DEPLOYMENT.md           # 部署指南
│   ├── SETUP_COMPLETE.md       # 设置完成清单
│   ├── README_check_publications.md  # 出版物检查说明
│   ├── SCRIPTS_CHANGELOG.md    # 脚本更新日志
│   └── LICENSE.md              # 许可证
├── scripts/                     # 🛠️ 维护脚本
│   ├── README.md               # 脚本详细说明（推荐阅读）
│   ├── check_missing_publications_enhanced.py
│   ├── create_publication_template.py
│   ├── extract_abstract_from_pdf.py
│   └── ...
├── content/                     # 📝 网站内容
│   ├── en/                     # 英文内容
│   │   ├── authors/            # 作者信息
│   │   ├── home/               # 首页模块
│   │   ├── publication/        # 出版物
│   │   ├── post/               # 博客文章
│   │   └── project/            # 研究项目
│   └── zh/                     # 中文内容（同上）
├── config/                      # ⚙️ 网站配置
│   └── _default/
│       ├── config.yaml         # 核心配置
│       ├── params.yaml         # 功能参数
│       ├── menus.yaml          # 导航菜单
│       └── languages.yaml      # 多语言
├── assets/                      # 🎨 资源文件
├── static/                      # 📦 静态文件
├── My-Publications.bib          # 📚 总 BibTeX 文件
└── ...
```

## 🎯 关键维护点

根据 [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)，需要定期维护的内容：

1. **出版物** (`content/*/publication/`) - 最重要，每次发表新论文时更新
2. **个人信息** (`content/*/authors/admin/`) - 职位变动时更新
3. **首页内容** (`content/*/home/`) - 根据需要更新
4. **博客文章** (`content/*/post/`) - 根据写作计划更新
5. **研究项目** (`content/*/project/`) - 新项目启动或完成时更新

## 🛠️ 维护脚本概览

| 脚本 | 功能 | 何时使用 |
|------|------|----------|
| `check_missing_publications_enhanced.py` | 检查缺失的论文 | 更新网站前 |
| `create_publication_template.py` | 创建论文页面模板 | 添加新论文 |
| `extract_abstract_from_pdf.py` | 从 PDF 提取摘要 | 批量补充摘要 |

详细用法请查看：
- `../scripts/README.md` - 完整的脚本文档
- [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) - 实际使用场景

## 💡 建议阅读路径

### 路径 1: 新用户（从零开始）

```
QUICKSTART.md → MAINTENANCE_GUIDE.md → scripts/README.md
```

### 路径 2: 日常维护

```
MAINTENANCE_GUIDE.md → scripts/README.md（需要时查阅）
```

### 路径 3: 贡献代码

```
WORKFLOW.md → MAINTENANCE_GUIDE.md → 相关技术文档
```

### 路径 4: 部署上线

```
SETUP_COMPLETE.md → DEPLOYMENT.md → DOCS_DEPLOYMENT.md
```

### 路径 5: 更新文档

```
DOCS_DEPLOYMENT.md（如何添加和发布文档）
```

## 📞 获取帮助

1. **查看相关文档** - 先在本目录和 `scripts/` 目录中查找
2. **查看 Git 历史** - 查看过往提交了解修改示例
3. **查看官方文档** - [Hugo Blox 文档](https://docs.hugoblox.com/)
4. **搜索问题** - 在 Hugo Blox GitHub Issues 中搜索

---

**提示**: 如果你只想快速了解如何维护网站，直接阅读 [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) 即可！

