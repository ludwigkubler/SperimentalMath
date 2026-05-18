---
title: "SEC P vs NP — SUPPORTED findings"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-18 13:47 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — SUPPORTED findings

> **⚠ AUDIT 2026-05-08**: this report has been filtered against `retractions.json`. Some entries previously listed here have been retracted following a code-level audit. See [`AUDIT_2026-05-08.md`](../AUDIT_2026-05-08.md) for the full audit document and [`MULTIAGENT_PIPELINE.md`](../MULTIAGENT_PIPELINE.md) for the new review pipeline.

Compiled 2026-05-18 13:47 UTC from pvsnp_notebook.jsonl.
0 conjectures empirically supported (on small instances; all require follow-up at larger n).

> **Important caveat**: these are _empirical_ results on instances of size ≤ 20. 
> A SUPPORTED verdict here means the test did not find a counterexample in the sampled regime. 
> Genuine mathematical validation requires: (i) extending the test to n ≥ 50, 
> (ii) proving the bound analytically, (iii) independent reproduction.

_No SUPPORTED verdicts in the curated set._

---

## Retractions (originally `SUPPORTED`)

The following 3 entries were removed from this report on 2026-05-08 per the audit document. They are preserved in the raw `notebook/*.jsonl` for traceability but are NOT to be cited as scientific output.

### `7cbbaa3e1e4a` — Tropical Rank of Clause-Indicator Polynomial Bounds ACC Circuit Size

- **Original verdict**: `SUPPORTED`
- **Action**: `RETRACTED`
- **Reason**: Malformed test: cnf_to_tropical_matrix uses len(cnf[0]) as variable count; acc_circuit_size counts clauses+literals, no relation to ACC^0 complexity. The reported support_fraction is an XNOR artefact in the chosen n. Novelty filter recorded 0 arXiv hits.

### `b43a4129e5c5` — Ideal Generators Count Bounds Communication Complexity

- **Original verdict**: `SUPPORTED`
- **Action**: `RETRACTED`
- **Reason**: Pure stub: comm_complexity(f, n) := n, ideal_generators(f, n) := 2*n. Test reduces to n <= 2n, trivially true. Output line contained the unresolved placeholder 'RESULT: SUPPORTED <metric>=<value>'. Novelty filter recorded 0 arXiv hits.

### `e006a48b37a7` — Frobenius-Schur Indicator of Clause-Symmetry Group Predicts SAT Symmetry Breaking Cost

- **Original verdict**: `SUPPORTED`
- **Action**: `RETRACTED`
- **Reason**: Stub test: frobenius_schur_sum returns hard-coded constants based on string label; add_lex_leader_clause returns a fixed number of dummy clauses. Reported ratio_avg is the deterministic average of those constants. No CDCL run, no representation theory computed.


---

## Demoted entries (originally `SUPPORTED`, now `INCONCLUSIVE` pending reformulation)

### `15ae8fd62af0` — Grothendieck-Witt Class of Clause Polynomials Mod 2 Predicts Resolution Width

- **Original verdict**: `SUPPORTED`
- **New verdict**: `INCONCLUSIVE`
- **Action**: `DEMOTED_PENDING_REFORMULATION`
- **Reason**: Statement-test mismatch. The conjecture is stated over F_2 where Q(x) = sum <c,x>^2 mod 2 is linear (since a^2 = a in F_2), making the bilinear form B identically zero and the conjecture vacuous. The test silently substitutes 'integer inner product, then squared, then reduced mod 2', i.e. tests a different statement. The underlying intuition (Grothendieck-Witt class of clause polynomials) may be salvageable via re-formulation with an explicit ring assignment; pending such re-formulation, demoted to INCONCLUSIVE.
