# 01 - Code Inventory (sub-agent 1/6)

## Executive summary

Server `ludo@sec` carries a **17,437-file source corpus totalling 2.91 M LOC**, dominated by the Lean ecosystem (8,924 files / 2.19 M LOC = 75 % of all LOC) which lives almost entirely under `~/kissat/pvnp_lab/`. Python is the second pillar (6,348 files / 601 k LOC), spread across the SEC stacks and `~/Scrivania/future/`. The `~/kissat/pvnp_lab` tree alone accounts for ~77 % of total LOC, and the 20 largest files are **all** Lean (mostly mathlib vendored packages under `.lake/packages/`). The two SEC roots (`~/SEC` and `~/Scrivania/SEC`, both ~12 GB on disk) look like the same project twice: 165 of the 186 relative paths in `~/SEC` also exist in `~/Scrivania/SEC`, but `~/Scrivania/SEC` is much larger (2,894 files vs 186), so `~/SEC` appears to be a stale subset / older snapshot. No `.ipynb` notebooks were found in the corpus, and no extension-less source file carries a shebang — the only extension-less files are 9 Dockerfiles vendored inside mathlib `.lake/packages/`.

---

## 1. Total source files

`wc -l /tmp/audit_1778671816/all_sources.txt` -> **17,437** (matches the input count).

Total LOC across the corpus: **2,913,740**.

## 2. Top 25 extensions

| ext           | count | total LOC | avg LOC |
|---------------|------:|----------:|--------:|
| lean          | 8,924 | 2,194,960 |  246.0  |
| py            | 6,348 |   601,220 |   94.7  |
| ts            |   501 |    20,516 |   41.0  |
| rs            |   453 |    21,289 |   47.0  |
| go            |   243 |    12,948 |   53.3  |
| js            |   158 |     4,369 |   27.7  |
| java          |   139 |     5,106 |   36.7  |
| kt            |   110 |     2,779 |   25.3  |
| php           |    92 |     3,436 |   37.3  |
| cpp           |    75 |     2,802 |   37.4  |
| tex           |    70 |     5,703 |   81.5  |
| sh            |    67 |     4,609 |   68.8  |
| yml           |    62 |     8,320 |  134.2  |
| toml          |    45 |       611 |   13.6  |
| sql           |    35 |     1,358 |   38.8  |
| yaml          |    27 |     8,314 |  307.9  |
| h             |    27 |       672 |   24.9  |
| html          |    23 |     6,708 |  291.7  |
| tsx           |    17 |     1,733 |  101.9  |
| hpp           |     9 |       272 |   30.2  |
| (Dockerfile)  |     9 |       400 |   44.4  |
| bib           |     3 |     5,615 | 1,871.7 |

Notes: the corpus has 22 distinct extensions overall — extensions below the table (e.g. only 3 `.bib`) are listed in row form above. The `.bib` average is inflated by a single 5,374-LOC mathlib `references.bib`.

## 3. Files by system root

| system                      |  files |       LOC | top-3 extensions          |
|-----------------------------|-------:|----------:|---------------------------|
| ~/kissat/pvnp_lab           |  8,872 | 2,236,995 | lean (8,639), py (80), yml (61) |
| ~/Scrivania/future          |  5,300 |   226,126 | py (3,115), ts (488), rs (448) |
| ~/Scrivania/SEC             |  2,894 |   399,771 | py (2,838), lean (20), sh (12) |
| ~/SEC                       |    186 |    40,131 | py (156), html (20), yaml (5) |
| ~/projects                  |    157 |     6,620 | py (132), ts (11), rs (5) |
| ~/tools                     |     28 |     4,097 | py (27), sh (1)           |
| ~/Scrivania/pubblicazioni   |      0 |         0 | (no source files)         |

Every file in `all_sources.txt` bucketed to one of the seven systems — no "other" residue. (The bucket figures for the two SEC roots differ slightly from naive substring counts because the regex is anchored at the system root, e.g. `~/SEC/scripts/tools/...` belongs to `~/SEC`, not `~/tools`.)

## 4. Largest 20 files by LOC

| LOC  | path |
|-----:|------|
| 7,468 | /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/Mathlib.lean |
| 5,374 | /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/docs/references.bib |
| 4,219 | /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/docs/1000.yaml |
| 2,017 | /home/ludo/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py |
| 2,017 | /home/ludo/Scrivania/SEC/src/research/pvsnp_explorer.py |
| 1,628 | /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/Cli/Cli/Basic.lean |
| 1,548 | .../mathlib/Mathlib/CategoryTheory/Limits/Shapes/Pullback/CommSq.lean |
| 1,525 | .../mathlib/Mathlib/LinearAlgebra/TensorProduct/Basic.lean |
| 1,521 | .../mathlib/Mathlib/Analysis/Calculus/ContDiff/Basic.lean |
| 1,517 | .../mathlib/Mathlib/Geometry/Manifold/ChartedSpace.lean |
| 1,515 | .../mathlib/Mathlib/GroupTheory/MonoidLocalization/Basic.lean |
| 1,511 | .../mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean |
| 1,494 | .../mathlib/Mathlib/Topology/Instances/ENNReal/Lemmas.lean |
| 1,482 | /home/ludo/Scrivania/SEC/src/entity/living/autonomous.py |
| 1,476 | .../mathlib/Mathlib/Algebra/Quaternion.lean |
| 1,472 | .../mathlib/Mathlib/Tactic/CC/Addition.lean |
| 1,463 | .../mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean |
| 1,463 | .../mathlib/Mathlib/CategoryTheory/Limits/Shapes/BinaryProducts.lean |
| 1,462 | .../mathlib/Mathlib/Algebra/Order/ToIntervalMod.lean |
| 1,455 | .../mathlib/Mathlib/Algebra/Order/Monoid/Unbundled/Basic.lean |

All 20 paths sit under `.lake/packages/mathlib/...` except `pvsnp_explorer.py` (duplicated under `~/kissat/pvnp_lab/system_v2/` and `~/Scrivania/SEC/src/research/` with identical 2,017 LOC) and `autonomous.py` (the SEC autonomous entity loop). Lean files dominate because the mathlib stdlib is vendored verbatim in the `.lake` package cache — downstream agents should treat anything under `.lake/packages/` as third-party, not project code.

## 5. System sizes summary

LOC per system (sorted):

- **~/kissat/pvnp_lab** : 2,236,995 LOC across 8,872 files (~77 % of total LOC)
- **~/Scrivania/SEC**   :   399,771 LOC across 2,894 files
- **~/Scrivania/future**:   226,126 LOC across 5,300 files
- **~/SEC**             :    40,131 LOC across   186 files
- **~/projects**        :     6,620 LOC across   157 files
- **~/tools**           :     4,097 LOC across    28 files
- **~/Scrivania/pubblicazioni**: 0 source files

### SEC duplicate check (both directories reported as ~12 GB)

|                        | ~/SEC        | ~/Scrivania/SEC |
|------------------------|-------------:|----------------:|
| source files           | 186          | 2,894           |
| total LOC              | 40,131       | 399,771         |
| top extension          | py (156)     | py (2,838)      |

**Overlap test**: of the 186 relative paths under `~/SEC`, **165 (89 %)** also exist with the identical relative path under `~/Scrivania/SEC`. Conclusion: `~/SEC` looks like a **stale partial mirror** (about 6 % the size of the live tree at `~/Scrivania/SEC`). The 12 GB-each disk figure must therefore be driven by **non-source assets** (the audit corpus only counts code; `~/SEC/data/content_factory/blog/...` etc. HTML/blob fields are presumably the bulk). This is consistent with the project memory note that "SEC solo su ~/Scrivania/SEC/" — `~/SEC` should be considered an outdated snapshot.

Confirmed duplicated source file across the two trees:
- `pvsnp_explorer.py` (2,017 LOC, identical LOC count in both `~/kissat/pvnp_lab/system_v2/src/` and `~/Scrivania/SEC/src/research/`).

## 6. Files-without-extension with a shebang

**0** files in the audit corpus.

The 9 "extension-less" files in `all_sources.txt` are all `Dockerfile` (filename has no `.`), none of which carry a `#!` shebang:

- /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/.docker/gitpod/Dockerfile
- /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/.docker/lean/Dockerfile
- /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/.docker/gitpod-blueprint/Dockerfile
- /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/mathlib/.devcontainer/Dockerfile
- /home/ludo/kissat/pvnp_lab/lab_c001/lean/TseitinTw/.lake/packages/batteries/.docker/gitpod/Dockerfile
- (plus 4 more vendored Dockerfiles under `.lake/packages/`)

(A wider probe outside `all_sources.txt` found 4 extension-less shebanged files — Lean toolchain shell wrappers like `~/.elan/toolchains/.../bin/leanmake` — but these are not in the audit corpus and downstream agents can ignore them.)

## 7. Notebooks (.ipynb)

**0** `.ipynb` files in the corpus. (Note for downstream agents: had any been present, their code is embedded JSON cells and would not be picked up by extension-based static analysis without a preprocessing step.)

## 8. Top-level caveats for downstream agents

- **Lean stdlib bloat**: 8,639 of the 8,872 files under `~/kissat/pvnp_lab` are `.lean` and a large fraction live in `.lake/packages/mathlib/...` or `.lake/packages/batteries/...`. These should be excluded from any "project-authored code" metrics — they are vendored third-party.
- **SEC mirroring**: treat `~/SEC` as a likely-stale duplicate of `~/Scrivania/SEC` (per user memory: "SEC solo su ~/Scrivania/SEC"). If running per-file analysis on the SEC stack, prefer `~/Scrivania/SEC`.
- **Python is the real custom surface area**: 6,348 .py files / 601 k LOC, mostly under `~/Scrivania/future` (3,115 .py) and `~/Scrivania/SEC` (2,838 .py). These are the files most likely to contain hand-written research code.
- **No notebooks** simplifies the remaining audits — every file in the corpus is plain text source.

