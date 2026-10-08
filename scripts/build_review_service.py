#!/usr/bin/env python3
"""Turn the local peer-review archive into the CV's Academic Services list.

Every manuscript Dr. Song reviews is filed under ``$REVIEWER_DIR`` as
``<Journal>/<YYYY-MM[-DD]>_<short title>/``. That directory is the source of
truth for *which* journals were reviewed for and *when* — but it says nothing
about a journal's field or its JCR quartile, and JCR is a paywalled Clarivate
product that cannot be scraped. So the two halves live apart:

  * the archive directory  → which journals, how many reviews, which dates
  * ``cv/journals.yaml``   → field grouping and quartile, verified by hand

This script joins them and writes ``cv/review-service.tex``, which
``cv/main.tex`` pulls in with ``\\input{review-service}``.

The registry is deliberately a gate, not a lookup table with defaults. Review a
new journal and the next build *fails* until its field and quartile are filled
in — which is the only moment anyone will remember to look them up. Nothing here
guesses a quartile, because a wrong one on a CV is worse than a missing section.

The archive lives outside the repo, so ``cv/review-service.tex`` is committed:
a fresh clone can rebuild the CV without it. When ``$REVIEWER_DIR`` is absent
this script skips with exit 0 and the committed file is used as-is.

    python scripts/build_review_service.py
    python scripts/build_review_service.py --dry-run
    REVIEWER_DIR=/elsewhere python scripts/build_review_service.py

Exit code is 0 when the file is up to date (or deliberately skipped), 1 when the
registry and the archive disagree.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "cv" / "journals.yaml"
OUTPUT = ROOT / "cv" / "review-service.tex"

DEFAULT_REVIEWER_DIR = os.environ.get("REVIEWER_DIR", "~/Documents/Community/Reviewer")

# Record folders are dated two ways: "2025-10-08_黄河水粮能指数" (current) and
# "2020-05_美国大坝" (older, no day). Anything else is not a review record.
RECORD_DATE = re.compile(r"^(\d{4})-(\d{2})(?:-\d{2})?_")

# Quartiles print as "(Q1)". "n/a" is for journals with no JCR ranking at all
# (not SCIE-indexed, or too new) — they print with no parenthetical rather than
# an invented one.
QUARTILES = ("Q1", "Q2", "Q3", "Q4")
UNRANKED = "n/a"

# TeX specials that turn up in journal names. Backslash is not among them: no
# journal name contains one, and escaping it properly would need \textbackslash.
TEX_ESCAPES = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "$": r"\$"}


@dataclass(frozen=True)
class Review:
    """One reviewed manuscript, identified by the folder it is filed in."""

    journal: str  # the journal directory name, i.e. the registry key
    folder: str  # the dated subfolder name
    year: int
    month: int

    @property
    def record_id(self) -> str:
        """How this record is named in the registry's `exclude_records`."""
        return f"{self.journal}/{self.folder}"


@dataclass(frozen=True)
class Journal:
    """A journal as it will be printed: registry metadata plus its reviews."""

    key: str
    name: str
    field: str
    quartile: str
    reviews: tuple[Review, ...]

    @property
    def count(self) -> int:
        return len(self.reviews)

    @property
    def latest(self) -> tuple[int, int]:
        return max((r.year, r.month) for r in self.reviews)

    @property
    def sort_key(self) -> tuple:
        # Most recently reviewed first, within each field. The year is printed
        # alongside each journal precisely because of this: an order the reader
        # cannot see gets read as a ranking, and this one is not a ranking.
        return (tuple(-n for n in self.latest), self.name.lower())


class Report:
    """Collects problems so one run reports every one, not just the first."""

    def __init__(self) -> None:
        self.problems: list[str] = []
        # Missing quartiles are collected apart from everything else. Filling
        # the registry in is normally a bulk job — one line per journal reads
        # as a checklist, where 33 copies of the same sentence does not.
        self.needs_quartile: list[str] = []

    def fail(self, message: str) -> None:
        self.problems.append(message)

    def needs_a_quartile(self, journal: str, found: str) -> None:
        self.needs_quartile.append(f"{journal}  (currently: {found or 'empty'})")

    def note(self, message: str) -> None:
        print(f"note  {message}")

    def flush(self) -> bool:
        """Print everything collected. True when the run may continue."""
        if not self.problems and not self.needs_quartile:
            return True
        total = len(self.problems) + len(self.needs_quartile)
        print(f"\n❌ {total} problem(s) between the archive and cv/journals.yaml:\n")
        for p in self.problems:
            print(f"  • {p}")
        if self.needs_quartile:
            print(
                f"  • {len(self.needs_quartile)} journal(s) still need a verified "
                f"`quartile:` — one of {', '.join(QUARTILES)}, or `{UNRANKED}` for a "
                f"journal with no JCR ranking at all:\n"
            )
            for line in self.needs_quartile:
                print(f"      {line}")
        return False


def tex(text: str) -> str:
    return "".join(TEX_ESCAPES.get(ch, ch) for ch in text)


def scan_archive(reviewer_dir: Path) -> tuple[dict[str, list[Review]], list[str]]:
    """Read the archive. Returns reviews by journal, and journals with none."""
    by_journal: dict[str, list[Review]] = defaultdict(list)
    empty: list[str] = []
    for journal_dir in sorted(p for p in reviewer_dir.iterdir() if p.is_dir()):
        found = []
        for record in sorted(p for p in journal_dir.iterdir() if p.is_dir()):
            match = RECORD_DATE.match(record.name)
            if not match:
                continue
            found.append(
                Review(
                    journal=journal_dir.name,
                    folder=record.name,
                    year=int(match.group(1)),
                    month=int(match.group(2)),
                )
            )
        if found:
            by_journal[journal_dir.name] = found
        else:
            empty.append(journal_dir.name)
    return dict(by_journal), empty


def load_registry() -> dict:
    if not REGISTRY.is_file():
        sys.exit(f"❌ {REGISTRY.relative_to(ROOT)} not found — it is a tracked source file.")
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    data.setdefault("journals", {})
    data.setdefault("field_order", [])
    data.setdefault("exclude_records", [])
    data.setdefault("checked", None)
    return data


def build(
    by_journal: dict[str, list[Review]], empty: list[str], registry: dict, report: Report
) -> list[Journal]:
    """Join archive and registry, collecting every disagreement into `report`."""
    entries: dict = registry["journals"]
    excluded = set(registry["exclude_records"])
    field_order: list[str] = registry["field_order"]

    for record_id in sorted(excluded):
        journal = record_id.split("/", 1)[0]
        if journal not in by_journal:
            report.fail(f"exclude_records lists `{record_id}`, but no such journal folder exists")

    # Folders with no dated record: either deliberately skipped, or a gap to fix
    # in the archive. Never patched up here — the archive is the source of truth.
    for name in empty:
        entry = entries.get(name)
        if isinstance(entry, dict) and entry.get("skip"):
            continue
        report.note(
            f"`{name}` has no dated subfolder, so it is not listed — "
            f"add a `YYYY-MM_title` folder to include it, or give it `skip:` in the registry"
        )

    journals: list[Journal] = []
    for key, reviews in sorted(by_journal.items()):
        entry = entries.get(key)
        if entry is None:
            report.fail(
                f"`{key}` has {len(reviews)} review(s) but no entry in cv/journals.yaml — add:\n"
                f"      {key}:\n"
                f"        field: <one of {', '.join(field_order) or '...'}>\n"
                f"        quartile: <Q1|Q2|Q3|Q4|n/a>\n"
                f"        source: <url you verified the quartile against>"
            )
            continue
        if entry.get("skip"):
            continue

        kept = [r for r in reviews if r.record_id not in excluded]
        if not kept:
            report.note(f"`{key}`: every record is in exclude_records, so it is not listed")
            continue

        field = entry.get("field")
        quartile = str(entry.get("quartile", "")).strip()
        if not field:
            report.fail(f"`{key}` has no `field:` in cv/journals.yaml")
        elif field_order and field not in field_order:
            report.fail(f"`{key}` has field `{field}`, which is not in `field_order`")
        if quartile not in QUARTILES and quartile != UNRANKED:
            report.needs_a_quartile(key, quartile)
        if field and quartile:
            journals.append(
                Journal(
                    key=key,
                    name=entry.get("name") or key,
                    field=field,
                    quartile=quartile,
                    reviews=tuple(kept),
                )
            )

    for key, entry in sorted(entries.items()):
        if not isinstance(entry, dict) or entry.get("skip"):
            continue
        if key not in by_journal:
            report.note(f"cv/journals.yaml has `{key}`, but the archive has no such folder")

    return journals


def render(journals: list[Journal], field_order: list[str]) -> str:
    grouped: dict[str, list[Journal]] = defaultdict(list)
    for journal in journals:
        grouped[journal.field].append(journal)
    fields = [f for f in field_order if f in grouped]

    total_reviews = sum(j.count for j in journals)
    since = min(r.year for j in journals for r in j.reviews)
    top = sum(1 for j in journals if j.quartile == "Q1")

    lines = [
        "% Generated by scripts/build_review_service.py from $REVIEWER_DIR — do not edit.",
        "% Change cv/journals.yaml or the review archive, then run `make update-cv`.",
        "",
        f"\\textnormal{{Peer reviewer for \\textbf{{{len(journals)}}} journals "
        f"(\\textbf{{{total_reviews}}} reviews since {since}) across "
        f"\\textbf{{{len(fields)}}} fields; \\textbf{{{top}}} of them are top-quartile "
        f"(Q1) in their JCR category.}}",
    ]
    for field in fields:
        items = []
        for journal in sorted(grouped[field], key=lambda j: j.sort_key):
            # Journal names italic, as everywhere else in the CV; the quartile
            # and the repeat count stay upright so they read as annotations.
            # \mbox keeps a name whole: this is a dense run of proper nouns, and
            # letting TeX break inside one gives "Envi-ronmental Modelling".
            # Every name here is far shorter than the measure, and the "·"
            # separators leave plenty of legal break points between them.
            item = f"\\mbox{{\\textit{{{tex(journal.name)}}}}}"
            # The parenthetical carries the quartile and the year of the most
            # recent review; a journal with no quartile still shows its year.
            year = journal.latest[0]
            if journal.quartile != UNRANKED:
                item += f" ({journal.quartile}, {year})"
            else:
                item += f" ({year})"
            items.append(item)
        lines += [
            "",
            "\\vspace{0.35em}",
            f"\\textnormal{{\\textbf{{{tex(field)}}}\\enspace "
            + " $\\cdot$ ".join(items)
            + "}",
        ]
    # Ragged right, not justified. Justifying a dense run of unbreakable proper
    # nouns leaves TeX two bad options: hyphenate a journal title mid-word, or
    # stretch the interword space until the bold run-in headings come apart.
    # Ragged right removes both pressures and reads well for a list like this.
    #
    # The group MUST close after a \par: TeX reads \rightskip when it breaks
    # the paragraph, so closing first restores justification and the last block
    # silently reverts.
    return "{\\raggedright\n" + "\n".join(lines) + "\n\\par}\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--reviewer-dir",
        default=DEFAULT_REVIEWER_DIR,
        help=f"peer-review archive (default: $REVIEWER_DIR or {DEFAULT_REVIEWER_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would be written and whether it differs, without writing",
    )
    args = parser.parse_args()

    reviewer_dir = Path(os.path.expanduser(args.reviewer_dir))
    if not reviewer_dir.is_dir():
        # Not an error: the archive is outside the repo, so any other clone —
        # or CI — builds the CV from the committed cv/review-service.tex.
        print(f"skip  {reviewer_dir} not found; keeping the committed review list")
        return 0

    report = Report()
    by_journal, empty = scan_archive(reviewer_dir)
    registry = load_registry()
    if registry["checked"]:
        # The quartiles come from public secondary sources, not from Clarivate.
        # Say so on every build rather than letting the caveat rot in a comment.
        report.note(
            f"quartiles were last checked {registry['checked']} against public "
            f"sources — confirm them against JCR before relying on the CV"
        )
    journals = build(by_journal, empty, registry, report)
    if not report.flush():
        return 1
    if not journals:
        print("❌ no journals to print — the archive scan came back empty")
        return 1

    content = render(journals, registry["field_order"])
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else None
    rel = OUTPUT.relative_to(ROOT)
    reviews = sum(j.count for j in journals)

    if args.dry_run:
        print(content)
        print(f"{'would change' if content != current else 'unchanged'}: {rel}")
        return 0

    if content == current:
        print(f"ok    {rel} is up to date ({len(journals)} journals, {reviews} reviews)")
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"✅ wrote {rel} ({len(journals)} journals, {reviews} reviews)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
