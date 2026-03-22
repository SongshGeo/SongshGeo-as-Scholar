#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

"""
Extract and summarize abstracts from PDFs in publication folders.

This script uses OpenAI and LangChain to:
1. Extract abstract from PDFs in publication folders
2. Generate a concise summary
3. Update the index.md file with the extracted information

Usage:
    # Process all publications with PDFs
    python extract_abstract_from_pdf.py
    
    # Process a specific publication
    python extract_abstract_from_pdf.py --key song2023b
    
    # Process English or Chinese publications
    python extract_abstract_from_pdf.py --lang en
    
    # Dry run (preview only)
    python extract_abstract_from_pdf.py --dry-run
    
    # Force re-extract even if abstract exists
    python extract_abstract_from_pdf.py --force

By default, publications whose index.md already has both abstract and summary skip PDF loading
and OpenAI calls (incremental). Use --force to re-extract all candidates in the batch.

Requirements:
    pip install langchain openai pypdf python-dotenv pyyaml
    
Environment:
    Create a .env file with:
    OPENAI_API_KEY=your_api_key_here
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, Optional, List
import yaml

try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage
    from dotenv import load_dotenv, find_dotenv
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("\n💡 Install dependencies with:")
    print("   pip install langchain langchain-community langchain-openai pypdf python-dotenv pyyaml")
    exit(1)


# Load environment variables from .env file
# find_dotenv() will search in current directory and parent directories
# override=True ensures .env file takes precedence over existing env vars
load_dotenv(find_dotenv(usecwd=True), override=True)


def find_publications_with_pdfs(content_dir: str, lang: str = 'en') -> List[Dict]:
    """
    Find all publication folders that contain PDF files.
    
    Args:
        content_dir: Path to content directory
        lang: Language version (en or zh)
    
    Returns:
        List of dicts with publication info and PDF path
    """
    pub_dir = Path(content_dir) / lang / 'publication'
    if not pub_dir.exists():
        print(f"❌ Publication directory not found: {pub_dir}")
        return []
    
    publications = []
    
    for pub_folder in pub_dir.iterdir():
        if not pub_folder.is_dir():
            continue
        
        index_md = pub_folder / 'index.md'
        if not index_md.exists():
            continue
        
        # Find PDF files in the folder
        pdf_files = list(pub_folder.glob('*.pdf'))
        if pdf_files:
            publications.append({
                'key': pub_folder.name,
                'folder': pub_folder,
                'index_md': index_md,
                'pdf_files': pdf_files
            })
    
    return publications


def extract_abstract_from_pdf(pdf_path: Path, llm: ChatOpenAI) -> Optional[Dict[str, str]]:
    """
    Extract abstract from PDF using LangChain and OpenAI.
    
    Args:
        pdf_path: Path to PDF file
        llm: OpenAI LLM instance
    
    Returns:
        Dict with 'abstract' and 'summary' keys, or None if extraction fails
    """
    try:
        # Load PDF
        print(f"      📄 Loading PDF: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        
        if not pages:
            print(f"      ⚠️  No content extracted from PDF")
            return None
        
        # Usually abstract is on the first 1-2 pages
        first_pages_text = "\n".join([page.page_content for page in pages[:2]])
        
        # Limit text length to avoid token limits
        max_chars = 8000
        if len(first_pages_text) > max_chars:
            first_pages_text = first_pages_text[:max_chars]
        
        print(f"      🤖 Extracting abstract with OpenAI...")
        
        # Prompt to extract abstract
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that extracts abstracts from academic papers.
            Given the first pages of a paper, extract the abstract section.
            Return ONLY the abstract text, without section headings like "Abstract" or "ABSTRACT".
            If no abstract is found, return "NOT_FOUND"."""),
            ("human", "Extract the abstract from this paper text:\n\n{text}")
        ])
        
        extract_chain = extract_prompt | llm
        abstract_response = extract_chain.invoke({"text": first_pages_text})
        abstract = abstract_response.content.strip()
        
        if abstract == "NOT_FOUND" or not abstract:
            print(f"      ⚠️  Abstract not found in PDF")
            return None
        
        print(f"      ✅ Abstract extracted ({len(abstract)} chars)")
        
        # Generate summary
        print(f"      🤖 Generating summary...")
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that creates concise summaries of academic abstracts.
            Create a 1-2 sentence summary that captures the main contribution and key finding.
            Keep it clear, concise, and informative."""),
            ("human", "Summarize this abstract:\n\n{abstract}")
        ])
        
        summary_chain = summary_prompt | llm
        summary_response = summary_chain.invoke({"abstract": abstract})
        summary = summary_response.content.strip()
        
        print(f"      ✅ Summary generated ({len(summary)} chars)")
        
        return {
            'abstract': abstract,
            'summary': summary
        }
        
    except Exception as e:
        print(f"      ❌ Error extracting from PDF: {e}")
        return None


def parse_frontmatter(content: str) -> tuple[Dict, str]:
    """
    Parse YAML frontmatter from markdown file.
    
    Args:
        content: Full markdown file content
    
    Returns:
        Tuple of (frontmatter dict, body content)
    """
    # Match YAML frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    frontmatter_text = match.group(1)
    body = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter or {}, body
    except yaml.YAMLError as e:
        print(f"      ⚠️  Error parsing YAML: {e}")
        return {}, content


def index_has_complete_abstract_summary(index_path: Path) -> bool:
    """Return True if frontmatter already has non-empty abstract and summary."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError:
        return False
    frontmatter, _ = parse_frontmatter(content)
    if not frontmatter:
        return False
    has_abstract = bool(str(frontmatter.get('abstract', '') or '').strip())
    has_summary = bool(str(frontmatter.get('summary', '') or '').strip())
    return has_abstract and has_summary


def create_minimal_index_md(pub_key: str, extracted: Dict[str, str]) -> str:
    """
    Create a minimal index.md from extracted content.
    
    Args:
        pub_key: Publication key (folder name)
        extracted: Dict with 'abstract' and 'summary'
    
    Returns:
        Complete index.md content as string
    """
    from datetime import datetime
    
    template = f"""---
title: 'Extracted from PDF - Please Update'

# Authors (please update)
authors:
  - admin

date: '{datetime.now().year}-01-01T00:00:00Z'

# Publication type (please update)
# 2 = Journal article
publication_types: ['2']

# Publication name (please update)
publication: ''
publication_short: ''

abstract: '{extracted['abstract']}'

summary: '{extracted['summary']}'

tags: []

# Display this page in the Featured widget?
featured: false

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


def update_index_md(index_path: Path, extracted: Dict[str, str], force: bool = False, 
                   override: bool = False, dry_run: bool = False) -> bool:
    """
    Update index.md with extracted abstract and summary.
    
    Args:
        index_path: Path to index.md
        extracted: Dict with 'abstract' and 'summary'
        force: Force update even if abstract exists
        override: Completely override the file with minimal template
        dry_run: Preview only, don't actually write
    
    Returns:
        True if updated, False otherwise
    """
    # If override is requested, create minimal template
    if override:
        pub_key = index_path.parent.name
        new_content = create_minimal_index_md(pub_key, extracted)
        
        if dry_run:
            print(f"      [DRY RUN] Would completely override index.md with minimal template")
            return True
        
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"      ✅ Completely overrode index.md with minimal template")
            print(f"      ⚠️  Please update: title, authors, publication name, etc.")
            return True
        except Exception as e:
            print(f"      ❌ Error writing index.md: {e}")
            return False
    
    # Read current content
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)
    
    if not frontmatter:
        print(f"      ⚠️  No frontmatter found in index.md")
        return False
    
    # Check if abstract already exists
    has_abstract = bool(frontmatter.get('abstract', '').strip())
    has_summary = bool(frontmatter.get('summary', '').strip())
    
    if has_abstract and has_summary and not force:
        print(f"      ℹ️  Abstract and summary already exist (use --force to overwrite)")
        return False
    
    # Update frontmatter
    updated = False
    if not has_abstract or force:
        frontmatter['abstract'] = extracted['abstract']
        print(f"      {'[DRY RUN] Would update' if dry_run else '✏️  Updating'} abstract")
        updated = True
    
    if not has_summary or force:
        frontmatter['summary'] = extracted['summary']
        print(f"      {'[DRY RUN] Would update' if dry_run else '✏️  Updating'} summary")
        updated = True
    
    if not updated:
        print(f"      ℹ️  No updates needed")
        return False
    
    if dry_run:
        return True
    
    # Write updated content
    try:
        new_content = "---\n" + yaml.dump(frontmatter, allow_unicode=True, sort_keys=False) + "---\n" + body
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"      ✅ Updated index.md")
        return True
        
    except Exception as e:
        print(f"      ❌ Error writing index.md: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract abstracts from PDFs and update publication pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all publications with PDFs
  python extract_abstract_from_pdf.py
  
  # Process a specific publication
  python extract_abstract_from_pdf.py --key song2023b
  
  # Preview without making changes
  python extract_abstract_from_pdf.py --dry-run
  
  # Force re-extract even if abstract exists
  python extract_abstract_from_pdf.py --force --key wang2025g
  
Environment:
  Set OPENAI_API_KEY in your environment or create a .env file:
    OPENAI_API_KEY=sk-...
        """
    )
    parser.add_argument('--key', help='Process only this publication key')
    parser.add_argument('--lang', default='en', choices=['en', 'zh'],
                       help='Language version (default: en)')
    parser.add_argument('--content-dir', default='content',
                       help='Content directory (default: content)')
    parser.add_argument('--model', default='gpt-4o-mini',
                       help='OpenAI model to use (default: gpt-4o-mini)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview only, do not write changes')
    parser.add_argument('--force', action='store_true',
                       help='Force re-extract even if abstract exists')
    parser.add_argument('--override', action='store_true',
                       help='Completely override index.md with extracted content (creates minimal template)')
    parser.add_argument('--max-publications', type=int,
                       help='Max publications still needing work to process (after incremental filter)')
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("\n💡 Set it in your shell:")
        print("   export OPENAI_API_KEY='sk-...'")
        print("\n   Or create a .env file:")
        print("   echo 'OPENAI_API_KEY=sk-...' > .env")
        return 1
    
    print("🔍 Scanning for publications with PDFs...\n")
    
    # Find publications
    publications = find_publications_with_pdfs(args.content_dir, args.lang)
    
    if not publications:
        print("❌ No publications with PDFs found")
        return 1
    
    print(f"📚 Found {len(publications)} publications with PDFs\n")
    
    # Filter by key if specified
    if args.key:
        publications = [p for p in publications if p['key'] == args.key]
        if not publications:
            print(f"❌ Publication '{args.key}' not found or has no PDF")
            return 1

    total_after_key = len(publications)
    skipped_incremental = 0

    # Incremental: skip items that already have abstract+summary (no PDF / no API) unless --force
    if args.force:
        print("🔄 --force: re-extracting from PDF for all candidates in this run\n")
    else:
        skipped_incremental = sum(
            1 for p in publications if index_has_complete_abstract_summary(p['index_md'])
        )
        if skipped_incremental:
            print(
                f"⏭️  {skipped_incremental} publication(s) already have abstract+summary — "
                f"skipping (incremental, no API)\n"
            )
        publications = [
            p for p in publications
            if not index_has_complete_abstract_summary(p['index_md'])
        ]
        if not publications:
            print("✅ Nothing to process — all selected publications already have abstract and summary.")
            print("   Use --force to re-extract from PDFs.")
            return 0

    publications.sort(key=lambda p: p['key'])

    # Limit batch size (only applies to publications still needing work)
    if args.max_publications:
        total_need = len(publications)
        publications = publications[: args.max_publications]
        if total_need > len(publications):
            print(
                f"📌 Processing {len(publications)} of {total_need} publication(s) "
                f"needing work (--max-publications)\n"
            )

    # Initialize LLM
    print(f"🤖 Initializing OpenAI ({args.model})...\n")
    try:
        llm = ChatOpenAI(
            model=args.model,
            temperature=0,
            openai_api_key=api_key
        )
    except Exception as e:
        print(f"❌ Error initializing OpenAI: {e}")
        return 1
    
    # Process publications
    processed = 0
    updated = 0
    skipped = 0
    errors = 0
    
    for i, pub in enumerate(publications, 1):
        print(f"[{i}/{len(publications)}] Processing: {pub['key']}")
        
        # Use the first PDF if multiple exist
        pdf_path = pub['pdf_files'][0]
        
        # Extract abstract from PDF
        extracted = extract_abstract_from_pdf(pdf_path, llm)
        
        if not extracted:
            errors += 1
            print()
            continue
        
        # Update index.md
        if update_index_md(pub['index_md'], extracted, args.force, args.override, args.dry_run):
            updated += 1
        else:
            skipped += 1
        
        processed += 1
        print()
    
    # Print summary
    print("=" * 80)
    print("📊 Summary:")
    print(f"   Publications (after --key):      {total_after_key}")
    print(f"   Skipped incremental (no API):    {skipped_incremental}")
    print(f"   In this extraction batch:        {len(publications)}")
    print(f"   Successfully processed:          {processed}")
    print(f"   Updated index.md:                {updated}")
    print(f"   Skipped at write (no change):    {skipped}")
    print(f"   Errors:                          {errors}")
    
    if args.dry_run:
        print("\n💡 This was a dry run. Remove --dry-run to actually update files.")
    
    if updated > 0 and not args.dry_run:
        print("\n✅ Files updated successfully!")
        print("💡 Review the changes and commit if satisfied:")
        print(f"   git diff content/{args.lang}/publication/")
    
    return 0


if __name__ == '__main__':
    exit(main())

