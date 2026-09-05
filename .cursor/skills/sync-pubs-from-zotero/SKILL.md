---
name: sync-pubs-from-zotero
description: >-
  Syncs the publication list directly from a Zotero saved search (default
  "#00.English my-pubs") instead of a manual .bib export. Talks to the running
  Zotero via Better BibTeX: resolves the saved search read-only from
  zotero.sqlite, keeps journal/conference articles, and merges them add-only into
  My-Publications.bib, then drives the existing create-pages / auto-tag /
  update-publist steps. Use when updating publications from Zotero, pulling new
  papers into the site, running make sync-pubs, or auto-maintaining the pub list.
---

# Sync publications from a Zotero saved search

## Scope

This skill covers **one task**: keep `My-Publications.bib` (and therefore the
site's publication pages) in step with a **Zotero saved search**, by talking to
the local Zotero app directly — no manual "export to `.bib`".

It is the front-end that feeds the existing pipeline. The last mile (create
pages, tags, PDF) reuses the same scripts as before and the
[compile-publist-from-bib](../compile-publist-from-bib/SKILL.md) skill for the PDF.

**Policy (fixed):** *add-only.* New papers are appended to the bib; existing
entries are never modified (unless you pass `--update-existing`) and are never
deleted. Papers that dropped out of the search are only **reported** for you to
review by hand. Only **journal + conference** articles become pages — other
Zotero item types (presentations, theses, reports, books) are ignored. English
locale only (`content/en/publication/`).

## Preconditions

1. **Zotero is running** with the **Better BibTeX** plugin installed. It is
   required to resolve citation keys and export BibTeX (`http://localhost:23119`).
2. A **saved search** exists in Zotero (default name `#00.English my-pubs`).
3. `My-Publications.bib` exists at the repo root (the master bib).
4. For the page/PDF steps: the normal toolchain (`poetry`, `xelatex`, `biber`)
   as used by `make full-update` / `make update-publist`.

## Primary workflow (this repository)

From the repository root:

```bash
make sync-pubs
```

This runs, in order:

1. **Preview** — `sync_pubs_from_zotero.py --dry-run`: prints what would be
   added, what is already present under another key, what has no citation key,
   and what is in the bib but no longer in the search. Writes nothing.
2. **Confirm** — `[y/N]` prompt. Anything but `y`/`Y` stops with no changes.
3. **Update bib** — appends new entries to `My-Publications.bib`.
4. **Create pages** — `create_publication_template.py` makes
   `content/en/publication/<key>/{index.md,cite.bib}` for newly-added,
   publication-dated entries (drafts/submitted are skipped).
5. **Tag** — `auto_tag_publications.py` regenerates `my-role` + `role-*`/`year-*`
   tags so the home Publications widget filters pick up new pages.
6. **PDF** — `make update-publist` rebuilds `static/uploads/pubs.pdf`.

Then curate the new pages (set `featured:`, topical `tags`, drop in a PDF),
`make server` to preview, and `make deploy`.

## Just the bib (no pages)

To only refresh the bib and inspect it yourself:

```bash
poetry run python scripts/sync_pubs_from_zotero.py --dry-run   # preview
poetry run python scripts/sync_pubs_from_zotero.py             # write bib only
```

## Options

Forward flags through `SYNC_ARGS` (the search name defaults **inside the
script**, because it starts with `#`, which Make would treat as a comment):

```bash
make sync-pubs SYNC_ARGS="--since 2020"                       # only recent papers
make sync-pubs SYNC_ARGS="--search '#00.English my-pubs'"     # a different search
make sync-pubs SYNC_ARGS="--update-existing"                  # also refresh existing entries
```

See [reference.md](reference.md) for every flag and how the saved search is
evaluated; [examples.md](examples.md) for worked prompts.

## Failure recovery

1. **"Can't reach Better BibTeX"** — open Zotero; confirm the Better BibTeX
   plugin is installed and enabled.
2. **"Saved search … not found"** — check the name in Zotero (it is
   case-sensitive and includes the leading `#`).
3. **"Unsupported saved-search condition"** — you added a condition operator the
   evaluator doesn't implement yet; extend `sync_pubs_from_zotero.py` (the tool
   errors rather than guess).
4. **A paper you expect is skipped as "no citation key"** — pin a Better BibTeX
   citation key on that item in Zotero (right-click ▸ Better BibTeX ▸ pin), then
   re-run.
5. **A paper shows "≈ stale key, consider renaming"** — the bib already has that
   paper under an auto-minted key (e.g. `zotero-item-…`); rename the bib entry
   (and its content folder) to the proper citation key by hand.
