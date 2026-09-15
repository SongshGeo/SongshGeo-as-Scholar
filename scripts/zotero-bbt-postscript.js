/*
 * Better BibTeX export postscript — corresponding-author annotations.
 * ====================================================================
 *
 * WHERE THIS RUNS
 *   Not in this repo. Paste it into Zotero:
 *       Settings ▸ Better BibTeX ▸ Advanced ▸ Export ▸ Postscript
 *   It then runs on *every* BBT export — the "Export Items…" dialog, auto-export,
 *   and the JSON-RPC `item.export` call that `scripts/sync_pubs_from_zotero.py`
 *   makes. This file is the tracked copy; Zotero holds the live one (in the pref
 *   `extensions.zotero.translators.better-bibtex.postscript`). Edit here, then
 *   re-paste — see scripts/README.md.
 *
 * WHAT IT DOES
 *   Zotero has no field for "who is the corresponding author", so this library
 *   records it as a *tag* on the item: `corr:2` = the 2nd author is corresponding.
 *   biblatex expects it as a name annotation instead:
 *
 *       Author+an = {2=corresponding}
 *
 *   The postscript translates the one into the other and then drops the `corr:*`
 *   tags from `keywords`, so the marker lives in exactly one place in the bib.
 *   Several corresponding authors are allowed: `corr:1` + `corr:3` together
 *   export as `{1=corresponding;3=corresponding}` — biblatex separates list
 *   items with `;` (a `,` would separate two annotations of the *same* author).
 *
 * WHY IT MATTERS HERE
 *   `Author+an` is the only input to the corresponding-author logic downstream:
 *   `cv/author-filter.tex` uses it to decide which papers the CV lists at all,
 *   `publist/main.tex` and `cv/main.tex` use it to print the `*`, and
 *   `scripts/create_publication_template.py` turns it into the `author_notes`
 *   of a new publication page. All of those fail *closed* — no annotation means
 *   a paper is quietly left out, never wrongly claimed. So an export without
 *   this postscript does not error; it just silently under-reports authorship.
 *   (That is exactly what a Better BibTeX reinstall caused: the pref reset to
 *   empty and the annotations vanished from the next export.)
 *
 * SCOPE
 *   `Translator.BetterTeX` covers both Better BibTeX and Better BibLaTeX.
 *   `Author+an` is a biblatex construct and plain BibTeX ignores it, but it is
 *   emitted for both so a stray bibtex export is never the silently lossy one.
 *   This repo wants **Better BibLaTeX** (`BBT_TRANSLATOR` in
 *   sync_pubs_from_zotero.py): it keeps `date`/`journaltitle` and exports tags
 *   as Unicode, where plain BibTeX ASCII-folds the emoji tags to empty strings.
 */

if (Translator.BetterTeX) {
  // `corr:2`, `corr 2`, `corresponding:2`, full-width colon — all mean the same.
  const CORRESPONDING = /^corr(?:esponding)?\s*[:：\-]?\s*(\d+)$/i

  const positions = []
  const otherTags = []

  for (const raw of item.tags || []) {
    const tag = typeof raw === 'string' ? raw : raw.tag
    const match = CORRESPONDING.exec((tag || '').trim())
    if (!match) {
      otherTags.push(raw)
      continue
    }
    const position = parseInt(match[1], 10)
    if (position > 0 && !positions.includes(position)) positions.push(position)
  }

  if (positions.length) {
    positions.sort((a, b) => a - b)
    entry.add({
      name: 'Author+an',
      value: positions.map(position => `${position}=corresponding`).join(';'),
      enc: 'verbatim',
      replace: true,
    })

    // Drop the `corr:*` tags now that the annotation carries them. An empty
    // array is a no-op for entry.add(), so an item whose *only* tag was `corr:N`
    // has to lose the field outright.
    if (otherTags.length) {
      entry.add({ name: 'keywords', value: otherTags, enc: 'tags', replace: true })
    }
    else {
      entry.remove('keywords')
    }
  }
}
