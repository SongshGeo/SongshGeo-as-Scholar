# Examples: prompts and commands

## Routine sync (this repo)

**User prompt:**

> Pull my latest papers from Zotero and update the publication list.

**Agent actions:**

1. Confirm Zotero is running with Better BibTeX.
2. Run `make sync-pubs` from the repo root.
3. Read the preview, confirm `y`, let it create pages / tag / rebuild the PDF.
4. Remind the user to curate new pages (`featured:`, tags, PDF) and `make deploy`.

---

## Preview only, no changes

**User prompt:**

> What's in my Zotero search that isn't on the site yet? Don't change anything.

**Agent actions:**

```bash
poetry run python scripts/sync_pubs_from_zotero.py --dry-run
```

Report the NEW / stale-key / no-citekey / not-in-search sections back to the user.

---

## Only recent papers

**User prompt:**

> Only sync papers from 2020 onward.

**Agent actions:**

```bash
make sync-pubs SYNC_ARGS="--since 2020"
```

---

## A different saved search

**User prompt:**

> Sync from my "#01.Selected" saved search instead.

**Agent actions:**

```bash
make sync-pubs SYNC_ARGS="--search '#01.Selected'"
```

(The name is case-sensitive and includes the leading `#`. It is passed via
`SYNC_ARGS` because a bare `#…` in the Makefile would be read as a comment.)

---

## A paper is missing from the sync

**User prompt:**

> "Improving representation of collective memory…" is in my search but didn't sync.

**Agent actions:**

1. Run `--dry-run` and look at the **NO BETTER BIBTEX CITATION KEY** section.
2. If listed there, pin a citation key in Zotero (right-click ▸ Better BibTeX ▸
   pin citation key), then re-run `make sync-pubs`.

---

## Zotero was closed

**User prompt:**

> `make sync-pubs` says it can't reach Better BibTeX.

**Agent actions:**

1. Open the Zotero app (Better BibTeX loads with it).
2. Re-run `make sync-pubs`. The tool needs the live app for citation keys and
   BibTeX export, even though it reads membership from the local database.
