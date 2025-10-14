#!/usr/bin/env python3
"""
Create publication page templates from BibTeX entries.

This script generates Hugo publication page templates for entries
that don't yet have corresponding folders.

Usage:
    python create_publication_template.py <path_to_master.bib> [--lang en|zh] [--dry-run]
"""

import argparse
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Set


def parse_bibtex_entry(entry_text: str, key: str) -> dict:
    """Parse a single BibTeX entry and extract fields."""
    fields = {
        'key': key,
        'title': '',
        'authors': [],
        'year': '',
        'doi': '',
        'abstract': '',
        'journal': '',
        'volume': '',
        'pages': '',
        'url': '',
    }
    
    # Extract title
    title_match = re.search(r'title\s*=\s*[{"]([^}"]+)[}"]', entry_text, re.DOTALL)
    if title_match:
        fields['title'] = title_match.group(1).strip().replace('\n', ' ')
    
    # Extract authors
    author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', entry_text, re.DOTALL)
    if author_match:
        author_str = author_match.group(1)
        # Split by 'and' for multiple authors
        authors = [a.strip() for a in re.split(r'\s+and\s+', author_str)]
        fields['authors'] = authors
    
    # Extract year
    year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}",]?', entry_text)
    if year_match:
        fields['year'] = year_match.group(1)
    
    # Extract DOI
    doi_match = re.search(r'doi\s*=\s*[{"]([^}"]+)[}"]', entry_text)
    if doi_match:
        fields['doi'] = doi_match.group(1).strip()
    
    # Extract journal/booktitle
    journal_match = re.search(r'(?:journal|journaltitle|booktitle)\s*=\s*[{"]([^}"]+)[}"]', entry_text)
    if journal_match:
        fields['journal'] = journal_match.group(1).strip()
    
    # Extract abstract
    abstract_match = re.search(r'abstract\s*=\s*[{"]([^}"]+)[}"]', entry_text, re.DOTALL)
    if abstract_match:
        fields['abstract'] = abstract_match.group(1).strip().replace('\n', ' ')
    
    # Extract volume
    volume_match = re.search(r'volume\s*=\s*[{"]?([^}",]+)[}",]?', entry_text)
    if volume_match:
        fields['volume'] = volume_match.group(1).strip()
    
    # Extract pages
    pages_match = re.search(r'pages\s*=\s*[{"]?([^}",]+)[}",]?', entry_text)
    if pages_match:
        fields['pages'] = pages_match.group(1).strip()
    
    # Extract URL
    url_match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', entry_text)
    if url_match:
        fields['url'] = url_match.group(1).strip()
    
    return fields


def parse_bibtex_entries(bib_file: str) -> Dict[str, dict]:
    """Parse all BibTeX entries from file."""
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = {}
    pattern = r'@\w+\s*\{\s*([^,\s]+)\s*,([^@]*?)(?=\n@|\Z)'
    
    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        key = match.group(1)
        entry_text = match.group(2)
        entries[key] = parse_bibtex_entry(entry_text, key)
    
    return entries


def get_existing_publications(content_dir: str, lang: str = 'en') -> Set[str]:
    """Get set of existing publication folder names."""
    pub_dir = Path(content_dir) / lang / 'publication'
    if not pub_dir.exists():
        return set()
    
    existing = set()
    for item in pub_dir.iterdir():
        if item.is_dir() and (item / 'index.md').exists():
            existing.add(item.name)
    
    return existing


def generate_index_md(entry: dict, lang: str = 'en') -> str:
    """Generate index.md content from BibTeX entry."""
    # Format authors for Hugo
    authors = []
    for author in entry['authors'][:5]:  # Limit to first 5 authors
        # Try to identify if it's the site admin
        if any(name in author.lower() for name in ['song', 'shuang', '宋', '爽']):
            authors.append('  - admin')
        else:
            # Clean author name
            clean_name = author.replace(', ', ' ').replace(',', '')
            authors.append(f'  - {clean_name}')
    
    authors_yaml = '\n'.join(authors) if authors else '  - admin'
    
    # Determine publication type (default to journal article)
    pub_type = "'2'"  # 2 = Journal article
    
    # Format date
    year = entry['year'] or datetime.now().year
    date_str = f"'{year}-01-01T00:00:00Z'"
    
    # Generate title
    title = entry['title'].replace("'", "\\'")
    
    # Generate abstract
    abstract = entry['abstract'].replace("'", "\\'") if entry['abstract'] else ''
    
    # Generate publication info
    publication = entry['journal'].replace("'", "\\'") if entry['journal'] else ''
    
    # Template
    template = f"""---
title: '{title}'

# Authors
authors:
{authors_yaml}

date: {date_str}
"""
    
    # Add DOI if available
    if entry['doi']:
        template += f"""
hugoblox:
  ids:
    doi: '{entry['doi']}'
"""
    
    template += f"""
# Publication type
publication_types: [{pub_type}]

# Publication name
publication: '{publication}'
publication_short: ''
"""
    
    # Add abstract if available
    if abstract:
        template += f"""
abstract: '{abstract}'
"""
    
    # Add links section
    template += """
# Links (optional)
links: []

# Featured image
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Associated Projects (optional)
projects: []
---
"""
    
    return template


def create_publication_folder(entry: dict, content_dir: str, lang: str = 'en', 
                             bib_content: str = '', dry_run: bool = False):
    """Create publication folder with index.md and cite.bib."""
    pub_dir = Path(content_dir) / lang / 'publication' / entry['key']
    
    if dry_run:
        print(f"   [DRY RUN] Would create: {pub_dir}")
        return
    
    # Create directory
    pub_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index.md
    index_path = pub_dir / 'index.md'
    index_content = generate_index_md(entry, lang)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Create cite.bib if we have the original BibTeX
    if bib_content:
        cite_path = pub_dir / 'cite.bib'
        with open(cite_path, 'w', encoding='utf-8') as f:
            f.write(bib_content)
    
    print(f"   ✅ Created: {pub_dir}")


def extract_bib_entry(bib_file: str, key: str) -> str:
    """Extract a single BibTeX entry from file."""
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = rf'@\w+\s*\{{\s*{re.escape(key)}\s*,.*?(?=\n@|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    return match.group(0) if match else ''


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create publication page templates from BibTeX'
    )
    parser.add_argument('bib_file', help='Path to master BibTeX file')
    parser.add_argument('--lang', default='en', choices=['en', 'zh'],
                       help='Language (default: en)')
    parser.add_argument('--content-dir', default='content',
                       help='Content directory (default: content)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be created without actually creating')
    parser.add_argument('--force', action='store_true',
                       help='Overwrite existing folders')
    parser.add_argument('--only-missing', action='store_true', default=True,
                       help='Only create truly missing publications (default: True)')
    parser.add_argument('--all', action='store_true',
                       help='Create all publications, including those with title matches')
    
    args = parser.parse_args()
    
    # Handle conflicting options
    if args.all:
        args.only_missing = False
    
    # Parse BibTeX
    print(f"📖 Parsing BibTeX file: {args.bib_file}")
    try:
        entries = parse_bibtex_entries(args.bib_file)
        print(f"   Found {len(entries)} entries\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    # Get existing publications
    existing = get_existing_publications(args.content_dir, args.lang)
    print(f"📁 Found {len(existing)} existing publications\n")
    
    # Find missing publications
    missing_keys = set(entries.keys()) - existing
    
    if args.only_missing:
        # Use enhanced matching to find truly missing publications
        print("🔍 Using intelligent matching to find truly missing publications...")
        try:
            # Import the enhanced checker functions
            from check_missing_publications_enhanced import parse_bibtex_keys, get_existing_publications as get_existing_enhanced, find_matches
            
            # Parse with enhanced functions
            bib_entries_enhanced = parse_bibtex_keys(args.bib_file)
            existing_enhanced = get_existing_enhanced(args.content_dir, args.lang)
            
            # Find matches
            exact_matches, title_matches, truly_missing = find_matches(
                bib_entries_enhanced, existing_enhanced, 0.8
            )
            
            # Only create truly missing publications
            missing_keys = {entry['key'] for entry in truly_missing}
            
            print(f"   Found {len(exact_matches)} exact matches")
            print(f"   Found {len(title_matches)} title-based matches")
            print(f"   Found {len(truly_missing)} truly missing publications\n")
            
        except ImportError:
            print("   ⚠️  Enhanced checker not available, using simple matching")
            print(f"   Found {len(missing_keys)} missing publications\n")
    
    if not missing_keys:
        print("✅ All publications already have folders!")
        return 0
    
    print(f"🔨 Creating {len(missing_keys)} publication folders:\n")
    
    # Create folders
    created = 0
    for key in sorted(missing_keys):
        entry = entries[key]
        bib_content = extract_bib_entry(args.bib_file, key)
        
        try:
            create_publication_folder(entry, args.content_dir, args.lang, 
                                    bib_content, args.dry_run)
            created += 1
        except Exception as e:
            print(f"   ❌ Error creating {key}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Total missing publications: {len(missing_keys)}")
    print(f"   Successfully created:       {created}")
    
    if args.dry_run:
        print(f"\n💡 Remove --dry-run to actually create the folders")
    
    if args.only_missing:
        print(f"\n🔍 Note: Only created truly missing publications (used intelligent matching)")
        print(f"   Use --all to create all publications, including those with title matches")
    
    return 0


if __name__ == '__main__':
    exit(main())

