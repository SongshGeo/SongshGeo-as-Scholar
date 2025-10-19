# Changelog

All notable changes to the publication management scripts.

## [2.0.0] - 2025-01-18

### 🎉 Major Refactor

#### Added
- **Centralized Logging System** with loguru
  - Automatic log rotation (10MB)
  - 3-month retention policy
  - Compressed archives
  - Thread-safe logging
  
- **Automated Workflow** via Makefile
  - `make full-update`: Complete publication update workflow
  - `make check-pdf`: Check PDF coverage
  - `make preview-rename`: Safe file renaming preview
  - `make rename`: Rename cite.bib keys and PDFs
  - `make extract-abstracts`: Extract from PDFs using OpenAI
  - `make update-publist`: Compile and sync publication list
  - `make show-log`: View recent logs
  - `make clean-logs`: Clean old logs

- **File Renaming Feature**
  - Rename cite.bib citation keys to match folder names
  - Rename PDF files to citation_key.pdf
  - Dry-run mode for safe preview
  
- **PDF Extraction Enhancements**
  - `--override`: Completely override index.md with minimal template
  - Better error handling
  - Progress indicators

#### Changed
- **BibTeX File Location**: Moved from `content/` to project root
- **Logging**: Replaced print statements with structured logging
- **Configuration**: Added `.env` support for API keys
- **Documentation**: Complete rewrite of README and guides

#### Fixed
- API key environment variable handling
- PDF file name edge cases
- Error reporting in batch operations

## [1.0.0] - 2024-12-01

### Initial Release

#### Added
- `check_missing_publications.py`: Basic publication checking
- `check_missing_publications_enhanced.py`: Enhanced checking with title matching
- `create_publication_template.py`: Template generation
- `extract_abstract_from_pdf.py`: PDF abstract extraction with OpenAI
- Basic Makefile targets

---

## Migration Guide (1.x → 2.0)

### 1. Move BibTeX File

```bash
# Move from content/ to root
mv content/My-Publications.bib ./My-Publications.bib
```

### 2. Install New Dependencies

```bash
# Update poetry
poetry lock
poetry install --extras pdf-extraction
```

### 3. Update Scripts Calls

Old:
```bash
python scripts/check_missing_publications.py content/My-Publications.bib
```

New:
```bash
make check
# or
poetry run python scripts/check_missing_publications_enhanced.py My-Publications.bib
```

### 4. Setup Logging

Logs are now automatically managed in `logs/` directory (gitignored).

### 5. Use New Workflow

```bash
# Instead of manual steps, use:
make full-update
```

---

## Deprecation Notice

- `content/My-Publications.bib` location is deprecated, move to root
- Direct Python script calls are still supported but `make` commands are preferred
- Print-based output is replaced with logged output (use `--verbose` for console output)

