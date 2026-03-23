#!/usr/bin/env python3
"""Fetch h-index and citation count from Google Scholar and write to _data/scholar.yml."""

import sys
from scholarly import scholarly, ProxyGenerator

SCHOLAR_ID = "1cdNGL4AAAAJ"
OUTPUT_FILE = "_data/scholar.yml"

def fetch():
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["indices", "citedby"])
    citations = author.get("citedby", "—")
    hindex = author.get("hindex", "—")
    return citations, hindex

def fetch_with_proxy():
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)
    return fetch()

def main():
    # Try direct first, then via free proxy
    for attempt, fn in enumerate([fetch, fetch_with_proxy], start=1):
        try:
            citations, hindex = fn()
            with open(OUTPUT_FILE, "w") as f:
                f.write("# Auto-updated by .github/workflows/update_scholar.yml\n")
                f.write(f"citations: \"{citations}\"\n")
                f.write(f"hindex: \"{hindex}\"\n")
            print(f"Updated (attempt {attempt}): citations={citations}, h-index={hindex}")
            return
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}", file=sys.stderr)

    # Both attempts failed — keep existing file, don't break the workflow
    print("Could not fetch Scholar data. Keeping existing _data/scholar.yml.", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
