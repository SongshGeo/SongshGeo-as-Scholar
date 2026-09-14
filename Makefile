# Makefile for SongshGeo CV Site
# ================================

# Configuration
BIB_FILE := My-Publications.bib
LANG := en
CONTENT_DIR := content
PUBLIST_DIR := publist
CV_DIR := cv
UPLOADS_DIR := static/uploads
# Final publication list PDF path (override: make PUBLIST_OUTPUT_PDF=/path/to/out.pdf update-publist)
PUBLIST_OUTPUT_PDF := $(UPLOADS_DIR)/pubs.pdf
# Final full-CV PDF path. The filename is linked from content/*/authors/admin/_index.md,
# so changing it means updating those links too.
CV_OUTPUT_PDF := $(UPLOADS_DIR)/SongshGeo_fullCV.pdf
# Peer-review archive that feeds the CV's Academic Services section. It lives
# outside the repo, so cv/review-service.tex is committed and any clone without
# this directory still builds the CV. Override with an env var or on the command
# line: make update-cv REVIEWER_DIR=/path/to/archive
REVIEWER_DIR ?= $(HOME)/Documents/Community/Reviewer

# TeX engine per document — see the latex_build comment; do not swap these.
PUBLIST_ENGINE := xelatex
CV_ENGINE := pdflatex
# Output redirection for the LaTeX passes. The *-verbose targets clear it per-target
# so the full engine/biber output reaches the terminal.
LATEX_QUIET := > /dev/null 2>&1
# Zip bundle for sharing the compile-publist-from-bib skill (see package-publist-skill)
PUBLIST_SKILL_ZIP_DIR := dist

# Optional: cap how many incomplete publications to process per extract run (empty = all)
EXTRACT_MAX_PUBLICATIONS :=

# Optional: e.g. CHECK_PROMPT_FLAGS=--all so create prompt includes drafts (submitted, under review)
CHECK_PROMPT_FLAGS :=

# Optional extra flags forwarded to sync_pubs_from_zotero.py (see `make sync-pubs`).
# The saved-search name defaults inside the script (it starts with '#', which Make
# would treat as a comment). Override the search or scope here, e.g.:
#   make sync-pubs SYNC_ARGS="--since 2020"
#   make sync-pubs SYNC_ARGS="--search '#00.English my-pubs' --update-existing"
SYNC_ARGS :=

# Python interpreter
PYTHON := poetry run python

# Script paths
SCRIPT_DIR := scripts
CHECK_SCRIPT := $(SCRIPT_DIR)/check_missing_publications_enhanced.py
CREATE_SCRIPT := $(SCRIPT_DIR)/create_publication_template.py
EXTRACT_SCRIPT := $(SCRIPT_DIR)/extract_abstract_from_pdf.py
SYNC_SCRIPT := $(SCRIPT_DIR)/sync_pubs_from_zotero.py
AUTOTAG_SCRIPT := $(SCRIPT_DIR)/auto_tag_publications.py
INTEGRITY_SCRIPT := $(SCRIPT_DIR)/check_site_integrity.py
PDF_SYNC_SCRIPT := $(SCRIPT_DIR)/check_generated_pdfs.py
REVIEW_SCRIPT := $(SCRIPT_DIR)/build_review_service.py

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help check check-pdf check-pdf-interactive preview-rename rename extract-abstracts update-publist \
		update-publist-verbose update-cv update-cv-verbose update-reviews update-pdfs verify-pdfs install-hooks \
		package-publist-skill sync-pubs package-sync-pubs-skill full-update install server build test test-full clean status commit push deploy \
		docs-serve docs-build

# Default target
help:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║         SongshGeo CV Site - Publication Management            ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)📚 Publication Management Workflow:$(NC)"
	@echo "  $(YELLOW)make sync-pubs$(NC)          Pull Zotero saved search → bib → pages → tags → PDFs"
	@echo "  $(YELLOW)make check$(NC)              Check for duplicates/missing publications"
	@echo "  $(YELLOW)make check-pdf$(NC)          Check which publications lack PDFs"
	@echo "  $(YELLOW)make check-pdf-interactive$(NC) Same + optional prompt to create missing pages"
	@echo "  $(YELLOW)make preview-rename$(NC)     Preview file renaming (cite.bib + PDFs)"
	@echo "  $(YELLOW)make rename$(NC)             Rename files to match citation keys"
	@echo "  $(YELLOW)make extract-abstracts$(NC)  Extract abstracts from PDFs"
	@echo "  $(YELLOW)make update-publist$(NC)     Compile publication list PDF"
	@echo "  $(YELLOW)make update-publist-verbose$(NC) Same, show XeLaTeX/biber output (debug)"
	@echo "  $(YELLOW)make update-cv$(NC)          Compile full CV PDF (same master bib)"
	@echo "  $(YELLOW)make update-cv-verbose$(NC)  Same, show pdfLaTeX/biber output (debug)"
	@echo "  $(YELLOW)make update-reviews$(NC)     Rebuild the CV peer-review list from REVIEWER_DIR"
	@echo "  $(YELLOW)make update-pdfs$(NC)        Rebuild both PDFs (publist + CV)"
	@echo "  $(YELLOW)make package-publist-skill$(NC) Zip skill + Makefile + docs for sharing"
	@echo "  $(YELLOW)make package-sync-pubs-skill$(NC) Zip the Zotero-sync skill for sharing"
	@echo "  $(YELLOW)make full-update$(NC)        Complete workflow (check → rename → extract → PDFs)"
	@echo ""
	@echo "$(GREEN)🛠️  Development:$(NC)"
	@echo "  $(YELLOW)make install$(NC)            Install dependencies"
	@echo "  $(YELLOW)make server$(NC)             Start Hugo development server"
	@echo "  $(YELLOW)make build$(NC)              Build the site"
	@echo "  $(YELLOW)make test$(NC)               Integrity checks on our own code"
	@echo "  $(YELLOW)make test-full$(NC)          Build, then also check rendered output"
	@echo "  $(YELLOW)make install-hooks$(NC)      Install the pre-commit hooks (once per clone)"
	@echo "  $(YELLOW)make verify-pdfs$(NC)        Rebuild both PDFs and diff against the committed ones"
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
	@$(MAKE) install-hooks
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

# Check for missing publications
check:
	@echo "$(BLUE)📖 Checking publications status...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG)

# Check for missing PDFs
check-pdf:
	@echo "$(BLUE)📄 Checking PDF coverage...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --check-pdf

# Same as check-pdf; in TTY may prompt to create missing publication folders (full-update)
check-pdf-interactive:
	@echo "$(BLUE)📄 Checking PDF coverage...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --check-pdf --prompt-create-missing $(CHECK_PROMPT_FLAGS)

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
	@$(PYTHON) $(EXTRACT_SCRIPT) $(if $(EXTRACT_MAX_PUBLICATIONS),--max-publications $(EXTRACT_MAX_PUBLICATIONS),)
	@echo "$(GREEN)✅ Abstracts extracted$(NC)"

# Shared LaTeX build used by every document in this repo (publist/, cv/).
# Each document lives in its own directory, is named main.tex, and pulls its
# bibliography from the one master $(BIB_FILE) at the repo root — the copy that
# lands in the document directory is a build artifact, not a source file.
#
# The engine is per-document and is NOT interchangeable:
#   publist/ needs xelatex  — its template is written for it.
#   cv/      needs pdflatex — it relies on \usepackage{times} and fontawesome v4,
#                             both of which are Type 1 / NFSS machinery. Under
#                             xelatex, fontspec takes over, `times` is silently
#                             ignored (the body font falls back to Latin Modern)
#                             and fontawesome v4 fails to find its OTF on macOS.
#   $(1) = source directory
#   $(2) = output PDF path
#   $(3) = human-readable label for the log lines
#   $(4) = TeX engine
# Verbosity comes from $(LATEX_QUIET), which the *-verbose targets clear per-target —
# passing shell redirection through $(call) would make any comma in an argument fatal.
define latex_build
	@if [ ! -d "$(1)" ]; then \
		echo "$(RED)❌ Error: $(1) directory not found$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(BIB_FILE)" ]; then \
		echo "$(RED)❌ Error: $(BIB_FILE) not found (set BIB_FILE to your .bib path)$(NC)"; \
		exit 1; \
	fi
	@mkdir -p "$(dir $(2))"
	@cp -f "$(BIB_FILE)" "$(1)/$(notdir $(BIB_FILE))"
	@cd $(1) && $(4) -interaction=nonstopmode main.tex $(LATEX_QUIET)
	@cd $(1) && biber main $(LATEX_QUIET)
	@cd $(1) && $(4) -interaction=nonstopmode main.tex $(LATEX_QUIET)
	@cd $(1) && $(4) -interaction=nonstopmode main.tex $(LATEX_QUIET)
	@if [ -f "$(1)/main.pdf" ]; then \
		cp $(1)/main.pdf $(2); \
		echo "$(GREEN)✅ $(3) updated: $(2)$(NC)"; \
	else \
		echo "$(RED)❌ Error: Failed to compile $(3)$(NC)"; \
		exit 1; \
	fi
endef

# Compile publication list and move to uploads
update-publist:
	@echo "$(BLUE)📄 Compiling publication list...$(NC)"
	$(call latex_build,$(PUBLIST_DIR),$(PUBLIST_OUTPUT_PDF),Publication list,$(PUBLIST_ENGINE))

# Same as update-publist but prints XeLaTeX/biber output (for debugging)
update-publist-verbose: LATEX_QUIET :=
update-publist-verbose:
	@echo "$(BLUE)📄 Compiling publication list (verbose)...$(NC)"
	$(call latex_build,$(PUBLIST_DIR),$(PUBLIST_OUTPUT_PDF),Publication list,$(PUBLIST_ENGINE))

# Regenerate cv/review-service.tex from the peer-review archive. Fails when a
# newly reviewed journal is missing its field/quartile in cv/journals.yaml;
# skips quietly (exit 0) when REVIEWER_DIR does not exist on this machine.
update-reviews:
	@echo "$(BLUE)📋 Refreshing the peer-review list...$(NC)"
	@$(PYTHON) $(REVIEW_SCRIPT) --reviewer-dir "$(REVIEWER_DIR)"

# Compile the full academic CV and move to uploads
update-cv: update-reviews
	@echo "$(BLUE)📄 Compiling full CV...$(NC)"
	$(call latex_build,$(CV_DIR),$(CV_OUTPUT_PDF),Full CV,$(CV_ENGINE))

# Same as update-cv but prints pdfLaTeX/biber output (for debugging)
update-cv-verbose: LATEX_QUIET :=
update-cv-verbose: update-reviews
	@echo "$(BLUE)📄 Compiling full CV (verbose)...$(NC)"
	$(call latex_build,$(CV_DIR),$(CV_OUTPUT_PDF),Full CV,$(CV_ENGINE))

# Rebuild every PDF that is generated from the master bib
update-pdfs: update-publist update-cv

# Zip the compile-publist-from-bib skill, Makefile, README, publist-related docs, and the
# publist/ LaTeX template for sharing.
package-publist-skill:
	@echo "$(BLUE)📦 Packaging publist skill bundle...$(NC)"
	@command -v zip >/dev/null 2>&1 || { echo "$(RED)❌ zip not found (install zip).$(NC)"; exit 1; }
	@mkdir -p "$(PUBLIST_SKILL_ZIP_DIR)"
	@if [ ! -d .cursor/skills/compile-publist-from-bib ]; then \
		echo "$(RED)❌ Error: .cursor/skills/compile-publist-from-bib not found$(NC)"; \
		exit 1; \
	fi
	@STAMP=$$(date +%Y%m%d-%H%M%S); \
	ZIP="$(PUBLIST_SKILL_ZIP_DIR)/publist-skill-$$STAMP.zip"; \
	rm -f "$$ZIP"; \
	zip -r "$$ZIP" \
		.cursor/skills/compile-publist-from-bib \
		Makefile \
		README.md \
		docs/README.md \
		docs/WORKFLOW.md \
		docs/QUICKSTART.md \
		docs/SETUP_COMPLETE.md \
		docs/SCRIPTS_CHANGELOG.md; \
	if [ $$? -ne 0 ]; then exit 1; fi; \
	zip "$$ZIP" $(PUBLIST_DIR)/main.tex $(PUBLIST_DIR)/README.md; \
	if [ $$? -ne 0 ]; then exit 1; fi; \
	echo "$(GREEN)✅ Bundle: $$ZIP$(NC)"

# Sync the master bib from a Zotero saved search, then run the full page pipeline.
# Needs Zotero running with the Better BibTeX plugin (see sync-pubs-from-zotero skill).
sync-pubs:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║              Sync Publications from Zotero                    ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1/5: Previewing changes from the Zotero saved search...$(NC)"
	@$(PYTHON) $(SYNC_SCRIPT) --bib $(BIB_FILE) $(SYNC_ARGS) --dry-run
	@echo ""
	@printf "%s" "$(YELLOW)Apply these bib changes and rebuild the site pages? [y/N] $(NC)"
	@read -r confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "$(RED)Stopped — nothing written.$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 2/5: Updating $(BIB_FILE)...$(NC)"
	@$(PYTHON) $(SYNC_SCRIPT) --bib $(BIB_FILE) $(SYNC_ARGS)
	@echo ""
	@echo "$(YELLOW)Step 3/5: Creating pages for new publications ($(LANG))...$(NC)"
	@$(PYTHON) $(CREATE_SCRIPT) $(BIB_FILE) --lang $(LANG)
	@echo ""
	@echo "$(YELLOW)Step 4/5: Syncing role / year tags...$(NC)"
	@$(PYTHON) $(AUTOTAG_SCRIPT)
	@echo ""
	@echo "$(YELLOW)Step 5/5: Rebuilding the publication list and CV PDFs...$(NC)"
	@$(MAKE) update-pdfs
	@echo ""
	@echo "$(GREEN)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║              ✅ Zotero Sync Completed!                        ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Review changes: $(YELLOW)git diff $(BIB_FILE) && git status content/$(LANG)/publication/$(NC)"
	@echo "  2. Curate new pages (featured, tags, PDFs), then: $(YELLOW)make server$(NC)"
	@echo "  3. Commit + deploy: $(YELLOW)make deploy$(NC)"

# Zip the sync-pubs-from-zotero skill + the sync script for sharing.
package-sync-pubs-skill:
	@echo "$(BLUE)📦 Packaging Zotero-sync skill bundle...$(NC)"
	@command -v zip >/dev/null 2>&1 || { echo "$(RED)❌ zip not found (install zip).$(NC)"; exit 1; }
	@mkdir -p "$(PUBLIST_SKILL_ZIP_DIR)"
	@if [ ! -d .cursor/skills/sync-pubs-from-zotero ]; then \
		echo "$(RED)❌ Error: .cursor/skills/sync-pubs-from-zotero not found$(NC)"; \
		exit 1; \
	fi
	@STAMP=$$(date +%Y%m%d-%H%M%S); \
	ZIP="$(PUBLIST_SKILL_ZIP_DIR)/sync-pubs-skill-$$STAMP.zip"; \
	rm -f "$$ZIP"; \
	zip -r "$$ZIP" \
		.cursor/skills/sync-pubs-from-zotero \
		$(SYNC_SCRIPT) \
		$(CREATE_SCRIPT) \
		$(CHECK_SCRIPT) \
		$(AUTOTAG_SCRIPT) \
		Makefile; \
	if [ $$? -ne 0 ]; then exit 1; fi; \
	echo "$(GREEN)✅ Bundle: $$ZIP$(NC)"

# Full update workflow
full-update:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║                  Full Publication Update                      ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1/6: Checking publication status...$(NC)"
	@$(MAKE) check
	@echo ""
	@echo "$(YELLOW)Step 2/6: BibTeX vs site folders + PDF files in each folder...$(NC)"
	@$(MAKE) check-pdf-interactive
	@echo ""
	@printf "%s\n" "$(YELLOW)── Steps 3–4: align cite.bib and PDF names with folder keys (optional) ──$(NC)"
	@printf "%s" "$(YELLOW)Continue to preview renames? [y/N] $(NC)"
	@read -r confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "$(RED)Stopped here (no renames).$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 3/6: Previewing file renaming...$(NC)"
	@$(MAKE) preview-rename
	@echo ""
	@printf "%s" "$(YELLOW)Apply those renames? [y/N] $(NC)"
	@read -r confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "$(RED)Stopped here (no renames applied).$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 4/6: Renaming files...$(NC)"
	@$(MAKE) rename
	@echo ""
	@printf "%s" "$(YELLOW)Run OpenAI abstract extraction (incremental skips filled pages)? [y/N] $(NC)"
	@read -r confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(YELLOW)Step 5/6: Extracting abstracts...$(NC)"; \
		$(MAKE) extract-abstracts; \
	else \
		echo "$(YELLOW)Step 5/6: Skipped abstract extraction$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 6/6: Updating publication list and CV...$(NC)"
	@$(MAKE) update-pdfs
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

# Install the pre-commit hooks. Needed once per clone; `make install` runs it too.
install-hooks:
	@echo "$(BLUE)🪝 Installing pre-commit hooks...$(NC)"
	@command -v pre-commit >/dev/null 2>&1 || { \
		echo "$(RED)❌ pre-commit not found — install it with: pipx install pre-commit$(NC)"; \
		exit 1; \
	}
	@pre-commit install
	@echo "$(GREEN)✅ Hooks installed$(NC)"
	@echo "$(YELLOW)   One-time sweep of the whole repo: pre-commit run --all-files$(NC)"

# The thorough version of the PDF sync check: recompile both documents and diff
# them against what is committed. Slower than the pre-commit hook, which only
# checks that the PDFs were staged alongside their sources.
verify-pdfs:
	@echo "$(BLUE)🔍 Verifying the generated PDFs match their sources...$(NC)"
	@$(PYTHON) $(PDF_SYNC_SCRIPT) --rebuild

# Start Hugo development server
server:
	@echo "$(BLUE)🚀 Starting Hugo development server...$(NC)"
	@hugo server --logLevel error --disableFastRender

# Build the site
build:
	@echo "$(BLUE)🏗️  Building the site...$(NC)"
	@hugo --gc --minify --logLevel error
	@echo "$(GREEN)✅ Build complete!$(NC)"

# Integrity checks for the code we wrote ourselves (not the theme).
# Source-only by default; `make test-full` builds first and also checks output.
test:
	@echo "$(BLUE)🔍 Checking site integrity (our code only)...$(NC)"
	@$(PYTHON) $(INTEGRITY_SCRIPT)

test-full: build
	@echo "$(BLUE)🔍 Checking site integrity, including rendered output...$(NC)"
	@$(PYTHON) $(INTEGRITY_SCRIPT) --public public

# Clean generated files
clean:
	@echo "$(BLUE)🧹 Cleaning generated files...$(NC)"
	@rm -rf public resources .hugo_build.lock
	@for d in $(PUBLIST_DIR) $(CV_DIR); do \
		rm -f $$d/*.aux $$d/*.bbl $$d/*.bcf $$d/*.blg $$d/*.bpx \
			$$d/*.log $$d/*.out $$d/*.run.xml $$d/*.pdf $$d/$(notdir $(BIB_FILE)); \
	done
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
