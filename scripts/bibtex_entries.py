"""Shared BibTeX entry splitter.

Three scripts used to carry their own copy of this regex and they had drifted:
two spelled the body `([^@]*?)`, one `(.*?)`. The `[^@]` variants cannot step
over an `@` inside a field (an e-mail in `note`, an ORCID URL, …), so the
lookahead never reaches the next entry and the whole entry is dropped without
a word — leaving the three scripts disagreeing about which citekeys exist.

Import from here instead of re-deriving the pattern.
"""

from __future__ import annotations

import re
from typing import Iterator, NamedTuple

# Body is `.*?` on purpose: an entry may legitimately contain '@'. The lookahead
# is what ends an entry — a '@' in the first column of a following line.
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", re.DOTALL)


class Entry(NamedTuple):
    """One parsed `@type{key, ...}` block."""

    type: str
    key: str
    body: str
    raw: str


def iter_entries(text: str) -> Iterator[Entry]:
    """Yield every BibTeX entry in `text`, in source order."""
    for m in ENTRY_RE.finditer(text):
        yield Entry(type=m.group(1), key=m.group(2), body=m.group(3), raw=m.group(0).strip())


def entry_year(raw: str) -> str:
    """Four-digit year from a `date =` or `year =` field; '' when absent."""
    m = re.search(r"\b(?:date|year)\s*=\s*\{?\D*(\d{4})", raw)
    return m.group(1) if m else ""


def field(body: str, name: str) -> str:
    """Value of a brace- or quote-delimited field, stripped; '' when absent.

    The same three regexes (title, author, doi) were copy-pasted across the
    scripts. Same drift risk as the entry pattern, so they live here too.
    """
    m = re.search(rf"""\b{name}\s*=\s*[{{"'](.*?)[}}"']""", body, re.DOTALL)
    return m.group(1).strip() if m else ""
