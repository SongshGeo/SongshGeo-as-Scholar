#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website  : https://cv.songshgeo.com/
"""
Sync the master BibTeX from a Zotero saved search — local, read-only, stdlib only.

This talks directly to your running Zotero (Better BibTeX) instead of a manual
"export to .bib". It resolves the members of a *saved search* (default
``#00.English my-pubs``), keeps only journal / conference articles, and merges
them into ``My-Publications.bib`` using an **add-only** policy: new papers are
appended, existing entries are left untouched (unless ``--update-existing``), and
nothing is ever deleted. Papers that dropped out of the search are only reported.

How it reads Zotero
-------------------
* **Membership** is computed from ``zotero.sqlite`` opened ``immutable=1``
  (read-only, bypasses locks) by evaluating the saved-search conditions —
  Zotero stores no membership table and exposes no "run search" endpoint.
* **Citation keys + BibTeX** come from Better BibTeX's JSON-RPC / export at
  ``http://localhost:23119`` — so **Zotero must be running with Better BibTeX**.

The membership evaluator supports exactly the condition operators this search
uses (``savedSearch``, ``itemType is/isNot``, ``tag is/isNot``,
``creator contains``, ``joinMode``); it **hard-errors on any other operator** so
editing the search in Zotero can never silently produce a wrong result.

Usage
-----
    python scripts/sync_pubs_from_zotero.py [--dry-run] [--search NAME]
        [--bib My-Publications.bib] [--since YEAR] [--update-existing]

``--dry-run`` prints the plan and writes nothing. Run without it to write the bib
(the ``make sync-pubs`` target wraps this with a confirmation prompt and then
drives the existing create-pages / auto-tag / update-publist steps).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request

# ── Config (env-overridable, mirrors the zotero-search skill) ──────────────── #
DATA_DIR = os.path.expanduser(os.environ.get("ZOTERO_DATA_DIR", "~/Zotero"))
API_BASE = os.environ.get("ZOTERO_LOCAL_API", "http://localhost:23119").rstrip("/")
DEFAULT_SEARCH = "#00.English my-pubs"
# Item types that become publication pages (see plan: journal articles only).
JOURNAL_TYPES = {"journalArticle", "conferencePaper"}
BBT_TRANSLATOR = "Better BibLaTeX"  # matches the existing biblatex style of the bib
TITLE_THRESHOLD = 0.8               # same default as check_missing_publications_enhanced
TIMEOUT = 30

# "Real" bibliographic items: not deleted, not an attachment/note/annotation.
_REAL = ("i.itemID NOT IN (SELECT itemID FROM deletedItems) "
         "AND i.itemTypeID NOT IN (SELECT itemTypeID FROM itemTypes "
         "WHERE typeName IN ('attachment','note','annotation'))")


# ── Small utilities (mirrors check_missing_publications_enhanced) ──────────── #
def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace — for fuzzy matching."""
    normalized = re.sub(r"[^\w\s]", " ", (title or "").lower())
    return re.sub(r"\s+", " ", normalized).strip()


def similarity(a: str, b: str) -> float:
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def norm_doi(doi: str) -> str:
    return (doi or "").strip().lower().rstrip("/")


# ── Zotero SQLite (read-only) ──────────────────────────────────────────────── #
def _conn() -> sqlite3.Connection:
    db = os.path.join(DATA_DIR, "zotero.sqlite")
    if not os.path.isfile(db):
        sys.exit(f"❌ zotero.sqlite not found at {db} (set ZOTERO_DATA_DIR).")
    conn = sqlite3.connect(f"file:{urllib.parse.quote(db)}?immutable=1", uri=True)
    conn.execute("PRAGMA query_only = ON;")  # never write, ever
    conn.row_factory = sqlite3.Row
    return conn


class SavedSearch:
    """Read a saved search and evaluate its member item set from SQLite."""

    def __init__(self, conn: sqlite3.Connection):
        self.c = conn
        self.universe = {r["itemID"] for r in conn.execute(
            f"SELECT i.itemID FROM items i WHERE {_REAL}")}

    # -- condition primitives (each returns a set of itemIDs) --
    def _by_type(self, typ: str) -> set:
        return {r["itemID"] for r in self.c.execute(
            f"SELECT i.itemID FROM items i JOIN itemTypes t ON t.itemTypeID=i.itemTypeID "
            f"WHERE {_REAL} AND t.typeName=?", (typ,))}

    def _by_tag(self, name: str) -> set:
        return {r["itemID"] for r in self.c.execute(
            f"SELECT it.itemID FROM itemTags it JOIN tags t ON t.tagID=it.tagID "
            f"JOIN items i ON i.itemID=it.itemID WHERE {_REAL} AND t.name=?", (name,))}

    def _by_creator_contains(self, value: str) -> set:
        """Match Zotero 'creator contains': substring over name field combos."""
        v = value.strip().lower()
        out = set()
        for r in self.c.execute(
                "SELECT ic.itemID AS iid, cr.firstName AS fn, cr.lastName AS ln "
                "FROM itemCreators ic JOIN creators cr ON cr.creatorID=ic.creatorID"):
            fn, ln = (r["fn"] or ""), (r["ln"] or "")
            cands = (ln, fn, f"{fn} {ln}", f"{ln} {fn}", f"{ln}, {fn}", f"{fn}{ln}", f"{ln}{fn}")
            if any(v in cand.lower() for cand in cands):
                out.add(r["iid"])
        return out & self.universe

    def _conditions(self, sid: int) -> list:
        return [dict(r) for r in self.c.execute(
            "SELECT condition, operator, value FROM savedSearchConditions "
            "WHERE savedSearchID=? ORDER BY searchConditionID", (sid,))]

    def id_by_name(self, name: str):
        r = self.c.execute(
            "SELECT savedSearchID FROM savedSearches WHERE savedSearchName=?", (name,)).fetchone()
        return r["savedSearchID"] if r else None

    def _id_by_key(self, key: str):
        r = self.c.execute(
            "SELECT savedSearchID FROM savedSearches WHERE key=?", (key,)).fetchone()
        return r["savedSearchID"] if r else None

    def evaluate(self, sid: int, _seen=None) -> set:
        """Recursively evaluate a saved search to its member itemID set."""
        _seen = _seen or set()
        if sid in _seen:
            sys.exit(f"❌ Saved-search cycle detected at ID {sid}.")
        _seen.add(sid)

        join = "all"
        sets = []
        for cond in self._conditions(sid):
            name, op, val = cond["condition"], cond["operator"], cond["value"]
            if name == "joinMode":
                join = op
                continue
            if name == "creator" and op == "contains":
                s = self._by_creator_contains(val)
            elif name == "itemType" and op == "is":
                s = self._by_type(val)
            elif name == "itemType" and op == "isNot":
                s = self.universe - self._by_type(val)
            elif name == "tag" and op == "is":
                s = self._by_tag(val)
            elif name == "tag" and op == "isNot":
                s = self.universe - self._by_tag(val)
            elif name == "savedSearch" and op == "is":
                nested = self._id_by_key(val)
                if nested is None:
                    sys.exit(f"❌ Nested saved search '{val}' not found.")
                s = self.evaluate(nested, _seen)
            else:
                sys.exit(
                    f"❌ Unsupported saved-search condition: '{name} {op}'.\n"
                    f"   This tool only understands savedSearch / itemType / tag / "
                    f"creator-contains / joinMode.\n"
                    f"   Add support in sync_pubs_from_zotero.py before relying on it.")
            sets.append(s)

        if not sets:
            return set(self.universe)
        result = sets[0]
        for s in sets[1:]:
            result = (result & s) if join == "all" else (result | s)
        return result

    def item_meta(self, ids: set) -> dict:
        """itemID -> {key, itemType} for the given ids."""
        if not ids:
            return {}
        q = ("SELECT i.itemID AS iid, i.key AS k, t.typeName AS tn FROM items i "
             "JOIN itemTypes t ON t.itemTypeID=i.itemTypeID "
             f"WHERE i.itemID IN ({','.join('?' * len(ids))})")
        return {r["iid"]: {"key": r["k"], "itemType": r["tn"]} for r in self.c.execute(q, list(ids))}

    def titles(self, keys: list) -> dict:
        """itemKey -> title (for reporting items that have no citation key)."""
        if not keys:
            return {}
        q = ("SELECT i.key AS k, v.value AS title FROM items i "
             "JOIN itemData d ON d.itemID=i.itemID "
             "JOIN fields f ON f.fieldID=d.fieldID AND f.fieldName='title' "
             "JOIN itemDataValues v ON v.valueID=d.valueID "
             f"WHERE i.key IN ({','.join('?' * len(keys))})")
        return {r["k"]: r["title"] for r in self.c.execute(q, keys)}


# ── Better BibTeX JSON-RPC / export (needs Zotero running) ─────────────────── #
def _http(url: str, data: bytes | None = None) -> str:
    req = urllib.request.Request(
        url, data=data,
        headers={"Accept": "application/json", "Content-Type": "application/json",
                 "User-Agent": "sync-pubs-from-zotero/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def _rpc(method: str, params: list):
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": params}).encode()
    return json.loads(_http(f"{API_BASE}/better-bibtex/json-rpc", data=body)).get("result")


def require_bbt() -> None:
    try:
        _rpc("user.groups", [])
    except Exception:
        sys.exit(
            "❌ Can't reach Better BibTeX at " + API_BASE + ".\n"
            "   Open Zotero (with the Better BibTeX plugin installed) and retry —\n"
            "   it is required to fetch citation keys and export BibTeX.")


def citation_keys(item_keys: list) -> dict:
    """itemKey -> Better BibTeX citekey (missing keys omitted)."""
    if not item_keys:
        return {}
    return {k: v for k, v in (_rpc("item.citationkey", [item_keys]) or {}).items() if v}


def export_biblatex(citekeys: list) -> str:
    if not citekeys:
        return ""
    res = _rpc("item.export", [sorted(citekeys), BBT_TRANSLATOR])
    return res if isinstance(res, str) else (res[-1] if isinstance(res, list) else str(res))


# ── BibTeX parsing / merge ─────────────────────────────────────────────────── #
_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", re.DOTALL)


def parse_entries(text: str) -> list:
    """Return [{key, type, raw, title, normalized_title, doi}] preserving source order."""
    out = []
    for m in _ENTRY_RE.finditer(text):
        etype, key, body = m.group(1), m.group(2), m.group(3)
        title = re.search(r"title\s*=\s*[{\"'](.*?)[}\"']", body, re.DOTALL)
        doi = re.search(r"doi\s*=\s*[{\"'](.*?)[}\"']", body)
        title = (title.group(1).strip() if title else "")
        out.append({
            "key": key, "type": etype, "raw": m.group(0).strip(),
            "title": title, "normalized_title": normalize_title(title),
            "doi": norm_doi(doi.group(1) if doi else ""),
        })
    return out


def classify(exported: list, existing: list) -> dict:
    """Split exported entries into new / duplicate (same paper, other key) / already-present."""
    by_key = {e["key"] for e in existing}
    by_doi = {e["doi"]: e["key"] for e in existing if e["doi"]}
    result = {"new": [], "present": [], "duplicate": []}
    for e in exported:
        if e["key"] in by_key:
            result["present"].append(e)
        elif e["doi"] and e["doi"] in by_doi:
            e["dup_of"] = by_doi[e["doi"]]
            e["dup_reason"] = "same DOI"
            result["duplicate"].append(e)
        else:
            best, score = None, 0.0
            for x in existing:
                if x["normalized_title"] and e["normalized_title"]:
                    s = similarity(x["normalized_title"], e["normalized_title"])
                    if s > score and s >= TITLE_THRESHOLD:
                        best, score = x["key"], s
            if best:
                e["dup_of"], e["dup_reason"] = best, f"title {score:.0%}"
                result["duplicate"].append(e)
            else:
                result["new"].append(e)
    return result


def entry_year(raw: str) -> str:
    m = re.search(r"\b(?:date|year)\s*=\s*\{?\D*(\d{4})", raw)
    return m.group(1) if m else ""


def is_placeholder_key(key: str) -> bool:
    """A key Zotero/BBT auto-minted for want of a real citekey (not <author><year>)."""
    return bool(re.match(r"(?i)^(zotero-item-|item[-_]?\d|[A-Z0-9]{8}$)", key)) \
        and not re.match(r"^[a-z]+\d{4}", key)


# ── Reporting ──────────────────────────────────────────────────────────────── #
def hr(title: str) -> None:
    print("\n" + "─" * 68 + f"\n{title}\n" + "─" * 68)


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync My-Publications.bib from a Zotero saved search.")
    ap.add_argument("--search", default=DEFAULT_SEARCH, help=f"Saved-search name (default: {DEFAULT_SEARCH!r})")
    ap.add_argument("--bib", default="My-Publications.bib", help="Master BibTeX to update")
    ap.add_argument("--since", type=int, default=None, help="Only add papers with year >= SINCE")
    ap.add_argument("--dry-run", action="store_true", help="Print the plan; write nothing")
    ap.add_argument("--update-existing", action="store_true",
                    help="Also overwrite existing entries in place with the Zotero version "
                         "(default: never touch existing entries)")
    args = ap.parse_args()

    require_bbt()

    # 1) Resolve saved-search membership from SQLite (read-only).
    with _conn() as conn:
        ss = SavedSearch(conn)
        sid = ss.id_by_name(args.search)
        if sid is None:
            sys.exit(f"❌ Saved search {args.search!r} not found in Zotero.")
        members = ss.evaluate(sid)
        meta = ss.item_meta(members)
        journal_keys = [m["key"] for m in meta.values() if m["itemType"] in JOURNAL_TYPES]
        # 2) Map to Better BibTeX citation keys (needs Zotero running).
        ck = citation_keys(journal_keys)
        no_citekey = [k for k in journal_keys if k not in ck]
        no_citekey_titles = ss.titles(no_citekey)

    print(f"🔎 Saved search {args.search!r}: {len(members)} items, "
          f"{len(journal_keys)} journal/conference, {len(ck)} with citation keys.")

    # 3) Export those citekeys as biblatex.
    exported_text = export_biblatex(list(ck.values()))
    exported = parse_entries(exported_text)
    if args.since:
        kept = [e for e in exported if not entry_year(e["raw"]) or int(entry_year(e["raw"])) >= args.since]
        dropped = len(exported) - len(kept)
        if dropped:
            print(f"   --since {args.since}: ignoring {dropped} older paper(s).")
        exported = kept

    # 4) Classify against the current bib (add-only).
    if not os.path.isfile(args.bib):
        sys.exit(f"❌ Bib file not found: {args.bib}")
    existing_text = open(args.bib, encoding="utf-8").read()
    existing = parse_entries(existing_text)
    buckets = classify(exported, existing)
    search_citekeys = set(ck.values())
    # Existing bib entries no longer represented in the search (advisory only).
    # Exclude anything the search *does* cover — same key, same DOI/title, or the
    # fuzzy dup-target of an exported entry (a stale placeholder key still counts).
    exported_dois = {e["doi"] for e in exported if e["doi"]}
    exported_titles = {e["normalized_title"] for e in exported if e["normalized_title"]}
    dup_targets = {e["dup_of"] for e in buckets["duplicate"]}
    orphans = [x for x in existing
               if x["key"] not in search_citekeys
               and x["key"] not in dup_targets
               and x["doi"] not in exported_dois
               and x["normalized_title"] not in exported_titles]

    # ── Report ──
    hr(f"NEW — will be added to {os.path.basename(args.bib)} ({len(buckets['new'])})")
    for e in sorted(buckets["new"], key=lambda x: x["key"]):
        print(f"   + {e['key']}  ({entry_year(e['raw']) or '?'})  {e['title'][:60]}")
    if not buckets["new"]:
        print("   (none — bib already matches the search)")

    if buckets["duplicate"]:
        hr(f"ALREADY IN BIB UNDER ANOTHER KEY — skipped ({len(buckets['duplicate'])})")
        for e in buckets["duplicate"]:
            hint = "  ← stale key, consider renaming" if is_placeholder_key(e["dup_of"]) else ""
            print(f"   ~ {e['key']} ≈ {e['dup_of']} ({e['dup_reason']})  {e['title'][:46]}{hint}")

    if no_citekey:
        hr(f"NO BETTER BIBTEX CITATION KEY — skipped ({len(no_citekey)})")
        print("   Pin a citation key in Zotero (right-click ▸ Better BibTeX) to include these:")
        for k in no_citekey:
            print(f"   ! {k}  {(no_citekey_titles.get(k) or '')[:56]}")

    if orphans:
        hr(f"IN BIB BUT NOT IN SEARCH — review (advisory, nothing deleted) ({len(orphans)})")
        print("   These stay in the bib; remove them by hand if they no longer belong.")
        for x in sorted(orphans, key=lambda x: x["key"]):
            print(f"   ? {x['key']}  {x['title'][:60]}")

    if args.update_existing and buckets["present"]:
        hr(f"REFRESH — existing entries overwritten from Zotero ({len(buckets['present'])})")
        for e in sorted(buckets["present"], key=lambda x: x["key"]):
            print(f"   ↻ {e['key']}")

    # ── Write ──
    to_add = buckets["new"]
    if args.dry_run:
        print(f"\n💡 Dry run — nothing written. {len(to_add)} entr"
              f"{'y' if len(to_add) == 1 else 'ies'} would be appended to {args.bib}.")
        return 0

    new_text = existing_text
    if args.update_existing:
        present_by_key = {e["key"]: e for e in buckets["present"]}
        for x in existing:
            if x["key"] in present_by_key:
                new_text = new_text.replace(x["raw"], present_by_key[x["key"]]["raw"], 1)

    if to_add:
        addition = "\n\n".join(e["raw"] for e in sorted(to_add, key=lambda x: x["key"]))
        new_text = new_text.rstrip() + "\n\n" + addition + "\n"

    if new_text != existing_text:
        with open(args.bib, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"\n✅ Wrote {args.bib}: +{len(to_add)} new"
              + (f", refreshed {len(buckets['present'])}" if args.update_existing else "")
              + ".")
    else:
        print(f"\n✅ {args.bib} already up to date — no changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
