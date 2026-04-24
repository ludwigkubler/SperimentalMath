# SperimentalMath — auto-generated mathematics (verified and refuted)

**Author & copyright**: Ludovico Kubler, © 2026

This repository is the **output sink** of the autonomous research engine
[PvNP/system_v2](https://github.com/ludwigkubler/PvNP/tree/master/system_v2).

All artifacts here are generated without human intervention. Every entry is
**pre-registered**, multi-seed tested, adversarially critiqued, and — where
possible — formally verified in Lean 4. Failed attempts and dead frameworks
are kept as **metamathematical record**: the map of approaches that do NOT
work is as scientifically valuable as the map of those that do.

## Directory layout

```
SperimentalMath/
├── notebook/          ← individual cycle entries (one JSONL per month)
│   └── 2026-04.jsonl
├── frameworks/        ← Level-2 framework proposals and evolution
│   ├── proposed/      ← just proposed, not yet elaborated
│   ├── promoted/      ← fitness ≥ 0.3, actively evolved
│   ├── published/     ← fitness ≥ 0.5, paper written
│   └── dead/          ← fitness < 0.1, archived with post-mortem
├── papers/            ← auto-generated LaTeX + PDF for each SUPPORTED+CONFIRM
├── lean_verified/     ← Lean 4 files where `lake build` compiled (FORMAL_VERIFIED)
├── lean_stubs/        ← Lean 4 stubs that did not (yet) compile
├── barriers/          ← rejections grouped by which barrier killed them
│   ├── natural_proofs.jsonl
│   ├── relativization.jsonl
│   ├── algebrization.jsonl
│   └── karp_lipton.jsonl
├── reports/           ← human-readable markdown + PDF reports
│   ├── daily/
│   ├── supported_findings.md
│   ├── falsified_findings.md
│   ├── dead_frameworks_compendium.md
│   └── wall_atlas.md
└── stats.json         ← cumulative counters (machine-updated hourly)
```

## Read me if you're a human

Start with `reports/supported_findings.pdf` — it lists every
empirically-supported conjecture. **Only** entries in `lean_verified/`
correspond to machine-checked theorems. Everything else is a candidate
for review.

The "no-false-positive" policy: no claim from this repo is considered
mathematically valid unless it is in `lean_verified/` AND has been
independently reviewed. The critic agent + Lean gate give strong
pre-filtering, but `lake build` in an isolated Lean project is the
only deterministic check.

## What this repo is NOT

- Not a claim to solve P vs NP
- Not peer-reviewed
- Not a substitute for the working mathematician — it's a research assistant

## Cadence

The engine runs 24/7. Expected throughput (subject to rate limits):
- ~30 cycles per day (each ~60–90s, 30-min cooldown)
- ~1–2 SUPPORTED+CONFIRM per week (most will fail Lean gate)
- ~0.1–0.5 FORMAL_VERIFIED per week (goal: all become Mathlib PRs)
- 1 dead_frameworks.jsonl entry per hour (machine reports what didn't work)

Commits arrive hourly via `sync_output.sh` from the sec server.

## License

Apache-2.0.
