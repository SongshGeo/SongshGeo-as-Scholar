#!/usr/bin/env python3
"""Guard against committing a generated PDF that no longer matches its sources.

`static/uploads/pubs.pdf` and `static/uploads/SongshGeo_fullCV.pdf` are build
products of `publist/` and `cv/`, both driven by the one master
`My-Publications.bib`. They are tracked in git because Hugo serves them as
static assets — which means git will happily accept a commit where the source
moved and the PDF did not, and the site then advertises a stale CV.

Default mode (what the pre-commit hook runs) is a *staging* check: if a commit
touches a document's sources, that document's PDF has to be in the same commit.
It shells out to nothing but git, so it is fast enough to run on every commit.

``--rebuild`` additionally recompiles each document and compares the text of the
result against the PDF being committed, ignoring the date that LaTeX stamps in
on every run. That catches the case the staging check cannot see: a PDF that was
staged, but built from older sources. It needs a TeX installation plus
``pdftotext`` and takes roughly half a minute.

    python scripts/check_generated_pdfs.py
    python scripts/check_generated_pdfs.py --rebuild

Exit code is 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The master bibliography feeds every document here, so a change to it invalidates
# all of them.
MASTER_BIB = "My-Publications.bib"

# Files inside a document directory that are documentation, not build inputs.
NOT_A_BUILD_INPUT = {"README.md"}

# LaTeX stamps the build date into both documents (pubs.pdf via \maketitle, the CV
# via \today in its running header), so two builds of identical sources never
# produce identical text. Strip dates before comparing.
DATE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+(?:\d{1,2},\s*)?\d{4}\b"
)


@dataclass(frozen=True)
class Document:
    """A LaTeX document in this repo and the PDF it is published as."""

    name: str
    source_dir: str
    pdf: str
    make_target: str

    def staged_sources(self, staged: set[str]) -> list[str]:
        """Staged paths that would change this document's output."""
        touched = [
            path
            for path in staged
            if path.startswith(f"{self.source_dir}/")
            and Path(path).name not in NOT_A_BUILD_INPUT
        ]
        if MASTER_BIB in staged:
            touched.append(MASTER_BIB)
        return sorted(touched)


DOCUMENTS = (
    Document(
        name="publication list",
        source_dir="publist",
        pdf="static/uploads/pubs.pdf",
        make_target="update-publist",
    ),
    Document(
        name="full CV",
        source_dir="cv",
        pdf="static/uploads/SongshGeo_fullCV.pdf",
        make_target="update-cv",
    ),
)


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

    def note(self, message: str) -> None:
        print(f"skip  {message}")

    def exit_code(self) -> int:
        print()
        if self.failures:
            print(f"{len(self.failures)} of {self.checks} checks failed")
            return 1
        print(f"all {self.checks} checks passed")
        return 0


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def staged_paths() -> set[str]:
    """Paths staged for the commit being made (added, copied, modified, renamed)."""
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return {line for line in out.splitlines() if line}


def check_pdf_staged_with_its_sources(staged: set[str]) -> list[str]:
    problems = []
    for doc in DOCUMENTS:
        sources = doc.staged_sources(staged)
        if sources and doc.pdf not in staged:
            problems.append(
                f"{doc.name}: this commit changes {', '.join(sources)} "
                f"but not {doc.pdf} — run `make {doc.make_target}` and stage the PDF"
            )
    return problems


def pdf_text(pdf: Path) -> str:
    """Text of a PDF with build dates stripped, so two builds compare equal."""
    out = subprocess.run(
        ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
    ).stdout
    return DATE.sub("<date>", out)


def check_pdf_matches_a_fresh_build(doc: Document, staged: set[str]) -> list[str]:
    """Rebuild the document and compare it with the PDF being committed."""
    pdf = ROOT / doc.pdf
    with tempfile.TemporaryDirectory() as tmp:
        committed = Path(tmp) / "committed.pdf"
        if doc.pdf in staged:
            # Compare against the staged blob, which is what the commit will carry.
            committed.write_bytes(
                subprocess.run(
                    ["git", "show", f":{doc.pdf}"],
                    cwd=ROOT,
                    capture_output=True,
                    check=True,
                ).stdout
            )
        elif pdf.is_file():
            committed.write_bytes(pdf.read_bytes())
        else:
            return [f"{doc.name}: {doc.pdf} does not exist"]

        before = pdf_text(committed)
        build = subprocess.run(
            ["make", doc.make_target], cwd=ROOT, capture_output=True, text=True
        )
        if build.returncode != 0:
            return [
                f"{doc.name}: `make {doc.make_target}` failed — "
                f"run `make {doc.make_target}-verbose` to see why"
            ]
        if pdf_text(pdf) != before:
            return [
                f"{doc.name}: {doc.pdf} differs from a fresh build of {doc.source_dir}/ "
                f"— it was built from older sources; stage the rebuilt PDF"
            ]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="also recompile each document and diff it against the committed PDF",
    )
    args = parser.parse_args()

    report = Report()
    staged = staged_paths()
    report.check(
        "each generated PDF is staged alongside its sources",
        check_pdf_staged_with_its_sources(staged),
    )

    if args.rebuild:
        if shutil.which("pdftotext") is None:
            report.note("--rebuild needs pdftotext (brew install poppler)")
        else:
            for doc in DOCUMENTS:
                report.check(
                    f"{doc.pdf} matches a fresh build",
                    check_pdf_matches_a_fresh_build(doc, staged),
                )

    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main())
