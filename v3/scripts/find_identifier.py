#!/usr/bin/env python3
"""Search CrossRef and arXiv for a paper by title + authors.
Returns candidate DOIs / arXiv IDs ranked by relevance.

Usage:
  python3 find_identifier.py "title" --author "name" [--year YYYY]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

_UA = "v3-portfolio-validator/2.0"


def search_crossref(title: str, author: str = "", year: int | None = None, n: int = 5):
    q = f"https://api.crossref.org/works?query.title={urllib.parse.quote(title)}"
    if author:
        q += f"&query.author={urllib.parse.quote(author)}"
    q += f"&rows={n}"
    req = urllib.request.Request(q, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    items = data.get("message", {}).get("items", [])
    results = []
    for it in items:
        results.append({
            "doi": it.get("DOI", ""),
            "title": (it.get("title") or [""])[0][:80],
            "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "venue": it.get("container-title", [""])[0][:60],
            "authors": ", ".join(
                f"{a.get('given','')} {a.get('family','')}".strip()
                for a in (it.get("author") or [])[:3]
            )[:80],
        })
    return results


def search_arxiv(title: str, n: int = 5):
    q = (f"http://export.arxiv.org/api/query?search_query=ti:%22"
         f"{urllib.parse.quote(title)}%22&max_results={n}")
    req = urllib.request.Request(q, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8", "replace")
    # Crude XML parsing: pull <entry>...</entry> blocks
    results = []
    parts = body.split("<entry>")
    for part in parts[1:]:
        block = part.split("</entry>")[0]
        # Pull arxiv id from <id> URL
        if "<id>" in block:
            url = block.split("<id>")[1].split("</id>")[0]
            aid = url.rsplit("/abs/", 1)[-1].rsplit("v", 1)[0]
        else:
            aid = ""
        if "<title>" in block:
            t = " ".join(block.split("<title>")[1].split("</title>")[0].split())[:80]
        else:
            t = ""
        if "<published>" in block:
            y = block.split("<published>")[1][:4]
        else:
            y = ""
        results.append({"arxiv_id": aid, "title": t, "year": y})
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("title")
    p.add_argument("--author", default="")
    p.add_argument("--year", type=int, default=None)
    p.add_argument("--n", type=int, default=5)
    args = p.parse_args()

    print(f"Searching: {args.title!r}")
    if args.author:
        print(f"  with author: {args.author!r}")
    if args.year:
        print(f"  in year: {args.year}")
    print()

    print("=== CrossRef ===")
    try:
        for r in search_crossref(args.title, args.author, args.year, args.n):
            year_match = ""
            if args.year and r["year"] and abs(int(r["year"]) - args.year) <= 1:
                year_match = " [YEAR MATCH]"
            print(f"  DOI: {r['doi']}")
            print(f"    title:   {r['title']}")
            print(f"    year:    {r['year']}{year_match}")
            print(f"    venue:   {r['venue']}")
            print(f"    authors: {r['authors']}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")
    print()
    print("=== arXiv ===")
    try:
        for r in search_arxiv(args.title, args.n):
            print(f"  arXiv: {r['arxiv_id']}  ({r['year']})  {r['title']}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
