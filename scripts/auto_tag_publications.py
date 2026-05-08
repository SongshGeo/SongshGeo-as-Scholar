#!/usr/bin/env python3
"""
Sync publication frontmatter so the home Publications widget can filter by:

- `my-role`  list of {`leading`, `featured`, `co-authored`} written into
              the YAML head matter as the source of truth for role.
- `tags`     receive `role-leading` / `role-featured` / `role-co-authored`
              (mirrors of `my-role`, used by Isotope CSS classes) plus
              `year-<YYYY>` (used by the timeline picker in JS).

Source-of-truth rules
---------------------
- `leading`     admin is `authors[0]` OR `author_notes[admin_index]` matches
                /correspond/i
- `featured`    `featured: true` is set in the frontmatter
- `co-authored` admin is in `authors` and `leading` is NOT applicable

Existing user tags are preserved; only the script-managed tag families
(`role-*`, `year-*`, plus deprecated `first-author`/`co-author`/
`corresponding-author`/`recent`) are rewritten on each run.

Usage
-----
    python scripts/auto_tag_publications.py
    python scripts/auto_tag_publications.py --dry-run
"""

import argparse
import re
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent
PUB_DIRS = [ROOT / "content" / lang / "publication" for lang in ("en", "zh")]

ADMIN_KEY = "admin"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)", re.DOTALL)

# Tag families this script owns. Anything matching these patterns is rewritten
# from the computed values; user-authored topical tags are preserved.
MANAGED_TAG_PREFIXES = ("role-", "year-")
DEPRECATED_LITERAL_TAGS = {
    "first-author", "co-author", "corresponding-author", "recent",
}


def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    return (m.group(1), m.group(2)) if m else None


def extract_authors(fm: str) -> List[str]:
    block_re = re.compile(r"^authors:\s*\n((?:\s*-\s*.+\n)+)", re.MULTILINE)
    m = block_re.search(fm)
    if not m:
        return []
    return [
        re.sub(r"^[\"']|[\"']$", "", line.strip().lstrip("-").strip())
        for line in m.group(1).splitlines()
        if line.strip().startswith("-")
    ]


def extract_author_notes(fm: str) -> List[str]:
    block_re = re.compile(r"^author_notes:\s*\n((?:\s*-\s*.*\n)+)", re.MULTILINE)
    m = block_re.search(fm)
    if not m:
        return []
    notes = []
    for line in m.group(1).splitlines():
        s = line.strip().lstrip("-").strip()
        if s in ("[]", ""):
            notes.append("")
        else:
            notes.append(re.sub(r"^[\"']|[\"']$", "", s))
    return notes


def extract_date_year(fm: str) -> Optional[int]:
    m = re.search(r"^date:\s*['\"]?(\d{4})", fm, re.MULTILINE)
    return int(m.group(1)) if m else None


def extract_featured_flag(fm: str) -> bool:
    m = re.search(r"^featured:\s*(true|false)\b", fm, re.MULTILINE | re.IGNORECASE)
    return bool(m) and m.group(1).lower() == "true"


def compute_my_role(fm: str) -> List[str]:
    """Return the my-role list for this publication (preserves declared order)."""
    roles: List[str] = []
    authors = extract_authors(fm)
    notes = extract_author_notes(fm)

    if not authors:
        return roles

    try:
        admin_idx = authors.index(ADMIN_KEY)
    except ValueError:
        admin_idx = -1

    is_first = admin_idx == 0
    is_corresponding = (
        admin_idx >= 0
        and admin_idx < len(notes)
        and re.search(r"correspond", notes[admin_idx], re.IGNORECASE) is not None
    )

    if is_first or is_corresponding:
        roles.append("leading")

    if extract_featured_flag(fm):
        roles.append("featured")

    if admin_idx >= 0 and "leading" not in roles:
        roles.append("co-authored")

    return roles


def upsert_my_role_block(fm: str, roles: List[str]) -> str:
    """Replace or insert the `my-role:` block in the frontmatter."""
    block_re = re.compile(
        r"(^my-role:\s*(?:\n(?:\s*-\s*.+\n)*|\s*\[[^\]]*\]\s*\n))",
        re.MULTILINE,
    )
    body = "my-role:\n" + "".join(f"  - {r}\n" for r in roles) if roles else ""

    if block_re.search(fm):
        return block_re.sub(body, fm) if body else block_re.sub("", fm)

    if not body:
        return fm

    # Insert before the existing `tags:` block if present, else append
    tags_match = re.search(r"^tags:\s*\n", fm, re.MULTILINE)
    if tags_match:
        i = tags_match.start()
        return fm[:i] + body + fm[i:]
    return fm.rstrip() + "\n" + body


def merge_tags_block(fm: str, computed_tags: List[str]) -> str:
    """Merge computed `role-*`/`year-*` tags into the existing tags list,
    dropping any deprecated or stale managed tags first."""
    block_re = re.compile(r"(^tags:\s*\n)((?:\s*-\s*.+\n)*)", re.MULTILINE)
    m = block_re.search(fm)

    def is_managed(t: str) -> bool:
        return t.startswith(MANAGED_TAG_PREFIXES) or t in DEPRECATED_LITERAL_TAGS

    if m:
        header = m.group(1)
        body = m.group(2)
        existing = []
        for line in body.splitlines():
            s = line.strip().lstrip("-").strip()
            existing.append(re.sub(r"^[\"']|[\"']$", "", s))

        kept = [t for t in existing if t and not is_managed(t)]
        merged = kept + [t for t in computed_tags if t not in kept]
        rebuilt = header + "".join(f"  - {t}\n" for t in merged)
        return fm[: m.start()] + rebuilt + fm[m.end():]

    insertion = "tags:\n" + "".join(f"  - {t}\n" for t in computed_tags)
    return fm.rstrip() + "\n" + insertion


def process_file(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    parts = split_frontmatter(text)
    if not parts:
        return False
    fm, body = parts

    roles = compute_my_role(fm)
    year = extract_date_year(fm)

    computed_tags: List[str] = []
    for r in roles:
        computed_tags.append(f"role-{r}")
    if year is not None:
        computed_tags.append(f"year-{year}")

    if not roles and not computed_tags:
        return False

    new_fm = upsert_my_role_block(fm, roles)
    new_fm = merge_tags_block(new_fm, computed_tags)
    if new_fm == fm:
        return False

    if not dry_run:
        path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed = scanned = 0
    for pub_dir in PUB_DIRS:
        if not pub_dir.exists():
            continue
        for index_md in sorted(pub_dir.glob("*/index.md")):
            scanned += 1
            if process_file(index_md, args.dry_run):
                changed += 1
                rel = index_md.relative_to(ROOT)
                print(f"  {'would update' if args.dry_run else 'updated'}: {rel}")

    verb = "Would change" if args.dry_run else "Changed"
    print(f"\n{verb} {changed} of {scanned} publication files.")


if __name__ == "__main__":
    main()
