# Makefile for SongshGeo CV Site
# ================================

# Configuration
BIB_FILE := content/My-Publications.bib
LANG := en
CONTENT_DIR := content

# Python interpreter
PYTHON := python3

# Script paths
SCRIPT_DIR := scripts
CHECK_SCRIPT := $(SCRIPT_DIR)/check_missing_publications_enhanced.py
CREATE_SCRIPT := $(SCRIPT_DIR)/create_publication_template.py

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

.PHONY: help check create create-all clean server build install-deps

# Default target
help:
	@echo "$(BLUE)SongshGeo CV Site - Publication Management$(NC)"
	@echo ""
	@echo "Available targets:"
	@echo "  $(GREEN)make check$(NC)         - Check for missing publications"
	@echo "  $(GREEN)make create$(NC)        - Create missing publication pages (only truly missing)"
	@echo "  $(GREEN)make create-all$(NC)    - Create all missing publications (including title matches)"
	@echo "  $(GREEN)make preview$(NC)       - Preview what would be created"
	@echo "  $(GREEN)make server$(NC)        - Start Hugo development server"
	@echo "  $(GREEN)make build$(NC)         - Build the site"
	@echo "  $(GREEN)make clean$(NC)         - Clean generated files"
	@echo "  $(GREEN)make install-deps$(NC)  - Install Python dependencies"
	@echo ""
	@echo "Configuration:"
	@echo "  BibTeX file: $(YELLOW)$(BIB_FILE)$(NC)"
	@echo "  Language:    $(YELLOW)$(LANG)$(NC)"
	@echo ""

# Check for missing publications
check:
	@echo "$(BLUE)📖 Checking for missing publications...$(NC)"
	@$(PYTHON) $(CHECK_SCRIPT) $(BIB_FILE) --lang $(LANG) --verbose

# Preview what would be created
preview:
	@echo "$(BLUE)👀 Previewing publications to be created...$(NC)"
	@$(PYTHON) $(CREATE_SCRIPT) $(BIB_FILE) --lang $(LANG) --dry-run

# Create missing publication pages (only truly missing)
create:
	@echo "$(BLUE)🔨 Creating missing publication pages...$(NC)"
	@$(PYTHON) $(CREATE_SCRIPT) $(BIB_FILE) --lang $(LANG)
	@echo "$(GREEN)✅ Done! Remember to review and edit the generated files.$(NC)"

# Create all missing publications (including title matches)
create-all:
	@echo "$(BLUE)🔨 Creating ALL missing publication pages...$(NC)"
	@echo "$(YELLOW)⚠️  Warning: This will also create publications with title matches!$(NC)"
	@$(PYTHON) $(CREATE_SCRIPT) $(BIB_FILE) --lang $(LANG) --all
	@echo "$(GREEN)✅ Done! Remember to review and edit the generated files.$(NC)"

# Install Python dependencies
install-deps:
	@echo "$(BLUE)📦 Installing Python dependencies...$(NC)"
	@$(PYTHON) -m pip install bibtexparser

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
	@echo "$(GREEN)✅ Cleaned!$(NC)"

# Workflow: full check and create
workflow: check preview
	@echo ""
	@echo "$(YELLOW)Review the output above. If everything looks good, run:$(NC)"
	@echo "  $(GREEN)make create$(NC)     - to create only truly missing publications"
	@echo "  $(GREEN)make create-all$(NC) - to create all missing publications"

