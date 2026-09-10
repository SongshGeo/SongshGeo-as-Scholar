#!/usr/bin/env python3
"""Integrity checks for the parts of this site we wrote ourselves.

Deliberately scoped: this does *not* test Hugo, Hugo Blox, or the theme. It
tests the seams where our own code meets the theme, and the invariant this repo
cares about most — every string a visitor reads comes from one source of truth
(markdown front matter, config/, data/, or i18n/), never from a literal buried
in JS, SCSS, or a template.

Source-only checks run anywhere. Pass --public <dir> after a build to also check
the rendered output.

    python scripts/check_site_integrity.py
    python scripts/check_site_integrity.py --public public

Exit code is 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bibtex_entries import iter_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "zh")

# Our own front-end sources. The theme's own files are none of our business.
OUR_JS = sorted((ROOT / "assets" / "js").glob("*.js"))
OUR_LAYOUTS = sorted((ROOT / "layouts").rglob("*.html"))
OUR_SCSS = sorted((ROOT / "assets" / "scss").glob("*.scss"))

CJK = re.compile(r"[一-鿿]")


class Report:
    """Collects failures so one run reports every problem, not just the first."""

    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, name: str, problems: list[str]) -> None:
        self.checks += 1
        if problems:
            self.failures.append(name)
            print(f"FAIL  {name}")
            for p in problems:
                print(f"        {p}")
        else:
            print(f"ok    {name}")

    def exit_code(self) -> int:
        print()
        if self.failures:
            print(f"{len(self.failures)} of {self.checks} checks failed: {', '.join(self.failures)}")
            return 1
        print(f"all {self.checks} checks passed")
        return 0


# ── source checks ──────────────────────────────────────────────────────────── #


def check_publications_trace_to_bib() -> list[str]:
    """Every publication page must be regenerable from My-Publications.bib.

    A page whose folder name is not a citekey in the bib is invisible to
    sync_pubs_from_zotero.py, so it can never be corrected or refreshed.
    """
    bib = (ROOT / "My-Publications.bib").read_text(encoding="utf-8")
    keys = {e.key for e in iter_entries(bib)}
    problems = []
    for lang in LANGS:
        pub_dir = ROOT / "content" / lang / "publication"
        if not pub_dir.is_dir():
            continue
        for page in sorted(p for p in pub_dir.iterdir() if p.is_dir()):
            if page.name not in keys:
                problems.append(f"content/{lang}/publication/{page.name}/ has no entry in My-Publications.bib")
    return problems


def check_i18n_files_agree() -> list[str]:
    """en.yaml and zh.yaml must define exactly the same keys."""
    problems = []
    tables = {}
    for lang in LANGS:
        path = ROOT / "i18n" / f"{lang}.yaml"
        if not path.is_file():
            return [f"i18n/{lang}.yaml is missing"]
        tables[lang] = {
            m.group(1)
            for m in re.finditer(r"^([a-z0-9_]+):", path.read_text(encoding="utf-8"), re.M)
        }
    only_en = tables["en"] - tables["zh"]
    only_zh = tables["zh"] - tables["en"]
    for k in sorted(only_en):
        problems.append(f"'{k}' is in i18n/en.yaml but not i18n/zh.yaml")
    for k in sorted(only_zh):
        problems.append(f"'{k}' is in i18n/zh.yaml but not i18n/en.yaml")
    return problems


def _i18n_keys(lang: str) -> set[str] | None:
    """Keys defined in i18n/<lang>.yaml; None when the file is absent."""
    path = ROOT / "i18n" / f"{lang}.yaml"
    if not path.is_file():
        return None
    return {m.group(1) for m in re.finditer(r"^([a-z0-9_]+):", path.read_text(encoding="utf-8"), re.M)}


def _brand_role_ids() -> list[str]:
    """Role ids in data/brand_roles.yaml; empty when the file is absent."""
    path = ROOT / "data" / "brand_roles.yaml"
    if not path.is_file():
        return []
    return [m.group(1) for m in re.finditer(r"^- id:\s*(\S+)", path.read_text(encoding="utf-8"), re.M)]


def check_i18n_keys_resolve() -> list[str]:
    """Every key our templates ask for must exist in the i18n tables."""
    defined = _i18n_keys("en")
    if defined is None:
        return ["i18n/en.yaml is missing, so no template key can resolve"]
    role_ids = _brand_role_ids()
    problems = []
    for tpl in OUR_LAYOUTS:
        text = tpl.read_text(encoding="utf-8")
        for m in re.finditer(r'i18n\s+"([a-z0-9_]+)"', text):
            if m.group(1) not in defined:
                problems.append(f"{tpl.relative_to(ROOT)} asks for i18n key '{m.group(1)}', which is undefined")
        # Keys built with printf, e.g. (printf "brand_role_%s" .id) over data/brand_roles.yaml.
        for m in re.finditer(r'printf\s+"([a-z0-9_]+)%s([a-z0-9_]*)"', text):
            prefix, suffix = m.group(1), m.group(2)
            if not role_ids:
                problems.append(f"{tpl.relative_to(ROOT)} builds '{prefix}<id>{suffix}' keys, but data/brand_roles.yaml has no ids")
            for role_id in role_ids:
                key = f"{prefix}{role_id}{suffix}"
                if key not in defined:
                    problems.append(f"{tpl.relative_to(ROOT)} builds i18n key '{key}', which is undefined")
    return problems


# A literal that reaches the reader: assigned to a text sink, or set as one of
# the attributes a screen reader speaks.
DOM_TEXT_SINK = re.compile(
    r"\.(?:textContent|innerText|innerHTML|title|placeholder)\s*=|"
    r"setAttribute\(\s*['\"](?:aria-label|title|placeholder|alt)['\"]"
)
JS_STRING = re.compile(r"'([^'\\]*)'|\"([^\"\\]*)\"")
HTML_TAG = re.compile(r"<[^>]*>")
GO_ACTION = re.compile(r"\{\{.*?\}\}", re.DOTALL)
GO_COMMENT = re.compile(r"\{\{/\*.*?\*/\}\}", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
TWO_WORDS = re.compile(r"[A-Za-z]{2,}\s+[A-Za-z]{2,}")
THREE_WORDS = re.compile(r"[A-Za-z]{2,}(?:[\s,]+[A-Za-z]{2,}){2,}")


def _is_prose(literal: str, min_words: re.Pattern[str]) -> bool:
    """True when what's left after stripping markup still reads like a sentence."""
    bare = HTML_TAG.sub("", literal).strip()
    return bool(CJK.search(bare) or min_words.search(bare))


def check_no_hardcoded_display_text() -> list[str]:
    """No visible copy may be authored inside JS, SCSS, or a template.

    Catching only CJK would miss the likeliest relapse — an English literal
    slipped back into JS. So JS is judged by where a literal *goes*: anything
    assigned to a DOM text sink, or set as a spoken attribute, must come from
    window.__siteUI. Markup fragments ('<span class="x">') strip to nothing and
    are left alone; '<span>Read more</span>' does not.
    """
    problems = []

    for js in OUR_JS:
        for i, line in enumerate(js.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("//", 1)[0]
            if CJK.search(code):
                problems.append(f"{js.relative_to(ROOT)}:{i} has a CJK string literal; move it to i18n/")
                continue
            if "IS_ZH" in code:
                problems.append(f"{js.relative_to(ROOT)}:{i} branches on language in JS; use i18n/ via window.__siteUI")
            if not DOM_TEXT_SINK.search(code):
                continue
            for m in JS_STRING.finditer(code):
                literal = m.group(1) if m.group(1) is not None else m.group(2)
                if _is_prose(literal, TWO_WORDS):
                    problems.append(
                        f"{js.relative_to(ROOT)}:{i} writes the literal {literal!r} to the page; "
                        "move it to i18n/ and read it from window.__siteUI"
                    )

    for scss in OUR_SCSS:
        for i, line in enumerate(scss.read_text(encoding="utf-8").splitlines(), 1):
            m = re.search(r'content:\s*"([^"]{2,})"', line)
            if m and re.search(r"[A-Za-z]{3}", m.group(1)):
                problems.append(f"{scss.relative_to(ROOT)}:{i} renders words via CSS content: {m.group(1)!r}")

    # Templates: strip Go actions and comments, then HTML, and see what prose is
    # left standing. Anything still there was typed into the template.
    for tpl in OUR_LAYOUTS:
        text = tpl.read_text(encoding="utf-8")
        text = GO_COMMENT.sub("", text)
        text = HTML_COMMENT.sub("", text)
        text = GO_ACTION.sub("", text)
        for i, line in enumerate(text.splitlines(), 1):
            bare = HTML_TAG.sub(" ", line).strip()
            if CJK.search(bare) or THREE_WORDS.search(bare):
                problems.append(
                    f"{tpl.relative_to(ROOT)}: hardcoded prose {bare[:60]!r}; use (i18n \"<key>\") instead"
                )
    return problems


def check_no_unresolved_wikilinks() -> list[str]:
    """No Obsidian `[[wikilink]]` may survive into content.

    The repo is edited in Obsidian (see .obsidian/). Hugo has no idea what
    `[[Some Note]]` means, so it renders the brackets literally on the page —
    silently, with no build warning. Two of these shipped before this check.
    """
    wikilink = re.compile(r"\[\[([^\]\n]+)\]\]")
    problems = []
    for lang in LANGS:
        for md in sorted((ROOT / "content" / lang).rglob("*.md")):
            for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                for m in wikilink.finditer(line):
                    problems.append(
                        f"{md.relative_to(ROOT)}:{i} has the unresolved wikilink [[{m.group(1)}]]; "
                        'use [text]({{< relref "/section/page" >}})'
                    )
    return problems


def check_bib_parsers_agree() -> list[str]:
    """No script may re-derive the BibTeX entry regex; they drifted once already."""
    problems = []
    for py in sorted((ROOT / "scripts").glob("*.py")):
        if py.name in ("bibtex_entries.py", Path(__file__).name):
            continue  # the parser itself, and this checker, which quotes the pattern
        for i, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
            # The tell is the entry *terminator* — a '@' in the first column of
            # the next line. Regexes that merely mention '@\w+' (renaming a
            # citekey, say) are a different job and are left alone.
            if r"(?=\n@" in line:
                problems.append(
                    f"{py.relative_to(ROOT)}:{i} re-derives the BibTeX entry boundary; import bibtex_entries instead"
                )
    return problems


# ── rendered-output checks ─────────────────────────────────────────────────── #


def check_ui_payload_is_an_object(public: Path) -> list[str]:
    """window.__siteUI must render as a JS object literal, in every language.

    Hugo's contextual escaping will happily emit `jsonify` output as a quoted
    *string* unless it is piped through safeJS — and then every consumer of
    window.__siteUI silently no-ops. This is the check that catches that.
    """
    problems = []
    for lang in LANGS:
        index = public / "index.html" if lang == "en" else public / lang / "index.html"
        if not index.is_file():
            problems.append(f"{index.relative_to(public)} not found; did the build run?")
            continue
        # Tolerate both builds: `hugo` emits JSON, `hugo --minify` rewrites it
        # as a JS object literal with bare keys. Both must start with '{'.
        m = re.search(r"window\.__siteUI\s*=\s*(.+?)(?:;\s*)?</script>", index.read_text(encoding="utf-8"))
        if not m:
            problems.append(f"[{lang}] window.__siteUI is not emitted at all")
            continue
        payload = m.group(1).strip()
        if not payload.startswith("{"):
            problems.append(
                f"[{lang}] window.__siteUI is {payload[:1]!r}-quoted, not an object "
                "— pipe jsonify through safeJS in layouts/partials/custom_js.html"
            )
            continue
        for section in ("about", "brand", "pubfilter"):
            if not re.search(rf'"?{section}"?\s*:\s*\{{', payload):
                problems.append(f"[{lang}] window.__siteUI.{section} is missing or empty")
        brand = re.search(r'"?text"?\s*:\s*"([^"]*)"', payload)
        if not brand or not brand.group(1).strip():
            problems.append(f"[{lang}] brand text is empty; it should come from the author page")
    return problems


def check_no_dead_internal_links(public: Path) -> list[str]:
    """Every internal link in the built site must resolve.

    This one check deliberately walks the whole rendered site rather than only
    our own pages: the theme's list, tag and author pages are generated *from*
    our content, so a dead link there still traces back to something we wrote.
    """
    comment = re.compile(r"<!--.*?-->", re.DOTALL)
    problems = []
    for page in sorted(public.rglob("*.html")):
        html = comment.sub("", page.read_text(encoding="utf-8", errors="ignore"))
        for href in re.findall(r'href="(/[^"#?]*)"', html):
            target = public / href.lstrip("/")
            if target.exists() or (target / "index.html").exists():
                continue
            problems.append(f"{page.relative_to(public)} links to {href}, which does not exist")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--public", type=Path, help="built site directory, to also check rendered output")
    args = parser.parse_args()

    report = Report()
    report.check("publications trace back to My-Publications.bib", check_publications_trace_to_bib())
    report.check("i18n/en.yaml and i18n/zh.yaml define the same keys", check_i18n_files_agree())
    report.check("every i18n key a template asks for is defined", check_i18n_keys_resolve())
    report.check("no display text hardcoded in JS, SCSS or templates", check_no_hardcoded_display_text())
    report.check("no unresolved [[wikilinks]] in content", check_no_unresolved_wikilinks())
    report.check("only one BibTeX entry parser in scripts/", check_bib_parsers_agree())

    if args.public:
        public = args.public if args.public.is_absolute() else ROOT / args.public
        if not public.is_dir():
            print(f"FAIL  --public {public} is not a directory")
            return 1
        report.check("window.__siteUI renders as a JS object", check_ui_payload_is_an_object(public))
        report.check("no dead internal links in the built site", check_no_dead_internal_links(public))

    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main())
