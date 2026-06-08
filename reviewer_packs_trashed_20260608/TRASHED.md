# TRASHED 2026-06-08 — Q3 reviewer_packs disposal

**Date**: 2026-06-08
**Author**: Ludovico Kubler (HARDY harness, Q3 reviewer_packs sub-agent)
**Eval report**: `HARDY/staging/q3_reviewer_packs_eval/EVAL_REPORT.md`

## What is this directory?

This is the former `reviewer_packs/` directory of SperimentalMath, renamed
on 2026-06-08 after a HARDY Q3 audit established that the corpus is
predominantly low-quality generator artefact rather than substantive
mathematical work. The full directory is preserved here (git history
intact) for one week as a safety net; it will then be removed.

A safety-net tarball is also archived at:
`SEC/research/archive/reviewer_packs_archive_20260608.tar.gz`.

## Rationale

| Quantity | Value |
|---|---|
| Total packs at audit time | 3,839 |
| Final-verdict `INCONCLUSIVE` | 3,819 / 3,839 (99.48%) |
| Final-verdict `SUPPORTED` / `FALSIFIED` | 0 / 0 |
| Sampled packs | 11 (3 oldest-in-window, 3 middle, 3 recent, 1 smallest, 1 largest) |
| Mean quality score (n=11, 0-15 rubric) | **4.45 / 15** |
| Mean quality excluding outlier `999ba4b45fab` (n=10) | 3.4 / 15 |
| Category: TRASH (score 0-6) | 10 / 11 (90.9%) |
| Category: KEEP-WORTHY (score 12-15) | 1 / 11 (9.1%) — pack `999ba4b45fab` |
| HARDY predicate-gate verdict | **BLOCK** on 11 / 11 |
| Dominant gate failures | `named_quantity_has_definition`, `falsifier_in_abstract` |

## Why this is not just a "low score" event

The population-wide INCONCLUSIVE rate of 99.48% **independently corroborates**
the per-pack scoring: the generator is not just emitting low-quality
statements, it is emitting statements whose test harnesses **cannot run**
(crash with `ZeroDivisionError`, `IndexError`, syntax errors, or 240s
timeouts before producing any TRIAL: lines). The named quantities (e.g.
"minimal Hodge diamond width", "minimal tropical symmetry length",
"minimal local index of braided monoid automorphisms") are never defined
formally — they are combinatorial-sounding placeholders. Citations
typically come from Semantic Scholar hits that are topic-adjacent but
substantively irrelevant.

Reading these packs as "open mathematical conjectures" without context
would mislead any downstream consumer (human or RAG) about
SperimentalMath's actual research output rate.

## What was rescued

Likely-substantive packs (size >= 18 KB AND containing at least one
substantive citation token: Goemans, Lasserre, Delorme, Saff, Schoenebeck,
Khot, Barak-Steurer, Razborov, Rossman, Karchmer, Fekete, Goldreich,
Williamson) were copied into `reviewer_packs_KEEP_20260608/` for human
review before this trash operation.

The Q3 sample's KEEP-WORTHY pack `999ba4b45fab.md` (Fekete capacity bounds
Max-Cut SoS-2 gap, 22.3 KB) is exactly the kind of work the rescue filter
is meant to catch.

## What was fixed in the generator

See `HARDY/staging/q3_reviewer_packs_eval/RATE_LIMIT.diff` for the
companion rate-limit patch (cuts artefact emission from ~138/day to
<=5/day, a 25x leakage reduction) pending the deeper fixes F1-F4
documented in EVAL_REPORT.md section 9 step 4 (constructive-definition
prompt, ADJACENT_OK novelty tightening, FALSIFIED-on-zero-support fix,
no-data-INCONCLUSIVE rejection).

## Restoration

To restore the corpus from the safety-net tarball:

```bash
cd /home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath
tar xzf /home/ludo/Scrivania/SEC/research/archive/reviewer_packs_archive_20260608.tar.gz
```

## Sentinel

`Q3_TRASHED:4.45:90.9pct:BLOCK_11of11:20260608`
