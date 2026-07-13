# Reference: Zotero saved search → publication list

## Data flow

```
Zotero saved search  ──(read-only zotero.sqlite)──▶  member item set
        │                                                  │
        │                                       keep journalArticle / conferencePaper
        ▼                                                  ▼
Better BibTeX JSON-RPC  ──item.citationkey──▶  citekeys  ──item.export──▶  biblatex
        │                                                                     │
        │                                          add-only merge (DOI + title dedup)
        ▼                                                                     ▼
                                     My-Publications.bib  ──▶  create pages ──▶ auto-tag ──▶ pubs.pdf
```

The **membership** is computed locally from `~/Zotero/zotero.sqlite` opened
`immutable=1` (read-only, bypasses Zotero's locks) — Zotero stores no
saved-search membership table and exposes no "run search" endpoint, so the tool
evaluates the search's conditions itself. **Citation keys and BibTeX** come from
Better BibTeX over HTTP, so **Zotero must be running**.

## How the saved search is evaluated

The tool reads `savedSearchConditions` for the named search and evaluates only
the operators the search actually uses. It **hard-errors on anything else** so an
edit in Zotero can never silently produce a wrong result.

| Condition | Operator | Meaning |
|-----------|----------|---------|
| `savedSearch` | `is` | Include the members of a nested saved search (resolved recursively). |
| `itemType` | `is` / `isNot` | Keep / drop an item type. |
| `tag` | `is` / `isNot` | Keep / drop items with a tag. |
| `creator` | `contains` | Match a creator name (substring over first/last-name combos). |
| `joinMode` | `all` / `any` | Combine the conditions with AND / OR. |

The default search `#00.English my-pubs` = **(nested "my works": creator is one
of the Song name variants) AND (itemType ≠ manuscript) AND (not tagged
`#🔤有英译🔤`)**. The name variants are read from the nested search — nothing is
hard-coded, so editing the variants in Zotero just works.

## `sync_pubs_from_zotero.py` flags

| Flag | Default | Role |
|------|---------|------|
| `--search NAME` | `#00.English my-pubs` | Saved-search name to sync from. |
| `--bib PATH` | `My-Publications.bib` | Master bib to update. |
| `--since YEAR` | (off) | Only add papers with year ≥ `YEAR` (undated entries kept). |
| `--dry-run` | (off) | Print the plan; write nothing. |
| `--update-existing` | (off) | Also overwrite existing entries in place with the Zotero version. Default never touches existing entries. |

## Report sections

- **NEW** — appended to the bib.
- **ALREADY IN BIB UNDER ANOTHER KEY** — same DOI or ≥80 % title match to an
  existing entry, so *not* re-added. `← stale key, consider renaming` flags cases
  where the existing key is an auto-minted placeholder (e.g. `zotero-item-…`).
- **NO BETTER BIBTEX CITATION KEY** — items with no citekey are skipped; pin one
  in Zotero to include them.
- **IN BIB BUT NOT IN SEARCH** — advisory only; these stay in the bib. Remove by
  hand if they no longer belong.

## Makefile mapping

Defined in [`Makefile`](../../../Makefile):

| Variable | Default | Role |
|----------|---------|------|
| `SYNC_SCRIPT` | `scripts/sync_pubs_from_zotero.py` | The sync tool. |
| `CREATE_SCRIPT` | `scripts/create_publication_template.py` | Makes new pages. |
| `AUTOTAG_SCRIPT` | `scripts/auto_tag_publications.py` | Regenerates role/year tags. |
| `BIB_FILE` | `My-Publications.bib` | Master bib. |
| `LANG` | `en` | Locale for created pages. |
| `SYNC_ARGS` | (empty) | Extra flags forwarded to the sync tool. |

Targets: **`make sync-pubs`** (preview → confirm → bib → pages → tags → PDF) and
**`make package-sync-pubs-skill`** (zip this skill + the scripts for sharing).

## Environment

| Var | Default | Role |
|-----|---------|------|
| `ZOTERO_DATA_DIR` | `~/Zotero` | Folder holding `zotero.sqlite`. |
| `ZOTERO_LOCAL_API` | `http://localhost:23119` | Zotero / Better BibTeX endpoint. |

Stdlib only — the sync tool needs no extra Python packages. The page/PDF steps
use the repo's existing Poetry environment and TeX toolchain.

## Relationship to other skills

- [compile-publist-from-bib](../compile-publist-from-bib/SKILL.md) — the PDF
  compile step (`make update-publist`) this skill calls last.
- `make full-update` — the pre-existing manual-export workflow; `sync-pubs`
  replaces its first step (hand-editing the bib) with a Zotero pull and adds the
  `auto_tag` step that `full-update` omits.
