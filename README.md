# SongshGeo Academic CV Site

Personal academic CV website built with [Hugo](https://gohugo.io/) and [Hugo Blox Builder](https://hugoblox.com/).

## 🚀 Quick Start

### Install Dependencies

```bash
make install
```

### Development

```bash
# Start development server
make server

# Or with Hugo directly
hugo server --logLevel error --disableFastRender
```

### Build

```bash
make build
```

## 📚 Publication Management Workflow

This project includes an automated workflow for managing academic publications:

### Complete Update Workflow

```bash
# Run the full automated workflow
make full-update
```

This will interactively guide you through:
1. ✅ **Check** for duplicates and missing publications
2. 📄 **Check PDF** coverage
3. 📝 **Rename** cite.bib keys and PDF files to match citation keys
4. 🤖 **Extract abstracts** from PDFs using OpenAI
5. 📋 **Compile** publication list PDF
6. 📊 **Log** all changes

### Individual Steps

```bash
# 1. Check publication status
make check

# 2. Check which publications lack PDFs
make check-pdf

# 3. Preview file renaming (safe)
make preview-rename

# 4. Rename files to match citation keys
make rename

# 5. Extract abstracts from PDFs (requires OpenAI API key)
make extract-abstracts

# 6. Update publication list PDF
make update-publist
```

### Configuration

Before starting, ensure:

1. **BibTeX File**: Export your publications from Zotero/Mendeley to `My-Publications.bib` in the project root
2. **OpenAI API Key**: Set in `.env` file for abstract extraction:
   ```bash
   echo 'OPENAI_API_KEY=sk-your-key' > .env
   ```
3. **Publist Directory**: The `publist/` directory should be synced with Overleaf

## 🛠️ Available Make Targets

### Publication Management

| Command | Description |
|---------|-------------|
| `make check` | Check for duplicates/missing publications |
| `make check-pdf` | Check which publications lack PDFs |
| `make preview-rename` | Preview file renaming (cite.bib + PDFs) |
| `make rename` | Rename files to match citation keys |
| `make extract-abstracts` | Extract abstracts from PDFs using OpenAI |
| `make update-publist` | Compile publication list PDF |
| `make full-update` | Complete automated workflow |

### Development

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make server` | Start Hugo development server |
| `make build` | Build the site |
| `make clean` | Clean generated files |

### Deployment

| Command | Description |
|---------|-------------|
| `make status` | Show git status |
| `make commit` | Commit all changes with message |
| `make push` | Push to GitHub (triggers deployment) |
| `make deploy` | Quick deploy (commit + push) |

### Logs

| Command | Description |
|---------|-------------|
| `make show-log` | Show recent log entries |
| `make clean-logs` | Clean old log files (>3 months) |

## 📁 Project Structure

```
.
├── README.md               # This file - Project overview
├── My-Publications.bib     # Master BibTeX file (export from Zotero)
├── Makefile               # Build automation
├── docs/                   # 📚 All documentation
│   ├── README.md          # Documentation index
│   ├── MAINTENANCE_GUIDE.md  # ⭐ Maintenance guide (recommended)
│   ├── QUICKSTART.md      # Quick start guide
│   ├── WORKFLOW.md        # Development workflow
│   ├── DEPLOYMENT.md      # Deployment guide
│   └── ...                # Other documentation
├── scripts/                # 🛠️ Publication management scripts
│   ├── README.md          # Detailed script documentation
│   ├── check_missing_publications_enhanced.py
│   ├── create_publication_template.py
│   ├── extract_abstract_from_pdf.py
│   ├── logger_config.py   # Centralized logging
│   └── ...
├── content/                # 📝 Site content
│   ├── en/                 # English content
│   │   ├── publication/    # Publication pages
│   │   ├── post/          # Blog posts
│   │   ├── project/       # Research projects
│   │   └── ...
│   └── zh/                 # Chinese content (same structure)
├── config/                 # ⚙️ Hugo configuration
│   └── _default/
│       ├── config.yaml     # Core config
│       ├── params.yaml     # Feature parameters
│       ├── menus.yaml      # Navigation menus
│       └── languages.yaml  # Multi-language settings
├── publist/                # 📄 LaTeX publication list (Overleaf sync)
│   ├── main.tex
│   └── My-Publications.bib # Symlinked to root
├── static/uploads/         # 📦 Uploaded files
│   └── pubs.pdf           # Compiled publication list
├── logs/                   # 📋 Operation logs (auto-cleaned after 3 months)
├── assets/                 # 🎨 Theme assets
└── public/                 # 🌐 Generated site (not in Git)
```

## 📖 Documentation

### 项目文档

所有详细文档已整理到 `docs/` 目录，并发布到在线文档站点：

**📖 在线文档**: https://songshgeo.github.io/SongshGeo-as-Scholar/

**本地文档**:
- **⭐ [维护指南](docs/MAINTENANCE_GUIDE.md)** - 日常维护、脚本使用、工作流程（推荐阅读）
- **[文档索引](docs/README.md)** - 查看所有可用文档
- **[快速开始](docs/QUICKSTART.md)** - 从零搭建网站
- **[工作流程](docs/WORKFLOW.md)** - Git 工作流、分支策略
- **[部署指南](docs/DEPLOYMENT.md)** - 部署到生产环境
- **[文档发布](docs/DOCS_DEPLOYMENT.md)** - 如何发布文档到 GitHub Pages
- **[脚本说明](scripts/README.md)** - 详细的脚本使用文档

**本地预览文档**:
```bash
make docs-serve  # 访问 http://localhost:3000
```

### 外部资源

- **Hugo Blox Builder**: [Official Documentation](https://docs.hugoblox.com/)
- **Hugo**: [Official Documentation](https://gohugo.io/documentation/)

## 🔄 Typical Workflow

### When Adding New Publications

1. **Export BibTeX** from your reference manager to `My-Publications.bib`
2. **Run full update**:
   ```bash
   make full-update
   ```
3. **Review changes**:
   ```bash
   git diff
   ```
4. **Test locally**:
   ```bash
   make server
   ```
5. **Deploy**:
   ```bash
   make deploy
   ```

### Logs

All script operations are logged to `logs/publications.log` with:
- ✅ Automatic rotation (every 10MB)
- 📅 Retention policy (3 months)
- 🗜️ Compression of old logs

View recent logs:
```bash
make show-log
```

## 🔧 Dependencies

- **Hugo** >= 0.148.2
- **Go** >= 1.21
- **Python** >= 3.11
- **Poetry** (Python package manager)
- **XeLaTeX** (for compiling publication list)

Python packages (managed by Poetry):
- PyYAML
- loguru (logging)
- langchain, openai, pypdf (for PDF extraction)

## 🌐 Deployment

The site automatically deploys to GitHub Pages when you push to `main` or `dev` branch:

```bash
make deploy
```

Check deployment status: https://github.com/SongshGeo/SongshGeo-as-Scholar/actions

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```bash
# Required for abstract extraction
OPENAI_API_KEY=sk-your-openai-api-key
```

## 📝 License

This repository contains the source code for my personal academic website.

## 🙏 Acknowledgments

Built with:
- [Hugo](https://gohugo.io/)
- [Hugo Blox Builder](https://hugoblox.com/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
