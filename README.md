# SongshGeo Academic CV Site

Personal academic CV website built with [Hugo](https://gohugo.io/) and [Hugo Blox Builder](https://hugoblox.com/).

## 🚀 Quick Start

### Development

```bash
# Start development server
make server

# Or with Hugo directly
hugo server --logLevel error --disableFastRender
```

### Build

```bash
# Build the site
make build

# Or with Hugo directly
hugo --gc --minify --logLevel error
```

### Deploy to GitHub Pages

```bash
# Check current status
make status

# Commit and push (triggers automatic deployment)
make deploy

# Or step by step
make commit  # Commit changes
make push    # Push to GitHub (auto-deploys via GitHub Actions)
```

The site will be automatically deployed to GitHub Pages when you push to the `main` or `dev` branch. Check deployment status at: https://github.com/SongshGeo/SongshGeo-as-Scholar/actions

## 📚 Publication Management

### Check for missing publications

```bash
make check
```

This will compare your BibTeX file (`content/My-Publications.bib`) with existing publication pages and show:
- ✅ Exact matches
- 🔍 Title-based matches (different citation keys, same title)
- ⚠️ Truly missing publications

### Preview what would be created

```bash
make preview
```

### Create missing publication pages

```bash
# Create only truly missing publications (recommended)
make create

# Create all missing publications (including title matches)
make create-all
```

### Full workflow

```bash
# 1. Check what's missing
make check

# 2. Preview what will be created
make preview

# 3. Create the missing pages
make create

# 4. Review and edit the generated files
# 5. Test locally
make server
```

## 🛠️ Available Make Targets

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make check` | Check for missing publications |
| `make preview` | Preview what would be created |
| `make create` | Create truly missing publication pages |
| `make create-all` | Create all missing publications |
| `make server` | Start Hugo development server |
| `make build` | Build the site |
| `make clean` | Clean generated files |
| `make install-deps` | Install Python dependencies |
| `make status` | Show git status |
| `make commit` | Commit all changes with message |
| `make push` | Push to GitHub (triggers deployment) |
| `make deploy` | Quick deploy (commit + push) |

## 📁 Project Structure

```
.
├── content/              # Site content
│   ├── en/              # English content
│   ├── zh/              # Chinese content
│   └── My-Publications.bib  # Master BibTeX file
├── scripts/             # Publication management scripts
│   ├── check_missing_publications_enhanced.py
│   ├── create_publication_template.py
│   └── README.md       # Detailed script documentation
├── config/              # Hugo configuration
├── Makefile            # Build automation
└── README.md           # This file
```

## 📖 Documentation

- **Script Documentation**: See [`scripts/README.md`](scripts/README.md) for detailed documentation about the publication management scripts
- **Hugo Blox Builder**: [Official Documentation](https://docs.hugoblox.com/)
- **Hugo**: [Official Documentation](https://gohugo.io/documentation/)

## 🔧 Dependencies

- Hugo >= 0.148.2
- Go >= 1.21
- Python 3 (for publication management scripts)
- bibtexparser (install with `make install-deps`)

## 📝 License

This repository contains the source code for my personal academic website.
