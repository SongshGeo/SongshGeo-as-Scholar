#!/usr/bin/env python3
"""
Check missing publications in Hugo site.

Compare a master BibTeX file with existing publication folders to find
which publications haven't been created yet.

Usage:
    python check_missing_publications.py <path_to_master.bib> [--lang en|zh]
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, Set

from bibtex_entries import field, iter_entries


def parse_bibtex_keys(bib_file: str) -> Dict[str, dict]:
    """
    Parse BibTeX file and extract citation keys with metadata.

    Args:
        bib_file: Path to .bib file

    Returns:
        Dictionary mapping citation keys to entry metadata
    """
    entries = {}

    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for entry in iter_entries(content):
        entry_type = entry.type
        key = entry.key
        fields = entry.body

        title = field(fields, 'title')
        authors = field(fields, 'author')

        # Year is numeric-only on purpose: "submitted" etc. are not years.
        year_match = re.search(r'year\s*=\s*[{"\']*(\d{4})[}"\',]*', fields)
        year = year_match.group(1) if year_match else ''

        entries[key] = {
            'type': entry_type,
            'title': title,
            'year': year,
            'authors': authors
        }

    return entries


def get_existing_publications(content_dir: str, lang: str = 'en') -> Set[str]:
    """
    Get set of existing publication folder names.

    Args:
        content_dir: Base content directory
        lang: Language code (en or zh)

    Returns:
        Set of folder names (citation keys)
    """
    pub_dir = Path(content_dir) / lang / 'publication'

    if not pub_dir.exists():
        return set()

    existing = set()
    for item in pub_dir.iterdir():
        if item.is_dir() and (item / 'index.md').exists():
            existing.add(item.name)

    return existing


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check for missing publications in Hugo site'
    )
    parser.add_argument(
        'bib_file',
        help='Path to master BibTeX file'
    )
    parser.add_argument(
        '--lang',
        default='en',
        choices=['en', 'zh'],
        help='Language to check (default: en)'
    )
    parser.add_argument(
        '--content-dir',
        default='content',
        help='Content directory (default: content)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show details for all entries'
    )

    args = parser.parse_args()

    # Parse BibTeX file
    print(f"📖 Parsing BibTeX file: {args.bib_file}")
    try:
        bib_entries = parse_bibtex_keys(args.bib_file)
        print(f"   Found {len(bib_entries)} entries in BibTeX file\n")
    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.bib_file}")
        return 1
    except Exception as e:
        print(f"❌ Error parsing BibTeX file: {e}")
        return 1

    # Get existing publications
    print(f"📁 Checking existing publications in {args.content_dir}/{args.lang}/publication/")
    existing_pubs = get_existing_publications(args.content_dir, args.lang)
    print(f"   Found {len(existing_pubs)} existing publication folders\n")

    # Find missing publications
    missing_keys = set(bib_entries.keys()) - existing_pubs

    if not missing_keys:
        print("✅ All publications from BibTeX file have corresponding folders!")
        return 0

    # Report missing publications
    print(f"⚠️  Found {len(missing_keys)} missing publications:\n")
    print("=" * 80)

    for i, key in enumerate(sorted(missing_keys), 1):
        entry = bib_entries[key]
        print(f"{i}. [{key}]")
        print(f"   Type:    {entry['type']}")
        if entry['year']:
            print(f"   Year:    {entry['year']}")
        if entry['title']:
            title = entry['title'].replace('\n', ' ').strip()
            if len(title) > 70:
                title = title[:67] + '...'
            print(f"   Title:   {title}")
        if args.verbose and entry['authors']:
            authors = entry['authors'].replace('\n', ' ').strip()
            if len(authors) > 70:
                authors = authors[:67] + '...'
            print(f"   Authors: {authors}")
        print()

    # Summary
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   Total entries in BibTeX:     {len(bib_entries)}")
    print(f"   Existing publication pages:  {len(existing_pubs)}")
    print(f"   Missing publication pages:   {len(missing_keys)}")
    print(f"\n💡 Tip: Use 'hugo import --bibtex {args.bib_file}' to create pages for missing entries")

    return 0


if __name__ == '__main__':
    exit(main())
