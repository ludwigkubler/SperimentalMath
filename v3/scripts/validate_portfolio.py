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
9. (with --check-urls) Each reference must have AT LEAST ONE valid identifier:
     - arxiv_id: validated via HEAD on arxiv.org
     - doi: validated via CrossRef API (bypasses publisher 403 blocks)
     - isbn: accepted without online check (static identifier)

Usage:
  python3 validate_portfolio.py /path/to/v3/problems
  python3 validate_portfolio.py /path/to/v3/problems --check-urls

Exit codes:
  0 — all pass
  1 — one or more files / urls failed
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

REQUIRED_TOP_LEVEL = [
    "problem_id", "title", "field", "status", "curated_by", "last_reviewed",
]
VALID_FIELDS = {
    "circuit_lb", "communication_complexity", "proof_complexity", "sat_hardness",
    "barrier_theory", "fine_grained", "algebraic_complexity", "derandomization",
}
VALID_STATUS = {"active", "frozen", "resolved", "abandoned"}
MAX_AGE_DAYS = 90
FOLKLORE_KEYS = {"folklore_3sum", "trivial_upper"}

_USER_AGENT = "v3-portfolio-validator/2.0"


# ── HTTP checks ────────────────────────────────────────────────────────────────

def check_doi_via_crossref(doi: str, timeout: int = 12) -> tuple[bool, str]:
    """Validate DOI via CrossRef API. Returns (ok, detail).

    CrossRef serves DOI metadata without redirecting to the publisher,
    so we don't hit 403 blocks from ACM/SIAM/Wiley/etc.
    """
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": _USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 300:
                return True, f"crossref {resp.status}"
            return False, f"crossref HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "DOI not in CrossRef"
        return False, f"crossref HTTP {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_arxiv(aid: str, timeout: int = 12) -> tuple[bool, str]:
    """Validate arXiv ID via arxiv.org HEAD."""
    aid_clean = aid.replace("arxiv:", "").replace("arXiv:", "").strip()
    url = f"https://arxiv.org/abs/{aid_clean}"
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": _USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, f"arxiv {resp.status}"
            return False, f"arxiv HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"arxiv HTTP {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_reference(r: dict) -> tuple[bool, list[str]]:
    """A reference is valid iff at least ONE identifier resolves OR
    verification_status is explicitly 'pre_crossref' (curator vouches for
    a paper that predates electronic indexing).

    Returns (any_ok, list of per-identifier strings).
    """
    key = r.get("key", "?")
    if key in FOLKLORE_KEYS:
        return True, ["folklore-exempt"]

    notes: list[str] = []
    any_ok = False

    arxiv = (r.get("arxiv_id") or "").strip()
    if arxiv:
        ok, detail = check_arxiv(arxiv)
        notes.append(f"arxiv:{arxiv} {'OK' if ok else 'FAIL'} ({detail})")
        any_ok = any_ok or ok

    doi = (r.get("doi") or "").strip()
    if doi:
        ok, detail = check_doi_via_crossref(doi)
        notes.append(f"doi:{doi} {'OK' if ok else 'FAIL'} ({detail})")
        any_ok = any_ok or ok

    isbn = (r.get("isbn") or "").strip()
    if isbn:
        notes.append(f"isbn:{isbn} OK (accepted-without-online-check)")
        any_ok = True

    vstatus = (r.get("verification_status") or "").strip()
    if vstatus == "pre_crossref":
        notes.append("verification_status=pre_crossref OK (curator-vouched)")
        any_ok = True

    if not notes:
        notes.append("no identifiers")

    return any_ok, notes


# ── Schema validation ──────────────────────────────────────────────────────────

def validate_schema(path: Path, data: dict) -> list[str]:
    fails: list[str] = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            fails.append(f"missing top-level field: {field}")

    if data.get("field") not in VALID_FIELDS:
        fails.append(
            f"invalid field: {data.get('field')!r}; expected one of {sorted(VALID_FIELDS)}"
        )

    if data.get("status") not in VALID_STATUS:
        fails.append(
            f"invalid status: {data.get('status')!r}; expected one of {sorted(VALID_STATUS)}"
        )

    pid = data.get("problem_id", "")
    if pid != path.stem:
        fails.append(f"problem_id {pid!r} != filename stem {path.stem!r}")

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
                fails.append(
                    f"[statement].lean_file {stmt['lean_file']!r} not next to TOML"
                )

    sig = data.get("significance_to_pvsnp", {})
    if not isinstance(sig, dict) or not sig.get("text"):
        fails.append("[significance_to_pvsnp].text missing or empty")

    kb = data.get("known_bounds", [])
    if not kb:
        fails.append("at least one [[known_bounds]] required")
    cr = data.get("canonical_references", [])
    if len(cr) < 3:
        fails.append(f"at least 3 [[canonical_references]] required (got {len(cr)})")
    oq = data.get("open_subquestions", [])
    if not oq:
        fails.append("at least one [[open_subquestions]] required")

    ref_keys = {r.get("key") for r in cr if r.get("key")}
    for b in kb:
        rk = b.get("reference_key")
        if rk and rk not in ref_keys:
            fails.append(
                f"known_bounds.reference_key {rk!r} not in canonical_references"
            )
    for br in data.get("known_barriers", []):
        rk = br.get("reference_key")
        if rk and rk not in ref_keys:
            fails.append(
                f"known_barriers.reference_key {rk!r} not in canonical_references"
            )

    lr = data.get("last_reviewed")
    if isinstance(lr, date):
        age = (date.today() - lr).days
        if age > MAX_AGE_DAYS:
            fails.append(f"last_reviewed is {age} days old (max {MAX_AGE_DAYS})")
    elif lr is not None:
        fails.append(f"last_reviewed not a date: {type(lr).__name__}")

    # Each canonical_reference must have at least one identifier OR a
    # 'pre_crossref' verification_status. Validator of URLs runs
    # separately; this only enforces schema presence.
    for r in cr:
        if r.get("key") in FOLKLORE_KEYS:
            continue
        has_id = bool(r.get("arxiv_id") or r.get("doi") or r.get("isbn"))
        is_pre_crossref = r.get("verification_status") == "pre_crossref"
        if not (has_id or is_pre_crossref):
            fails.append(
                f"canonical_reference {r.get('key')!r} has none of "
                f"arxiv_id, doi, isbn, verification_status=pre_crossref"
            )

    return fails


# ── Driver ────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio_dir", type=Path)
    parser.add_argument(
        "--check-urls", action="store_true",
        help="HTTP-validate every identifier (slow ~30s/file)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show every identifier check, not just failures",
    )
    args = parser.parse_args()

    if not args.portfolio_dir.is_dir():
        print(f"ERROR: not a directory: {args.portfolio_dir}", file=sys.stderr)
        return 2

    toml_files = sorted(
        p for p in args.portfolio_dir.glob("*.toml")
        if not p.name.startswith("_")
    )
    if not toml_files:
        print(f"ERROR: no TOML files in {args.portfolio_dir}", file=sys.stderr)
        return 2

    schema_pass = schema_fail = ref_pass = ref_fail = 0
    fail_summary: list[str] = []

    print(f"Validating {len(toml_files)} TOML files in {args.portfolio_dir}")
    print()

    for path in toml_files:
        print(f"== {path.name} ==")
        try:
            with path.open("rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            print(f"  FAIL: TOML parse error: {e}")
            schema_fail += 1
            fail_summary.append(f"{path.name}: parse error")
            continue

        sfails = validate_schema(path, data)
        if sfails:
            for msg in sfails:
                print(f"  FAIL: {msg}")
                fail_summary.append(f"{path.name}: {msg}")
            schema_fail += 1
        else:
            print("  OK: schema")
            schema_pass += 1

        if args.check_urls:
            print("  Checking references...")
            for r in data.get("canonical_references", []):
                key = r.get("key", "?")
                ok, notes = check_reference(r)
                if ok:
                    ref_pass += 1
                    if args.verbose:
                        for n in notes:
                            print(f"    OK   {key:35s}  {n}")
                else:
                    ref_fail += 1
                    print(f"    FAIL {key:35s}")
                    for n in notes:
                        print(f"          {n}")
                    fail_summary.append(f"{path.name}:{key}")
        print()

    print("=" * 60)
    print(f"Schema:     {schema_pass} pass / {schema_fail} fail")
    if args.check_urls:
        print(f"References: {ref_pass} pass / {ref_fail} fail "
              f"(rule: at least one identifier per reference must resolve)")

    if fail_summary:
        print()
        print("FAILURE SUMMARY:")
        for f in fail_summary:
            print(f"  - {f}")

    return 0 if (schema_fail == 0 and ref_fail == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
