# Makefile for SongshGeo CV Site
# ================================

# Configuration
BIB_FILE := My-Publications.bib
LANG := en
CONTENT_DIR := content
PUBLIST_DIR := publist
UPLOADS_DIR := static/uploads

# Python interpreter
PYTHON := poetry run python

# Script paths
SCRIPT_DIR := scripts
CHECK_SCRIPT := $(SCRIPT_DIR)/check_missing_publications_enhanced.py
CREATE_SCRIPT := $(SCRIPT_DIR)/create_publication_template.py
EXTRACT_SCRIPT := $(SCRIPT_DIR)/extract_abstract_from_pdf.py

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help check check-pdf preview-rename rename extract-abstracts update-publist \
		full-update install server build clean status commit push deploy \
		docs-serve docs-build

# Default target
help:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║         SongshGeo CV Site - Publication Management            ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)📚 Publication Management Workflow:$(NC)"
	@echo "  $(YELLOW)make check$(NC)              Check for duplicates/missing publications"
	@echo "  $(YELLOW)make check-pdf$(NC)          Check which publications lack PDFs"
	@echo "  $(YELLOW)make preview-rename$(NC)     Preview file renaming (cite.bib + PDFs)"
	@echo "  $(YELLOW)make rename$(NC)             Rename files to match citation keys"
	@echo "  $(YELLOW)make extract-abstracts$(NC)  Extract abstracts from PDFs"
	@echo "  $(YELLOW)make update-publist$(NC)     Compile publication list PDF"
	@echo "  $(YELLOW)make full-update$(NC)        Complete workflow (check → rename → extract → publist)"
	@echo ""
	@echo "$(GREEN)🛠️  Development:$(NC)"
	@echo "  $(YELLOW)make install$(NC)            Install dependencies"
	@echo "  $(YELLOW)make server$(NC)             Start Hugo development server"
	@echo "  $(YELLOW)make build$(NC)              Build the site"
	@echo "  $(YELLOW)make clean$(NC)              Clean generated files"
	@echo ""
	@echo "$(GREEN)🚀 Deployment:$(NC)"
	@echo "  $(YELLOW)make status$(NC)             Show git status"
	@echo "  $(YELLOW)make commit$(NC)             Commit all changes with message"
	@echo "  $(YELLOW)make push$(NC)               Push to GitHub (triggers deployment)"
	@echo "  $(YELLOW)make deploy$(NC)             Quick deploy (commit + push)"
	@echo ""
	@echo "$(GREEN)📝 Logs:$(NC)"
	@echo "  $(YELLOW)make show-log$(NC)           Show recent log entries"
	@echo "  $(YELLOW)make clean-logs$(NC)         Clean old log files"
	@echo ""
	@echo "$(GREEN)📖 Documentation:$(NC)"
	@echo "  $(YELLOW)make docs-serve$(NC)         Serve documentation locally (http://localhost:3000)"
	@echo "  $(YELLOW)make docs-build$(NC)         Build documentation for deployment"
	@echo ""

# Install dependencies
install:
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	@poetry install --extras pdf-extraction
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

# Check for missing publications
check:
	@echo "$(BLUE)📖 Checking publications status...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG)

# Check for missing PDFs
check-pdf:
	@echo "$(BLUE)📄 Checking PDF coverage...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --check-pdf

# Preview file renaming
preview-rename:
	@echo "$(BLUE)👀 Previewing file renaming...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --renaming --dry-run

# Rename files to match citation keys
rename:
	@echo "$(BLUE)📝 Renaming files to match citation keys...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --renaming
	@echo "$(GREEN)✅ Files renamed$(NC)"

# Extract abstracts from PDFs
extract-abstracts:
	@echo "$(BLUE)🤖 Extracting abstracts from PDFs...$(NC)"
	@echo "$(YELLOW)⚠️  This will use OpenAI API (costs apply)$(NC)"
	@$(PYTHON) $(EXTRACT_SCRIPT) --max-publications 10
	@echo "$(GREEN)✅ Abstracts extracted$(NC)"

# Compile publication list and move to uploads
update-publist:
	@echo "$(BLUE)📄 Compiling publication list...$(NC)"
	@if [ ! -d "$(PUBLIST_DIR)" ]; then \
		echo "$(RED)❌ Error: $(PUBLIST_DIR) directory not found$(NC)"; \
		exit 1; \
	fi
	@cd $(PUBLIST_DIR) && xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1
	@cd $(PUBLIST_DIR) && biber main > /dev/null 2>&1
	@cd $(PUBLIST_DIR) && xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1
	@cd $(PUBLIST_DIR) && xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1
	@if [ -f "$(PUBLIST_DIR)/main.pdf" ]; then \
		cp $(PUBLIST_DIR)/main.pdf $(UPLOADS_DIR)/pubs.pdf; \
		echo "$(GREEN)✅ Publication list updated: $(UPLOADS_DIR)/pubs.pdf$(NC)"; \
	else \
		echo "$(RED)❌ Error: Failed to compile publication list$(NC)"; \
		exit 1; \
	fi

# Full update workflow
full-update:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║                  Full Publication Update                      ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1/6: Checking publication status...$(NC)"
	@$(MAKE) check
	@echo ""
	@echo "$(YELLOW)Step 2/6: Checking for missing PDFs...$(NC)"
	@$(MAKE) check-pdf
	@echo ""
	@read -p "$(YELLOW)Continue with renaming? [y/N] $(NC)" confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "$(RED)Aborted by user$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 3/6: Previewing file renaming...$(NC)"
	@$(MAKE) preview-rename
	@echo ""
	@read -p "$(YELLOW)Proceed with renaming? [y/N] $(NC)" confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "$(RED)Aborted by user$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 4/6: Renaming files...$(NC)"
	@$(MAKE) rename
	@echo ""
	@read -p "$(YELLOW)Extract abstracts from PDFs? [y/N] $(NC)" confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(YELLOW)Step 5/6: Extracting abstracts...$(NC)"; \
		$(MAKE) extract-abstracts; \
	else \
		echo "$(YELLOW)Step 5/6: Skipped abstract extraction$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 6/6: Updating publication list...$(NC)"
	@$(MAKE) update-publist
	@echo ""
	@echo "$(GREEN)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║              ✅ Full Update Completed!                        ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Review changes: $(YELLOW)git diff$(NC)"
	@echo "  2. Test locally:   $(YELLOW)make server$(NC)"
	@echo "  3. Commit:         $(YELLOW)make commit$(NC)"
	@echo "  4. Deploy:         $(YELLOW)make push$(NC)"

# Start Hugo development server
server:
	@echo "$(BLUE)🚀 Starting Hugo development server...$(NC)"
	@hugo server --logLevel error --disableFastRender

# Build the site
build:
	@echo "$(BLUE)🏗️  Building the site...$(NC)"
	@hugo --gc --minify --logLevel error
	@echo "$(GREEN)✅ Build complete!$(NC)"

# Clean generated files
clean:
	@echo "$(BLUE)🧹 Cleaning generated files...$(NC)"
	@rm -rf public resources .hugo_build.lock
	@rm -f $(PUBLIST_DIR)/*.aux $(PUBLIST_DIR)/*.log $(PUBLIST_DIR)/*.out $(PUBLIST_DIR)/*.pdf
	@echo "$(GREEN)✅ Cleaned!$(NC)"

# Show recent logs
show-log:
	@echo "$(BLUE)📋 Recent log entries (last 50 lines):$(NC)"
	@if [ -f "logs/publications.log" ]; then \
		tail -50 logs/publications.log; \
	else \
		echo "$(YELLOW)No log file found$(NC)"; \
	fi

# Clean old log files
clean-logs:
	@echo "$(BLUE)🧹 Cleaning old log files...$(NC)"
	@find logs -name "*.log.*" -type f -mtime +90 -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Old logs cleaned$(NC)"

# Git operations
status:
	@echo "$(BLUE)📊 Git Status:$(NC)"
	@git status

commit:
	@echo "$(BLUE)💾 Committing changes...$(NC)"
	@git add -A
	@git status --short
	@read -p "Enter commit message: " msg; \
	git commit -m "$$msg"
	@echo "$(GREEN)✅ Committed!$(NC)"

push:
	@echo "$(BLUE)🚀 Pushing to GitHub...$(NC)"
	@git push github $$(git branch --show-current)
	@echo "$(GREEN)✅ Pushed! GitHub Actions will deploy automatically.$(NC)"
	@echo "$(YELLOW)Check deployment status at: https://github.com/SongshGeo/SongshGeo-as-Scholar/actions$(NC)"

deploy: commit push
	@echo "$(GREEN)✅ Deployment triggered!$(NC)"

# Preview and create workflow
workflow: check
	@echo ""
	@echo "$(YELLOW)Review the output above. If everything looks good, run:$(NC)"
	@echo "  $(GREEN)make create$(NC)        - to create only truly missing publications"
	@echo "  $(GREEN)make full-update$(NC)   - for complete update workflow"

# Documentation commands
docs-serve:
	@echo "$(BLUE)📖 Starting documentation server...$(NC)"
	@echo "$(GREEN)Opening http://localhost:3000$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@echo ""
	@command -v docsify >/dev/null 2>&1 || { \
		echo "$(YELLOW)Installing docsify-cli globally...$(NC)"; \
		npm install -g docsify-cli; \
	}
	@cd docs && docsify serve .

docs-build:
	@echo "$(BLUE)📖 Building documentation...$(NC)"
	@mkdir -p _site
	@cp -r docs/* _site/
	@mkdir -p _site/scripts
	@cp scripts/README.md _site/scripts/
	@echo "$(GREEN)✅ Documentation built in _site/$(NC)"
	@echo "$(YELLOW)Preview: open _site/index.html$(NC)"
