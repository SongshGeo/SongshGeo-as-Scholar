#!/usr/bin/env python3
"""
Enhanced publication checker with intelligent matching.

This script compares a master BibTeX file with existing publication folders,
using both exact citation key matching and intelligent title-based matching
to identify truly missing publications vs. citation key variations.

Usage:
    python check_missing_publications_enhanced.py <path_to_master.bib> [--lang en|zh]
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple
from difflib import SequenceMatcher
from logger_config import setup_logger, log_section, log_success, log_warning, log_error, log_info


def similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    # Remove common punctuation and normalize whitespace
    normalized = re.sub(r'[^\w\s]', ' ', title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


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
    
    # Match BibTeX entries: @article{key, ...}
    pattern = r'@(\w+)\s*\{\s*([^,\s]+)\s*,([^@]*?)(?=\n@|\Z)'
    
    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        entry_type = match.group(1)
        key = match.group(2)
        fields = match.group(3)
        
        # Extract title if available
        title_match = re.search(r'title\s*=\s*[{"\'](.*?)[}"\']', fields, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ''
        
        # Extract year if available (numeric only; "submitted" etc. are ignored)
        year_match = re.search(r'year\s*=\s*[{"\']*(\d{4})[}"\',]*', fields)
        year = year_match.group(1) if year_match else ''

        # biblatex date (YYYY, YYYY-MM, YYYY-MM-DD, ...)
        date_match = re.search(r'\bdate\s*=\s*\{([^}]*)\}', fields, re.DOTALL)
        date_val = date_match.group(1).strip() if date_match else ''

        # Extract authors
        author_match = re.search(r'author\s*=\s*[{"\'](.*?)[}"\']', fields, re.DOTALL)
        authors = author_match.group(1).strip() if author_match else ''
        
        # Extract DOI
        doi_match = re.search(r'doi\s*=\s*[{"\'](.*?)[}"\']', fields)
        doi = doi_match.group(1).strip() if doi_match else ''
        
        entries[key] = {
            'type': entry_type,
            'title': title,
            'normalized_title': normalize_title(title),
            'year': year,
            'date': date_val,
            'authors': authors,
            'doi': doi
        }

    return entries


def has_publishable_bib_date(entry: dict) -> bool:
    """True if BibTeX has a concrete publication date (biblatex date or 4-digit year).

    Entries with only year=submitted / under review / no date are False.
    """
    date_raw = (entry.get('date') or '').strip()
    year_raw = (entry.get('year') or '').strip()
    if date_raw and re.match(r'^\d{4}', date_raw):
        return True
    if year_raw and re.match(r'^\d{4}$', year_raw):
        return True
    return False


def get_existing_publications(content_dir: str, lang: str = 'en') -> Dict[str, dict]:
    """
    Get existing publication folder names and their metadata.
    
    Args:
        content_dir: Base content directory
        lang: Language code (en or zh)
        
    Returns:
        Dictionary mapping folder names to their metadata
    """
    pub_dir = Path(content_dir) / lang / 'publication'
    
    if not pub_dir.exists():
        return {}
    
    existing = {}
    for item in pub_dir.iterdir():
        if item.is_dir() and (item / 'index.md').exists():
            # Check for PDF files in the folder
            has_pdf = bool(list(item.glob('*.pdf')))
            pdf_files = [f.name for f in item.glob('*.pdf')]
            
            # Try to read metadata from index.md
            try:
                with open(item / 'index.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title
                title_match = re.search(r'title:\s*[\'"](.*?)[\'"]', content)
                title = title_match.group(1) if title_match else ''
                
                # Extract year
                year_match = re.search(r'date:\s*[\'"](\d{4})', content)
                year = year_match.group(1) if year_match else ''
                
                # Extract DOI
                doi_match = re.search(r'doi:\s*[\'"](.*?)[\'"]', content)
                doi = doi_match.group(1) if doi_match else ''
                
                existing[item.name] = {
                    'title': title,
                    'normalized_title': normalize_title(title),
                    'year': year,
                    'doi': doi,
                    'has_pdf': has_pdf,
                    'pdf_files': pdf_files
                }
            except Exception:
                # If we can't read the file, just use the folder name
                existing[item.name] = {
                    'title': '',
                    'normalized_title': '',
                    'year': '',
                    'doi': '',
                    'has_pdf': has_pdf,
                    'pdf_files': pdf_files
                }
    
    return existing


def rename_files_in_folder(folder_path: Path, target_key: str, dry_run: bool = False) -> dict:
    """
    Rename cite.bib key and PDF files in a publication folder.
    
    Args:
        folder_path: Path to publication folder
        target_key: Target citation key (folder name)
        dry_run: If True, only preview changes
    
    Returns:
        Dict with rename results
    """
    results = {
        'cite_bib_renamed': False,
        'pdfs_renamed': [],
        'errors': []
    }
    
    # Rename cite.bib key
    cite_bib_path = folder_path / 'cite.bib'
    if cite_bib_path.exists():
        try:
            with open(cite_bib_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace the citation key in cite.bib
            # Match pattern: @article{oldkey, or @book{oldkey, etc.
            pattern = r'(@\w+\s*\{\s*)([^,\s]+)(\s*,)'
            match = re.search(pattern, content)
            
            if match:
                old_key = match.group(2)
                if old_key != target_key:
                    new_content = re.sub(pattern, rf'\1{target_key}\3', content, count=1)
                    
                    if dry_run:
                        results['cite_bib_renamed'] = f"Would rename: {old_key} -> {target_key}"
                    else:
                        with open(cite_bib_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        results['cite_bib_renamed'] = f"Renamed: {old_key} -> {target_key}"
        except Exception as e:
            results['errors'].append(f"Error renaming cite.bib: {e}")
    
    # Rename PDF files
    pdf_files = list(folder_path.glob('*.pdf'))
    for pdf_file in pdf_files:
        old_name = pdf_file.name
        # Keep the extension, replace the name
        new_name = f"{target_key}.pdf"
        
        if old_name != new_name:
            new_path = folder_path / new_name
            
            if dry_run:
                results['pdfs_renamed'].append(f"Would rename: {old_name} -> {new_name}")
            else:
                try:
                    pdf_file.rename(new_path)
                    results['pdfs_renamed'].append(f"Renamed: {old_name} -> {new_name}")
                except Exception as e:
                    results['errors'].append(f"Error renaming {old_name}: {e}")
    
    return results


def find_matches(bib_entries: Dict[str, dict], existing: Dict[str, dict], 
                title_threshold: float = 0.8) -> Tuple[Set[str], List[dict], List[dict]]:
    """
    Find matches between BibTeX entries and existing publications.
    
    Returns:
        - exact_matches: Set of citation keys that have exact folder matches
        - title_matches: List of dicts with title-based matches
        - truly_missing: List of dicts for truly missing publications
    """
    exact_matches = set()
    title_matches = []
    truly_missing = []
    
    for bib_key, bib_entry in bib_entries.items():
        # Check for exact match first
        if bib_key in existing:
            exact_matches.add(bib_key)
            continue
        
        # Check for title-based matches
        best_match = None
        best_similarity = 0
        
        for existing_key, existing_entry in existing.items():
            if existing_entry['normalized_title'] and bib_entry['normalized_title']:
                sim = similarity(existing_entry['normalized_title'], bib_entry['normalized_title'])
                if sim > best_similarity and sim >= title_threshold:
                    best_similarity = sim
                    best_match = existing_key
        
        if best_match:
            title_matches.append({
                'bib_key': bib_key,
                'existing_key': best_match,
                'similarity': best_similarity,
                'bib_title': bib_entry['title'],
                'existing_title': existing[best_match]['title'],
                'bib_year': bib_entry['year'],
                'existing_year': existing[best_match]['year'],
                'bib_doi': bib_entry['doi'],
                'existing_doi': existing[best_match]['doi']
            })
        else:
            truly_missing.append({
                'key': bib_key,
                'type': bib_entry['type'],
                'title': bib_entry['title'],
                'year': bib_entry['year'],
                'date': bib_entry.get('date', ''),
                'authors': bib_entry['authors'],
                'doi': bib_entry['doi']
            })
    
    return exact_matches, title_matches, truly_missing


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Enhanced check for missing publications with intelligent matching'
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
        '--title-threshold',
        type=float,
        default=0.8,
        help='Title similarity threshold for matching (default: 0.8)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show details for all entries'
    )
    parser.add_argument(
        '--check-pdf',
        action='store_true',
        help='Also check which publications are missing PDF files'
    )
    parser.add_argument(
        '--renaming',
        action='store_true',
        help='Rename cite.bib keys and PDF files to match folder names (citation keys)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview renaming without actually changing files (use with --renaming)'
    )
    parser.add_argument(
        '--prompt-create-missing',
        action='store_true',
        help='If BibTeX has entries with no site page, prompt to run create_publication_template (TTY only)'
    )
    parser.add_argument(
        '--all',
        dest='prompt_include_unpublished',
        action='store_true',
        help='With --prompt-create-missing: include entries without a calendar date (submitted, under review, …)'
    )

    args = parser.parse_args()
    
    # Setup logging
    log = setup_logger("check_missing_publications", verbose=True)
    
    # Parse BibTeX file
    log_section(log, "Parsing BibTeX file")
    log_info(log, f"File: {args.bib_file}")
    try:
        bib_entries = parse_bibtex_keys(args.bib_file)
        log_success(log, f"Found {len(bib_entries)} entries in BibTeX file")
    except FileNotFoundError:
        log_error(log, f"File not found: {args.bib_file}")
        return 1
    except Exception as e:
        log_error(log, f"Error parsing BibTeX file: {e}")
        return 1
    
    # Get existing publications
    log_section(log, "Checking existing publications")
    log_info(log, f"Directory: {args.content_dir}/{args.lang}/publication/")
    existing = get_existing_publications(args.content_dir, args.lang)
    log_success(log, f"Found {len(existing)} existing publication folders")
    
    # Find matches
    exact_matches, title_matches, truly_missing = find_matches(
        bib_entries, existing, args.title_threshold
    )
    
    # Report results
    log_section(log, "RESULTS")
    
    log_section(log, f"ON SITE — SAME CITATION KEY ({len(exact_matches)})")
    if exact_matches:
        for key in sorted(exact_matches):
            entry = bib_entries[key]
            print(f"   • {key}: {entry['title'][:60]}...")
    else:
        print("   None")
    
    print(f"\n🔍 SAME PAPER, DIFFERENT KEY? ({len(title_matches)})")
    print("   (Review these — may be duplicates or need a key rename)")
    if title_matches:
        for match in title_matches:
            print(f"\n   BibTeX: {match['bib_key']}")
            print(f"   Existing: {match['existing_key']}")
            print(f"   Similarity: {match['similarity']:.2f}")
            print(f"   BibTeX Title: {match['bib_title'][:60]}...")
            print(f"   Existing Title: {match['existing_title'][:60]}...")
            if match['bib_year'] and match['existing_year']:
                print(f"   Years: {match['bib_year']} vs {match['existing_year']}")
            if match['bib_doi'] and match['existing_doi']:
                if match['bib_doi'] == match['existing_doi']:
                    print(f"   DOI: ✅ Same ({match['bib_doi']})")
                else:
                    print(f"   DOI: ❌ Different ({match['bib_doi']} vs {match['existing_doi']})")
    else:
        print("   None")
    
    print(f"\n📭 NOT ON THE SITE YET ({len(truly_missing)})")
    print("   (In your BibTeX but no folder under content/.../publication/)")
    if truly_missing:
        for i, entry in enumerate(truly_missing, 1):
            print(f"\n   {i}. [{entry['key']}]")
            print(f"      Type:    {entry['type']}")
            pub = has_publishable_bib_date(bib_entries[entry['key']])
            print(f"      Pub date: {'yes (biblatex date or 4-digit year)' if pub else 'no (draft / submitted / under review)'}")
            if entry.get('date'):
                print(f"      Date:    {entry['date']}")
            elif entry.get('year'):
                print(f"      Year:    {entry['year']}")
            if entry['title']:
                title = entry['title'].replace('\n', ' ').strip()
                if len(title) > 70:
                    title = title[:67] + '...'
                print(f"      Title:   {title}")
            if args.verbose and entry['authors']:
                authors = entry['authors'].replace('\n', ' ').strip()
                if len(authors) > 70:
                    authors = authors[:67] + '...'
                print(f"      Authors: {authors}")
            if entry['doi']:
                print(f"      DOI:     {entry['doi']}")
        with_pub_date = sum(
            1 for e in truly_missing if has_publishable_bib_date(bib_entries[e['key']])
        )
        print(
            f"\n   ── {with_pub_date} with publication date · "
            f"{len(truly_missing) - with_pub_date} without (not offered for auto-create by default)"
        )
    else:
        print("   None")
    
    # Check for missing PDFs if requested
    if args.check_pdf:
        print(f"\n" + "=" * 80)
        print(f"📄 PDF FILES IN EACH FOLDER")
        print("=" * 80)
        print("   (Add a .pdf next to index.md if you want downloads + abstract extraction.)")
        
        publications_without_pdf = []
        for key, entry in existing.items():
            if not entry['has_pdf']:
                publications_without_pdf.append({
                    'key': key,
                    'title': entry['title'],
                    'year': entry['year']
                })
        
        print(f"\n📂 FOLDERS WITHOUT A PDF ({len(publications_without_pdf)}):")
        if publications_without_pdf:
            for i, pub in enumerate(publications_without_pdf, 1):
                print(f"\n   {i}. [{pub['key']}]")
                if pub['year']:
                    print(f"      Year:  {pub['year']}")
                if pub['title']:
                    title = pub['title'].replace('\n', ' ').strip()
                    if len(title) > 70:
                        title = title[:67] + '...'
                    print(f"      Title: {title}")
        else:
            print("   None — every folder has at least one PDF. 🎉")
        
        # Summary for PDFs
        publications_with_pdf = len(existing) - len(publications_without_pdf)
        print(f"\n   With PDF:    {publications_with_pdf}")
        print(f"   Without PDF: {len(publications_without_pdf)}")
        
        if publications_without_pdf:
            print(f"\n💡 Add PDFs when you can, then run: make extract-abstracts")
    
    # Rename files if requested
    if args.renaming:
        print(f"\n" + "=" * 80)
        print(f"📝 FILE RENAMING")
        print("=" * 80)
        
        if args.dry_run:
            print("\n⚠️  DRY RUN MODE - No files will be changed\n")
        
        pub_dir = Path(args.content_dir) / args.lang / 'publication'
        renamed_count = 0
        error_count = 0
        
        for key in sorted(exact_matches):
            folder_path = pub_dir / key
            if not folder_path.exists():
                continue
            
            results = rename_files_in_folder(folder_path, key, args.dry_run)
            
            # Only show output if something was renamed or errors occurred
            if results['cite_bib_renamed'] or results['pdfs_renamed'] or results['errors']:
                print(f"\n📁 [{key}]")
                
                if results['cite_bib_renamed']:
                    print(f"   📄 cite.bib: {results['cite_bib_renamed']}")
                    if not args.dry_run:
                        renamed_count += 1
                
                for pdf_rename in results['pdfs_renamed']:
                    print(f"   📄 PDF: {pdf_rename}")
                    if not args.dry_run:
                        renamed_count += 1
                
                for error in results['errors']:
                    print(f"   ❌ Error: {error}")
                    error_count += 1
        
        # Summary for renaming
        print(f"\n📊 Renaming Summary:")
        if args.dry_run:
            print(f"   Would rename items (dry run)")
        else:
            print(f"   Files renamed:  {renamed_count}")
            print(f"   Errors:         {error_count}")
        
        if args.dry_run:
            print(f"\n💡 Remove --dry-run to actually rename files")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"\n📊 SUMMARY")
    print(f"   BibTeX entries:           {len(bib_entries)}")
    print(f"   Folders on site:          {len(existing)}")
    print(f"   Matched by citation key:  {len(exact_matches)}")
    print(f"   Possible key duplicates:  {len(title_matches)}")
    print(f"   No Hugo page yet:         {len(truly_missing)}")
    
    if truly_missing and not args.prompt_create_missing:
        print(f"\n💡 Create missing pages (published entries only by default):")
        print(f"   poetry run python scripts/create_publication_template.py {args.bib_file}")
        print(f"   Add --include-unpublished for drafts (submitted, under review, …)")
    
    if title_matches:
        print(f"\n🔧 Title-based matches need a human check:")
        print(f"   Same paper under two keys, or two different papers? Adjust BibTeX or folder names.")
    
    if exact_matches and not args.renaming:
        print(f"\n🔧 Optional — align cite.bib / PDF filenames with folder names:")
        print(f"   poetry run python scripts/check_missing_publications_enhanced.py {args.bib_file} --renaming --dry-run")

    if args.prompt_create_missing and truly_missing:
        candidates = (
            list(truly_missing) if args.prompt_include_unpublished else [
                m for m in truly_missing
                if has_publishable_bib_date(bib_entries[m['key']])
            ]
        )
        if not candidates and truly_missing and not args.prompt_include_unpublished:
            print(
                "\n💡 None of the missing entries have a publication date in BibTeX "
                "(biblatex `date` starting with a year, or a 4-digit `year`)."
            )
            print("   Drafts are skipped for the create prompt by default.")
            print("   Re-run with --all to include them (or use create_publication_template.py --include-unpublished).")
        elif candidates:
            _prompt_create_missing_publications(args, candidates)

    return 0


def _prompt_create_missing_publications(
    args: argparse.Namespace,
    candidates: List[dict],
) -> None:
    """Offer one-shot creation of missing publication folders (interactive only)."""
    if not sys.stdin.isatty():
        print(
            "\n💡 Non-interactive session: skipping create prompt. Run:\n"
            f"   poetry run python scripts/create_publication_template.py {args.bib_file} --lang {args.lang}"
        )
        print("   Add --include-unpublished to create drafts (submitted, under review, …).")
        return

    n = len(candidates)
    print("\n" + "─" * 60)
    if args.prompt_include_unpublished:
        if n == 1:
            print("📭 1 BibTeX entry has no Hugo publication folder yet (including drafts).")
        else:
            print(f"📭 {n} BibTeX entries have no Hugo publication folders yet (including drafts).")
    else:
        if n == 1:
            print("📭 1 BibTeX entry with a publication date has no Hugo publication folder yet.")
        else:
            print(
                f"📭 {n} BibTeX entries with publication dates have no Hugo publication folders yet."
            )
    try:
        reply = input("Create these pages now? [y/N]: ").strip().lower()
    except EOFError:
        return
    if reply not in ("y", "yes"):
        print("   Skipped. You can run create_publication_template.py later.")
        return

    script = Path(__file__).resolve().parent / "create_publication_template.py"
    cmd = [
        sys.executable,
        str(script),
        args.bib_file,
        "--lang",
        args.lang,
    ]
    if args.prompt_include_unpublished:
        cmd.append("--include-unpublished")
    print(f"\n🔨 Running: {' '.join(cmd)}\n")
    try:
        subprocess.check_call(cmd, cwd=Path(args.bib_file).resolve().parent)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ create_publication_template.py exited with code {e.returncode}")
    except FileNotFoundError:
        print(f"\n❌ Could not run: {script}")


if __name__ == '__main__':
    exit(main())
