# Reference: Bib → publication list PDF

## Generic model

Three conceptual inputs:

1. **`bib_file`** — BibTeX database path.
2. **`publist_dir`** — Local directory with LaTeX sources; must contain an entry file (here: `main.tex`).
3. **`output_pdf`** — Final PDF path (for Hugo: under `static/uploads/` so the site serves `/uploads/...`).

Execution pattern:

1. Copy `bib_file` into `publist_dir` under the **basename** that `main.tex` references in `\addbibresource{...}`.
2. Run the biblatex chain in `publist_dir`: `xelatex` → `biber` → `xelatex` → `xelatex`.
3. Copy the built PDF (e.g. `main.pdf`) to `output_pdf`.

## This repository: Makefile mapping

Defined in [`Makefile`](../../../Makefile) at the repo root:

| Variable | Default | Role |
|----------|---------|------|
| `BIB_FILE` | `My-Publications.bib` | Root-level BibTeX file; must exist for `update-publist`. |
| `PUBLIST_DIR` | `publist` | LaTeX template directory. |
| `UPLOADS_DIR` | `static/uploads` | Parent folder for site static assets. |
| `PUBLIST_OUTPUT_PDF` | `$(UPLOADS_DIR)/pubs.pdf` | Final publication list PDF path (override for custom output). |

Targets:

- **`make update-publist`** — Copies `$(BIB_FILE)` to `$(PUBLIST_DIR)/$(BIB_FILE)`, runs XeLaTeX + biber + XeLaTeX ×2 (output suppressed), then copies `main.pdf` to `$(PUBLIST_OUTPUT_PDF)`.
- **`make update-publist-verbose`** — Same compile sequence **without** hiding LaTeX/biber output (for debugging).

Override example:

```bash
make BIB_FILE=exports/library.bib PUBLIST_DIR=~/templates/my-publist PUBLIST_OUTPUT_PDF=./dist/pubs.pdf update-publist
```

Ensure `PUBLIST_DIR` contains `main.tex` and that `\addbibresource{...}` matches the **copied** filename inside that directory (the Makefile copies using `BIB_FILE`’s basename).

## Relationship to `output_pdf`

- In this repo, `output_pdf` corresponds to **`PUBLIST_OUTPUT_PDF`** (default `static/uploads/pubs.pdf`).
- Site links (e.g. author pages) use `/uploads/pubs.pdf` — keep the filename consistent if you change `PUBLIST_OUTPUT_PDF`.

## Local template without Overleaf

You only need:

- A folder on disk (`publist_dir`) with `main.tex` and any `\input`/style files.
- A `.bib` file whose name matches `\addbibresource{...}` after copy.
- A TeX distribution providing `xelatex` and `biber`.

Overleaf is **not** required; it is one possible source for the same files exported to your machine.

## Common issues

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `publist directory not found` | `PUBLIST_DIR` missing | Add or clone template into `publist/` (or set `PUBLIST_DIR`). |
| `BIB_FILE not found` | Wrong path or name | Place `.bib` at repo root or set `BIB_FILE`. |
| `Failed to compile` with no details | Default target hides logs | Run `make update-publist-verbose` or manual `xelatex` in `publist_dir`. |
| Empty or wrong bibliography | `biber` not run or wrong `.bib` name | Match `\addbibresource` to copied file; rerun full chain. |
| `make clean` removed artifacts | `clean` deletes `publist/*.pdf` etc. | Re-run `update-publist`; `static/uploads/pubs.pdf` is not removed by `clean` in the default Makefile. |

## Python / Poetry

`update-publist` does **not** use Poetry or Python. Installing Python deps is unrelated to compiling the publication list PDF.

## Sharing the skill (zip bundle)

From the repository root:

```bash
make package-publist-skill
```

Creates `dist/publist-skill-<timestamp>.zip` containing the Cursor skill (`.cursor/skills/compile-publist-from-bib/`), `Makefile`, `README.md`, and publist-related docs under `docs/`. If a local `publist/` directory exists, its **source** files are appended (e.g. `main.tex`, `My-Publications.bib`, `README.md`); nested `publist/.git`, LaTeX aux, and build PDFs are **excluded** to keep the bundle small and safe to share. The `dist/` directory is listed in `.gitignore`.

## Makefile abstraction (implemented)

The repository `Makefile` supports explicit overrides without editing files:

- **`PUBLIST_OUTPUT_PDF`** — final PDF path (maps to `output_pdf` in this skill).
- **`BIB_FILE`** — any path to a `.bib` file; it is copied into `PUBLIST_DIR` as **`$(notdir $(BIB_FILE))`**, so `main.tex` must use `\addbibresource{that_basename.bib}`.
- **`update-publist-verbose`** — same compile steps as `update-publist` but prints XeLaTeX/biber output for debugging.
