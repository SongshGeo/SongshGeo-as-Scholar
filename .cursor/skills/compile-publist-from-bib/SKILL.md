---
name: compile-publist-from-bib
description: >-
  Compiles a publication list PDF from a BibTeX file using a local LaTeX template
  directory (XeLaTeX + biber). Supports project defaults or custom bib_file,
  publist_dir, and output paths. Use when updating My-Publications.bib, rebuilding
  pubs.pdf, static/uploads/pubs.pdf, publication list PDF, biblatex publist,
  local LaTeX template without Overleaf, or when make update-publist fails silently.
---

# Compile publication list from BibTeX

## Scope

This skill covers **one task**: turn a `.bib` file into a **publication list PDF** using a **local** LaTeX project (template directory). It does **not** run publication checks, renaming, or OpenAI abstract extraction unless the user asks separately.

Overleaf is **optional** (sync template to disk if you use it); a purely local `publist/` directory is enough.

## Parameters

| Parameter | Meaning | Defaults in this repo |
|-----------|---------|------------------------|
| `bib_file` | Path to the master BibTeX file | `My-Publications.bib` at repository root |
| `publist_dir` | Directory containing `main.tex` and LaTeX resources | `publist/` |
| `output_pdf` | Where to place the final PDF for the site or user | `static/uploads/pubs.pdf` |

If the user does not specify paths, use the table defaults relative to the project root.

## Preconditions (check before compiling)

1. **`publist_dir` exists** and contains **`main.tex`** (or the entry file your template uses; this skill assumes `main.tex` as in this project).
2. **`bib_file` exists** and is readable.
3. **`\addbibresource{...}`** in `main.tex` matches the **filename** you copy into `publist_dir` (this repo expects the copied file to match `BIB_FILE`, e.g. `My-Publications.bib`).
4. **Toolchain**: `xelatex` and `biber` on `PATH` (biblatex workflow).
5. **Output directory** for `output_pdf` exists or can be created (e.g. `static/uploads/`).

## Primary workflow (this repository)

1. From the **repository root**, prefer:

   ```bash
   make update-publist
   ```

2. If compilation fails with little output (stdout is suppressed in the default target), run:

   ```bash
   make update-publist-verbose
   ```

   Then read the terminal and `publist/main.log` for errors.

3. Confirm **`output_pdf`** was updated (e.g. `static/uploads/pubs.pdf`).

## Generic workflow (any local template)

When `make` is unavailable or paths are custom:

1. Copy `bib_file` into `publist_dir` using the **name** expected by `main.tex` (e.g. `cp /path/to/papers.bib "$PUBLIST_DIR/My-Publications.bib"` if `\addbibresource{My-Publications.bib}`).
2. In `publist_dir`, run:

   ```bash
   xelatex -interaction=nonstopmode main.tex
   biber main
   xelatex -interaction=nonstopmode main.tex
   xelatex -interaction=nonstopmode main.tex
   ```

3. Copy the generated PDF (usually `main.pdf`) to `output_pdf`:

   ```bash
   cp main.pdf /path/to/output.pdf
   ```

## Makefile overrides (this repo)

You can override variables on the command line without editing files:

```bash
make BIB_FILE=Other.bib PUBLIST_DIR=/path/to/template PUBLIST_OUTPUT_PDF=/path/to/out.pdf update-publist
```

If `BIB_FILE` includes directories (e.g. `exports/papers.bib`), the Makefile copies it into `publist_dir` as **`papers.bib`** (basename). Ensure `main.tex` uses `\addbibresource{papers.bib}`.

See [reference.md](reference.md) for variable names and mapping to `output_pdf`.

## Failure recovery

1. **Silent failure**: Use `make update-publist-verbose` or run `xelatex`/`biber` manually in `publist_dir` without redirecting output.
2. **Missing `publist_dir`**: Obtain or create a local LaTeX publist template; align `\addbibresource` with the copied `.bib` filename.
3. **Stale `pubs.pdf`**: If `main.pdf` is missing, the Makefile reports failure; if unsure, compare timestamps or `git diff` on `output_pdf`.
4. **Wrong Bib name**: Ensure the copied file in `publist_dir` matches what `main.tex` references.

## Additional resources

- Details and repo-specific mapping: [reference.md](reference.md)
- Example prompts: [examples.md](examples.md)
