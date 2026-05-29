# Retractions — May 2026
**Repository:** [`ludwigkubler/SperimentalMath`](https://github.com/ludwigkubler/SperimentalMath)
**Issued:** 2026-05-23.
**Author:** Ludovico Kubler.

This notice is at the repository root so that any reader hitting the repo cold sees the retraction status before navigating to the `papers/` tree.

## What is retracted

- **`papers/compendium_v01.pdf` and `.tex`** — retracted. The four entries in this volume (`32a1e966ed26`, `e14f176e4ef1`, `44f82c29ed79`, `cca077d3c64c`) were claimed to be a "Tropical Fourier obstruction cluster"; three of the four were independently retracted on 2026-05-08 (see `retractions.json`) on the grounds that their tests used a hand-rolled "Tropical Fourier Transform" which is not in fact a Fourier-type quantity (it is a cyclic-rotation sum identically equal to $N \cdot \mathrm{mean}(f)$). The fourth, `e14f176e4ef1`, has a faithful Lean file at `lean_verified/e14f176e4ef1/Eaudit.lean` but its compendium presentation cites an unrelated arithmetic identity.
- **`papers/compendium_v02.pdf` and `.tex`** — retracted. Two entries: (a) `e14f176e4ef1` (as above); (b) `b0a4fb5d3039`, whose test refutes a conjecture about the k-CLIQUE minterm DNF using a Python function that does not build the k-CLIQUE minterm DNF (it builds out-stars per vertex).

The PDFs and `.tex` sources are kept under `papers/retracted/` for the historical record, with a stamp on the cover page.

## What replaces them

A single living document, [`papers/negative_observations_v0.1.md`](papers/negative_observations_v0.1.md), reframes the work as:
- inventory of 1772 cycles with 0 results,
- five recurring failure modes,
- **one** empirical measurement worth preserving (tropical discrepancy at finite β),
- pipeline corrections in flight,
- open questions for human collaborators.

## What does NOT change

- `notebook/2026-04.jsonl` and `notebook/2026-05.jsonl` — the raw cycle records — are NOT modified. The retraction is about *what is publicly framed as a result*, not about the historical telemetry.
- `retractions.json` — the per-entry retraction ledger — is unchanged.
- `lean_verified/e14f176e4ef1/Eaudit.lean` — the faithful Lean file — remains in place. It is not retracted; the *paper presentation that misquoted from a different Lean file* is.

## Why

Three reasons, in order of weight:

1. **Honesty.** Both compendia were assembled by an autonomous engine and admitted to public-facing `papers/` without an independent line-by-line audit. Code-level inspection on 2026-05-23 ([`REVIEW_2026-05-23.md`](REVIEW_2026-05-23.md)) found that neither the Lean files (in the LLM-generated `lean_counterexamples/` directory) nor the test-code constructions actually formalise the conjectures stated.
2. **Engineering.** The pipeline corrections being applied this week ([`INTERVENTION_PLAN_2026-05-23.md`](INTERVENTION_PLAN_2026-05-23.md)) include a fix that makes the compendium generator read from a stricter directory and refuse to publish a compendium with zero faithful entries. Retracting v01 and v02 brings the public artifacts in line with that policy.
3. **Methodology.** The repo's stated standard is "Royal-Society-grade" (`MULTIAGENT_PIPELINE.md`). Both compendia fall well below that bar on a first read. Public retraction now is cheaper than letting the volumes accumulate citations.

## Process for v03

The next compendium will be produced only when:
- at least one entry in `pvsnp_verified/<eid>/Eaudit.lean` passes `lake build`, AND
- the entry's Lean file references, by name, every primitive in the conjecture's statement (name-grep gate enforced by `pvsnp_compendium.py`), AND
- the human (L. K.) has signed off.

The Sunday cron that auto-generates the compendium is disabled until v03 is ready.

## Acknowledgement

These compendia were not the work of any external co-author. The errors are attributable to choices made by L. Kubler in the design of the pipeline (specifically, the `pvsnp_lean_counterexample.py` prompt that instructed the LLM to *replace* conjecture primitives with arithmetic surrogates). The independent 2026-05-23 review and the multiagent pipeline document are part of the corrective record. The retraction is published in the same repository where the originals appeared.

— L. Kubler, 2026-05-23.
