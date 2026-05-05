# Examples: prompts and commands

## Project defaults (this repo)

**User prompt:**

> Regenerate the publication list PDF from my master BibTeX file using the project defaults.

**Agent actions:**

1. Confirm `My-Publications.bib`, `publist/main.tex`, and toolchain (`xelatex`, `biber`).
2. Run `make update-publist` from repo root.
3. Verify `static/uploads/pubs.pdf`.

---

## Local paths only (no Overleaf)

**User prompt:**

> I do not use Overleaf. I have `~/cv/publist-template/` with `main.tex` and I want to build from `~/papers/all.bib` into `~/cv/out/pubs.pdf`.

**Agent actions:**

1. Ensure `\addbibresource{...}` in `main.tex` matches the basename used when copying the bib (e.g. copy `all.bib` to `all.bib` if the template says `\addbibresource{all.bib}`).
2. Run compilation in `~/cv/publist-template/` with the standard chain, or use:

   ```bash
   make BIB_FILE=~/papers/all.bib PUBLIST_DIR=~/cv/publist-template PUBLIST_OUTPUT_PDF=~/cv/out/pubs.pdf update-publist
   ```

   (Adjust paths; ensure `~/cv/out/` exists.)

---

## Debugging a failed build

**User prompt:**

> `make update-publist` failed but I see almost no error text.

**Agent actions:**

1. Run `make update-publist-verbose`.
2. If still unclear, `cd` to `publist_dir` and run `xelatex -interaction=nonstopmode main.tex` then `biber main`, inspect `main.log`.

---

## Custom bib filename at repo root

**User prompt:**

> My Bib file is `Exports.bib` in the project root; rebuild the site publication PDF.

**Agent actions:**

```bash
make BIB_FILE=Exports.bib update-publist
```

Ensure `publist/main.tex` uses `\addbibresource{Exports.bib}` **or** adjust the template — the Makefile copies the file as `$(BIB_FILE)` basename into `PUBLIST_DIR`.
