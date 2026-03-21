#!/usr/bin/env python3
"""Fetch h-index and citation count from Google Scholar and write to _data/scholar.yml."""

import sys
from scholarly import scholarly

SCHOLAR_ID = "1cdNGL4AAAAJ"
OUTPUT_FILE = "_data/scholar.yml"

def fetch():
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["indices", "citedby"])
    citations = author.get("citedby", "—")
    hindex = author.get("hindex", "—")
    return citations, hindex

def main():
    try:
        citations, hindex = fetch()
        with open(OUTPUT_FILE, "w") as f:
            f.write("# Auto-updated by .github/workflows/update_scholar.yml\n")
            f.write(f"citations: \"{citations}\"\n")
            f.write(f"hindex: \"{hindex}\"\n")
        print(f"Updated: citations={citations}, h-index={hindex}")
    except Exception as e:
        print(f"Error fetching scholar data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
