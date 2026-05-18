#!/usr/bin/env python3
"""Portfolio validator — v3 Phase 1 brought forward.

Validates the 6 Problem TOML files for:
1. TOML parse-ability
2. Required top-level fields (problem_id, title, field, status, …)
3. Required sub-tables ([statement], [significance_to_pvsnp])
4. Required array-of-tables (known_bounds, canonical_references, open_subquestions)
5. Reference-key integrity: every reference_key in known_bounds/known_barriers
   must exist in canonical_references.
6. Filename matches problem_id.
7. Companion .lean file exists.
8. last_reviewed is within 90 days.
9. (optional, with --check-urls) DOI and arXiv URLs resolve (HTTP HEAD).

Usage:
  python3 validate_portfolio.py /path/to/v3/problems        # local validation
  python3 validate_portfolio.py /path/to/v3/problems --check-urls  # + HTTP

Exit codes:
  0 — all pass
  1 — one or more files failed (per-file detail on stdout)
  2 — usage error
"""

from __future__ import annotations

import argparse
import sys
import tomllib
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

REQUIRED_TOP_LEVEL = ["problem_id", "title", "field", "status", "curated_by", "last_reviewed"]
VALID_FIELDS = {
    "circuit_lb", "communication_complexity", "proof_complexity", "sat_hardness",
    "barrier_theory", "fine_grained", "algebraic_complexity", "derandomization",
}
VALID_STATUS = {"active", "frozen", "resolved", "abandoned"}
MAX_AGE_DAYS = 90


def fail(msg: str) -> None:
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    print(f"  WARN: {msg}")


def validate_schema(path: Path, data: dict) -> list[str]:
    """Returns list of failure messages. Empty list = pass."""
    fails: list[str] = []

    # 1. Top-level required
    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            fails.append(f"missing top-level field: {field}")

    # 2. Field enum
    if data.get("field") not in VALID_FIELDS:
        fails.append(f"invalid field: {data.get('field')!r}; expected one of {sorted(VALID_FIELDS)}")

    # 3. Status enum
    if data.get("status") not in VALID_STATUS:
        fails.append(f"invalid status: {data.get('status')!r}; expected one of {sorted(VALID_STATUS)}")

    # 4. problem_id matches filename
    pid = data.get("problem_id", "")
    if pid != path.stem:
        fails.append(f"problem_id {pid!r} != filename stem {path.stem!r}")

    # 5. Required sub-tables
    stmt = data.get("statement", {})
    if not isinstance(stmt, dict):
        fails.append("[statement] missing or not a table")
    else:
        if not stmt.get("markdown"):
            fails.append("[statement].markdown missing or empty")
        if not stmt.get("lean_file"):
            fails.append("[statement].lean_file missing")
        else:
            lean_path = path.parent / stmt["lean_file"]
            if not lean_path.exists():
                fails.append(f"[statement].lean_file {stmt['lean_file']!r} does not exist next to TOML")

    sig = data.get("significance_to_pvsnp", {})
    if not isinstance(sig, dict) or not sig.get("text"):
        fails.append("[significance_to_pvsnp].text missing or empty")

    # 6. Required arrays
    kb = data.get("known_bounds", [])
    if not kb:
        fails.append("at least one [[known_bounds]] required")
    cr = data.get("canonical_references", [])
    if len(cr) < 3:
        fails.append(f"at least 3 [[canonical_references]] required (got {len(cr)})")
    oq = data.get("open_subquestions", [])
    if not oq:
        fails.append("at least one [[open_subquestions]] required")

    # 7. Reference-key integrity
    ref_keys = {r.get("key") for r in cr if r.get("key")}
    for b in kb:
        rk = b.get("reference_key")
        if rk and rk not in ref_keys:
            fails.append(f"known_bounds.reference_key {rk!r} not in canonical_references")
    for br in data.get("known_barriers", []):
        rk = br.get("reference_key")
        if rk and rk not in ref_keys:
            fails.append(f"known_barriers.reference_key {rk!r} not in canonical_references")

    # 8. last_reviewed freshness
    lr = data.get("last_reviewed")
    if isinstance(lr, date):
        age = (date.today() - lr).days
        if age > MAX_AGE_DAYS:
            fails.append(f"last_reviewed is {age} days old (max {MAX_AGE_DAYS})")
    elif lr is not None:
        fails.append(f"last_reviewed not a date: {type(lr).__name__}")

    # 9. Each [[canonical_references]] must have arxiv_id OR doi OR isbn
    for r in cr:
        if r.get("key") in {"folklore_3sum", "trivial_upper"}:
            # explicitly folklore — exempt
            continue
        if not (r.get("arxiv_id") or r.get("doi") or r.get("isbn")):
            fails.append(
                f"canonical_reference {r.get('key')!r} has none of arxiv_id, doi, isbn"
            )

    return fails


def check_url(url: str, timeout: int = 10) -> tuple[bool, str]:
    """HTTP HEAD. Returns (ok, detail)."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "v3-portfolio-validator/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.status
            if 200 <= code < 400:
                return True, f"{code}"
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as e:
        # Some publishers (Springer, etc.) return 403 on HEAD but 200 on GET
        if e.code == 403:
            try:
                req2 = urllib.request.Request(url, method="GET",
                    headers={"User-Agent": "v3-portfolio-validator/1.0"})
                with urllib.request.urlopen(req2, timeout=timeout) as resp:
                    if 200 <= resp.status < 400:
                        return True, f"GET {resp.status} (HEAD blocked)"
            except Exception as e2:
                return False, f"HEAD 403, GET failed: {type(e2).__name__}"
        return False, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URLError: {e.reason}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_citations(data: dict) -> list[tuple[str, str, bool, str]]:
    """For each canonical_reference, build URLs and HEAD-check.
    Returns list of (key, url, ok, detail)."""
    results = []
    for r in data.get("canonical_references", []):
        key = r.get("key", "?")
        arxiv = r.get("arxiv_id", "").strip()
        doi = r.get("doi", "").strip()
        urls = []
        if arxiv:
            # Strip any "arxiv:" or "arXiv:" prefix
            arxiv_clean = arxiv.replace("arxiv:", "").replace("arXiv:", "").strip()
            if arxiv_clean:
                urls.append(("arxiv", f"https://arxiv.org/abs/{arxiv_clean}"))
        if doi:
            urls.append(("doi", f"https://doi.org/{doi}"))
        if not urls:
            if key not in {"folklore_3sum", "trivial_upper"}:
                results.append((key, "(no url)", False, "no doi or arxiv_id"))
            continue
        for kind, url in urls:
            ok, detail = check_url(url)
            results.append((key, url, ok, detail))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio_dir", type=Path)
    parser.add_argument("--check-urls", action="store_true",
                        help="HTTP-validate every doi/arxiv (slow, may rate-limit)")
    args = parser.parse_args()

    if not args.portfolio_dir.is_dir():
        print(f"ERROR: not a directory: {args.portfolio_dir}", file=sys.stderr)
        return 2

    toml_files = sorted(p for p in args.portfolio_dir.glob("*.toml") if not p.name.startswith("_"))
    if not toml_files:
        print(f"ERROR: no TOML files in {args.portfolio_dir}", file=sys.stderr)
        return 2

    total_pass = 0
    total_fail = 0
    url_pass = 0
    url_fail = 0
    url_failures = []

    print(f"Validating {len(toml_files)} TOML files in {args.portfolio_dir}")
    print()

    for path in toml_files:
        print(f"== {path.name} ==")
        try:
            with path.open("rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            print(f"  FAIL: TOML parse error: {e}")
            total_fail += 1
            continue

        schema_fails = validate_schema(path, data)
        if schema_fails:
            for msg in schema_fails:
                fail(msg)
            total_fail += 1
        else:
            print("  OK: schema")
            total_pass += 1

        if args.check_urls:
            print("  Checking URLs...")
            url_results = check_citations(data)
            for key, url, ok, detail in url_results:
                if ok:
                    url_pass += 1
                else:
                    url_fail += 1
                    url_failures.append((path.name, key, url, detail))
                    print(f"    FAIL  {key:30s}  {url}  →  {detail}")
            if not any(not ok for _, _, ok, _ in url_results):
                print(f"  OK: {len(url_results)} URLs verified")

        print()

    print("=" * 60)
    print(f"Schema:  {total_pass} pass / {total_fail} fail")
    if args.check_urls:
        print(f"URLs:    {url_pass} pass / {url_fail} fail")
        if url_failures:
            print()
            print("URL FAILURES:")
            for fname, key, url, detail in url_failures:
                print(f"  {fname}:{key:30s} {detail}  ({url})")

    return 0 if (total_fail == 0 and url_fail == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
