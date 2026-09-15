# Full CV Compilation

This directory contains the LaTeX source for the full academic CV, published at
`static/uploads/SongshGeo_fullCV.pdf` and linked from the author pages
(`content/en/authors/admin/_index.md`, `content/zh/authors/admin/_index.md`).

It used to live on Overleaf with its own private copy of the bibliography. It now sits in
this repo and reads the **same master bib as the publication list**, so a `make sync-pubs`
from Zotero flows into the CV automatically — no more re-editing the reference list by hand.

## Files

Only `main.tex`, `resume.cls`, `author-filter.tex`, `journals.yaml`, `review-service.tex`
and this README are tracked in git. Everything else in this directory is a build artifact
and is gitignored.

- `main.tex` - The CV itself (**the source**). Education, employment, projects, talks,
  awards — hand-written here. The Publications and Academic Services sections are generated.
- `resume.cls` - Document class (a modified Trey Hunner / LaTeXTemplates resume class):
  section formatting, header/footer, the `rSection` environment.
- `author-filter.tex` - Biber sourcemap that tags first-author / corresponding-author papers
  so the Publications section can list only those. See below.
- `journals.yaml` - Field grouping and JCR quartile for every journal reviewed for
  (**the source** for those two facts). See below.
- `review-service.tex` - The Academic Services list, generated from `journals.yaml` plus the
  review archive. Generated but **tracked**, because the archive lives outside the repo.
- `My-Publications.bib` - Copy of the master bib at the repo root, made by `make update-cv`.
  **Never edit it here** — it is overwritten on every build. The master bib is maintained by
  `make sync-pubs` from Zotero.
- `main.pdf`, `main.aux`, `main.bbl`, `main.log`, … - LaTeX output and auxiliary files.

## Usage

```bash
make update-cv           # compile and copy to static/uploads/SongshGeo_fullCV.pdf
make update-cv-verbose   # same, but show the full pdfLaTeX/biber output when debugging
make update-pdfs         # rebuild both the CV and the publication list
```

`make sync-pubs` and `make full-update` both end by rebuilding the CV, so the usual Zotero
workflow needs no extra step.

Under the hood it is the same four-pass build as `publist/` (LaTeX → Biber → LaTeX → LaTeX),
driven by the shared `latex_build` macro in the `Makefile`.

## How the Publications section works

The CV lists **only published or accepted articles where Song is first or corresponding
author** — currently 11 of the 41 articles in the master bib — and points readers to
<https://cv.songshgeo.com/publication/> for the complete list. `publist/` remains the formal
complete list and still carries everything, including work under review.

```latex
\nocite{*}
\printbibliography[type=article, heading=none, keyword={cv-selected},
                   notkeyword={cv-unpublished}, notkeyword={duplicate-zh}]
```

Two build-time keywords do the filtering. Neither exists in the bib; both are attached by
sourcemaps so that the Zotero-generated bib is never edited.

| keyword | set by | meaning |
|---|---|---|
| `cv-selected` | `author-filter.tex` | Song is first author, or Song's position is the corresponding position |
| `cv-unpublished` | the status maps at the top of `main.tex` | `year` is `submitted`, `under review` or `in prep` |

`notkeyword={duplicate-zh}` alongside them is **inert today** — the keyword appears 0
times in the bib. It is kept for parity with `publist/main.tex`.

There used to be a `notkeyword={to-read}` beside it, added on the same "inert switch"
reasoning. It was removed in 2026-09: `to-read` is a tag actually in use in Zotero as a
personal reading marker, and the moment it landed on five of Song's own submitted papers
the switch started hiding them from both documents — silently, because these filters do
not report what they drop. **Do not add filters on keywords that Zotero may legitimately
attach to Song's own papers**; a build-time keyword (like `cv-selected`) is the safe kind,
because nothing outside this repo can set it.

`cv-unpublished` keys off the `year` field's status string. A legal year passes, and so does
`accepted` — it matches none of the three patterns, so accepted-but-not-yet-published papers
appear in the CV as intended.

`cv-selected` is not in the bib. It is attached at build time by the sourcemap in
**`author-filter.tex`**, which is `\input` into `main.tex`'s `\DeclareSourcemap`. The rule:

> Song, Shuang is the **first** author, **or** Song's position in the author list is exactly
> the position annotated as `corresponding`.

That second clause is the subtle one. Most `Author+an = {2=corresponding}` annotations in the
bib mark a **supervisor**, not Song — in `chen2022b` Song is 3rd, in `yang2017` Song is 6th,
and the corresponding author is the 2nd person in both. Matching on "does this entry have a
corresponding annotation" would wrongly pull in ~20 papers; the positions have to match.
`author-filter.tex` therefore carries one map per author position (covering positions 1–20)
and documents two traps worth knowing before editing it: literal spaces inside `\regexp{}`
are eaten by TeX (use `\s+`), and `fieldset` is skipped unless the map is `[overwrite]`
(nearly every entry already has a `keywords` field).

Other details:

- Only `@article` entries appear. The three `@inproceedings` (conference) entries in the
  master bib are deliberately left out of the CV; they do appear in `publist/`.
- `\GetTotalCount` counts the entries this document actually **prints** — so after filtering
  it equals the number listed (11), not the number published. The intro sentence is worded to
  match that meaning; do not reword it as a total without changing how the count is obtained.
- `maxnames=5` keeps author lists short. `publist/` uses `maxnames=50` because it is the
  formal complete list.
- Corresponding authors are marked with an asterisk (`Song, S.*`), with a
  `* = Corresponding author` legend under the list. This hooks `\mkbibnamegiven`, **not**
  `\mkbibnamefamily`: names print as "Song, S." (family first, given initial last), so the
  marker has to follow the given initial to land after the whole name. `publist/main.tex`
  hooks `mkbibnamefamily` and consequently renders `*Song, S.` — if you ever unify the two,
  that is the one to change.

### Known limits of the filter

All three fail **closed** — a paper gets left out, never wrongly claimed. That is the safe
direction for an authorship claim, but it does mean a missing paper is worth investigating
rather than shrugging at.

1. **Zotero must carry the annotation, and the export postscript must be installed.**
   `Author+an` does not exist in Zotero; it is produced at export time by
   `scripts/zotero-bbt-postscript.js` from the item's `corr:N` tag (see scripts/README.md).
   Two ways this fails, both silent:
   - the item has no `corr:N` tag → tag it in Zotero, re-run `make sync-pubs`;
   - the postscript is not installed in Better BibTeX → **every** annotation disappears at
     once, and the CV quietly shrinks. A Better BibTeX reinstall resets that pref, which is
     exactly what happened in 2026-09. Check with `grep -c 'Author+an' My-Publications.bib`
     (expect ~30, never 0) before trusting a freshly synced CV.

   Fix it in Zotero either way — never by editing the bib or hardcoding the key here.
2. **Author names must be `Family, Given`.** The position regex counts authors with
   `([^,]+,[^,]+\s+and\s+){n}`, which assumes exactly one comma per author. A braced
   institutional author (`{World Bank}`, no comma) or a suffixed name (`King, Jr., M.`, two
   commas) before Song shifts the count and the entry drops out. No such names are in the
   bib today, but it is regenerated from Zotero, so this can appear without warning.
3. **`maxnames=5` can hide the asterisk.** If Song is the corresponding author at position
   6 or later, the entry is still selected but Song is swallowed by "et al." and the `*`
   is not visible, even though the legend promises it. The highest corresponding position in
   the current set is 2. Raising `maxnames` for the CV is the fix if this ever comes up.

A quick way to check the filter against the bib is to recompute the expected set in Python
(parse `author` and `Author+an`, apply the rule above) and compare it with
`pdftotext static/uploads/SongshGeo_fullCV.pdf - | grep -cE '^\[[0-9]+\]'`.

## How the Academic Services section works

The list of journals reviewed for is generated by `scripts/build_review_service.py` from two
places that are deliberately kept apart:

| where | holds | maintained by |
|---|---|---|
| `$REVIEWER_DIR` (default `~/Documents/Community/Reviewer`) | which journals, how many reviews, which dates | filing each manuscript as `<Journal>/<YYYY-MM[-DD]>_<title>/` |
| `cv/journals.yaml` | each journal's field group and JCR quartile | by hand — see the caveat below |

The split is forced by the data: the archive is the only record of what was actually
reviewed, and a JCR quartile cannot be derived from anything on this machine — Clarivate is
a paywalled product with no public API, and the publishers do not publish quartiles on pages
a script can read (ScienceDirect, Wiley and SCImago all answer 403; Copernicus publishes
CiteScore and SJR but deliberately not JCR).

`make update-cv` regenerates `review-service.tex` first, so the usual workflow picks up new
reviews with no extra step. Two behaviours are worth knowing:

- **A newly reviewed journal fails the build** until it is added to `journals.yaml` with a
  field and a quartile. This is on purpose: finishing a review is the only moment anyone
  will remember to look the quartile up. The error prints a YAML stub to paste.
- **A missing `$REVIEWER_DIR` is not an error.** The script prints `skip` and exits 0, and
  the committed `review-service.tex` is used as-is, so the CV still builds on any clone.

Nothing guesses. A quartile that cannot be established stays `TODO` and blocks the build,
because a wrong quartile on a CV is worse than a missing section. Use `n/a` when no quartile
should be printed — the journal has none, or it could not be pinned down — and say which in
a `note:`.

**The quartiles in `journals.yaml` came from public secondary sources, not from Clarivate.**
The `checked:` date at the top of the file records when, and the build prints it on every
run. This matters because those sources are unreliable in a specific way: they routinely
print a SCImago **SJR** quartile under a "JCR" heading, and the two really do differ —
*Geomorphology* is SJR Q1 but JCR Q2, and *Frontiers in Water* is SJR Q1 but JCR Q2 (Water
Resources, 50/131). Where sources disagreed, the one naming an actual JCR category and rank
was taken, and the entries that could not be pinned down that way carry a `note:` saying so.
Confirm the set against institutional JCR access, and re-check after each June release.

A journal folder with no dated subfolder is reported and skipped, never silently patched up
in the registry: the archive is the source of truth, so the fix belongs there. Records that
are filed in the archive but are not peer reviews go in the `exclude_records:` list.

`name:` exists for exactly one reason — macOS forbids `:` in a directory name, so
*Journal of Hydrology: Regional Studies* and *AMBIO: A Journal of the Human Environment*
can never be spelled correctly as folders. Every other journal prints under its folder name,
so a folder named imprecisely is fixed by renaming the folder.

## One thing not to remove from `main.tex`

**The `\DeclareSourcemap` status block.** `year = {submitted}` / `{under review}` are not
valid dates, so biber falls back to a 9999 placeholder for all of them and the states get
interleaved by surname. The block tags them `cv-unpublished` (which is what excludes them)
and rewrites `presort` per state so each would form its own block if the filter were ever
relaxed. It runs at compile time rather than living in the bib because the bib is
regenerated from Zotero.

`publist/main.tex` additionally carries a `newunicodechar` dash mapping; this document does
**not**, and does not need one. That mapping exists because Times under *XeLaTeX* silently
drops bare Unicode en/em-dashes ("Human–Water" → "HumanWater"). Under pdfLaTeX the dashes
typeset correctly on their own — verified by building without the mapping. If the CV is ever
moved to XeLaTeX, add it back (see the engine section below).

## Engine: pdfLaTeX, not XeLaTeX

This document is built with **pdfLaTeX** (`CV_ENGINE` in the `Makefile`), unlike `publist/`,
which uses XeLaTeX. That is not an arbitrary choice — the CV was written for pdfTeX and two
of its packages depend on it:

- `times` sets the body font through NFSS. Under XeLaTeX, `fontspec` takes over the font
  selection and `times` is **silently ignored** — the whole CV falls back to Latin Modern,
  which looks quite different and is easy to miss.
- `fontawesome` (v4) ships a Type 1 font that pdfTeX picks up from the texmf tree directly.
  Under XeLaTeX it is loaded by font *name* via fontspec, which requires the OTF to be
  registered with the system font database; on macOS it is not, and the build fails outright.

If you ever want to move the CV to XeLaTeX, three things change together —
`\setmainfont{TeX Gyre Termes}` for the body font, `fontawesome5` for the icons, and the
`newunicodechar` dash mapping copied from `publist/main.tex` — and the result should be
diffed against the current PDF before committing.

## Not in this pipeline

`static/uploads/Song_CV_2pages.pdf` — the two-page short CV — is still maintained by hand
and has no source in this repo.
