# Φ on Tseitin — three-round draft bundle

**Ludovico Kubler** — committed 2026-06-01.

This directory contains the trajectory of three adversarial-publication
rounds on the cumulative-clause-space measure
$\Phi(\pi) = \sum_{t} |M_t|$ on Tseitin formulas, with the formal anchor in
`Conjecture003.lean` (cumulativeEntropy / proofStateEntropy).

## Files

| File | Status | Length |
|---|---|---:|
| `v1_phi_tseitin_draft.md` | First-pass draft. Panel verdict: 2 × `B_arxiv_preprint` + 1 × `C_negative_appendix`. | 193 lines |
| `v2_phi_tseitin_draft.md` | Closes 5 gaps. Introduces stretched-exp model (winning AIC). Panel verdict: 3 × `MAJOR_REVISION`. | 253 lines |
| `v3_phi_tseitin_draft.md` | Lemma A scope corrected; cluster-robust AIC; Tobit framework; SC verbatim. Panel verdict: 3 × `MAJOR_REVISION` (3 surgical defects remain). | 428 lines |
| `v3.5_cleanup_delta.md` | Delta over v3: honest Lemma A Lean stub, sign-test 7/0/1 recount, full censoring report including `rand_4reg`, concrete server-hour compute budget. | 143 lines |
| `preregistration_audit.md` | SC1–SC6 verbatim from the registry with status (refuted / partial / supported / aligned). | 145 lines |
| `zenodo_README.md` | Replication-package README pointing at the harnesses + raw `.jsonl` data files. | 101 lines |

## Honest disposition

This is **modest** empirical mathematics, not a P-vs-NP-relevant result.
The contribution is an empirical localisation of $\Phi$ on Tseitin under
DP min-occurrence inside the open ADRNV (ITCS 2017, Lemma 12) / Ben-Sasson–
Wigderson (JACM 2001) gap, with documented heuristic- and prover-
conditional negative findings (SC2, SC4 refuted by the data).

Posted to the mirror as a safety-net commit pending the v4 compute-upgrade
(~21 server-hours of additional runs detailed in `v3.5_cleanup_delta.md`
§D), which is now running on the SEC server.

## Companion artefacts on the server

`ssh ludo@sec ~/Scrivania/SEC/research/programme_harnesses/data/` contains the
14 scripts and `.jsonl` data files that produced the numerics above:

- `c003b_harness.py` — live harness used by the autonomous explorer.
- `urquhart.py` + `urquhart_data.jsonl` — certified-expander Tseitin.
- `structured_graphs.py` + `structured_table.txt` — grid / hypercube / cycle / tree / path.
- `drat_phi.py`, `paired_drat_dp.py`, `drat_paired*.jsonl` — DRAT cross-check vs DP.

## Companion: the rigorous negative theorem

For a **rigorous** (Theorem-grade) result from the same autonomous-research
session, see `papers/forman_ricci_saturation_note.md` (committed earlier in
this branch): $\mu(F^*_v) = \Theta((\log_2 v)^2)$ on the term-overlap graph
of the correct k-CLIQUE minterm DNF, closing the Forman–Ricci-as-monotone-
lower-bound-measure direction with a complete proof and a crossover at $v=194$.

— L. Kubler
