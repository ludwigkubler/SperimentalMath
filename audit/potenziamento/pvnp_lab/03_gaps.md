# PvsNP Lab — Gap Analysis (ranked)

Score = Impact * 2 - Effort (max 10, min -3). Sorted desc.

| # | Capability | In PvsNP Lab? | In SOTA | Sistema | Impact (1-5) | Effort (1-5) | Score | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Premise retrieval (DPR/dense) over Mathlib + lab_c001 lemmas | NO (uses `exact?` only) | yes | LeanDojo/ReProver | 5 | 2 | 8 | Drop-in: index `lab_c001/lean/TseitinTw/*.lean` + Mathlib once, hot path = embed goal + top-k; pass to LLM tactic prompt. Single biggest pass@1 win. |
| 2 | Persistent Lean kernel (no re-import per cycle) | NO (`lake build` per attempt) | yes | LeanDojo | 5 | 2 | 8 | Each cycle currently pays ~4 min Mathlib import. LeanDojo's persistent process turns that into seconds. 5-10x cycle throughput. |
| 3 | Log every NL→Lean autoformalization pair, success or fail | partial (`pvsnp_lean_gate_log.jsonl` written, not used) | yes | AlphaProof | 5 | 2 | 8 | We already write logs — add a sidecar dataset writer + a weekly LoRA fine-tune script on `lean4-base`. Compounds over time. |
| 4 | FunSearch-style island evolution of test programs per conjecture | NO (one test per cycle) | yes | FunSearch | 5 | 3 | 7 | For each SUPPORTED candidate, run an island of N test programs; pick best by signal strength before Lean gate. Cheaper than re-trying Lean. |
| 5 | VLM critique of generated figures (lab_c001 plots, system_v2 paper figures) | NO | yes | AIS v2 | 3 | 2 | 4 | Cheap, catches mislabeled axes / missing baselines / suspicious-looking curves in `make_plots.py` outputs. Auto-flag for human review. |
| 6 | Symbolic deduction engine for complexity-theory fragment (CNF / clause / width / treewidth lattice) | NO | yes | AlphaGeom2 | 5 | 5 | 5 | Big build but maps directly onto Tseitin / proof complexity. Start tiny: deduce width bounds from clause graph properties. |
| 7 | MCTS / iterative best-first over tactic candidates (Level 3) | NO (single LLM call/step) | yes | AlphaProof | 4 | 3 | 5 | Inside `pvsnp_lean_gate._llm_tactic_step`: generate K candidates, score each by post-state simplicity, expand top. |
| 8 | Cross-conjecture lemma reuse across Lean stubs | NO (silos) | yes | LeanDojo, AG2 | 4 | 3 | 5 | Each FORMAL_VERIFIED stub becomes a premise for the next cycle's retriever. F4 framework already provides scaffolding. |
| 9 | Knowledge-sharing search trees between framework children (F4) | NO (children re-explore from scratch) | yes | AG2 | 4 | 3 | 5 | When F4 mutates a parent framework, transfer the shared sub-conjecture results / Lean stubs / barrier verdicts to children. |
| 10 | Adversarial debate / multi-agent critic agreement (beyond barrier filter) | partial (single skeptic) | partial | (DeepMind debate, AIS v2 review) | 3 | 2 | 4 | 2 LLMs debate the SUPPORTED verdict, third LLM judges. Already half implemented in barriers — generalize the pattern. |
| 11 | Autoformalization training: LoRA fine-tune on accumulated NL→Lean pairs | NO | yes (RL+SFT) | AlphaProof | 4 | 4 | 4 | Once #3 ships, run a nightly LoRA training on a 7B base. Even modest gains compound. Hardware: server RTX 3070 Ti (per memory). |
| 12 | Tree search over experimental design space, not just solutions | NO (linear pipeline) | yes | AIS v2 | 3 | 3 | 3 | Per conjecture, branch on (test-formulation, seed, parameter range) and prune by signal. Generalizes #4. |
| 13 | Accessible-premise guard (no use-before-definition cheating) | NO | yes | LeanDojo | 3 | 2 | 4 | Static analysis: a retrieved premise must be visible in the import graph of the current stub. Prevents Lean gate false positives. |
| 14 | Manuscript polish loop (multi-pass draft → fig check → simulated review → revise) | NO (single write_paper call) | yes | AIS v2 | 3 | 2 | 4 | Today's `pvsnp_explorer.write_paper` is 1 call. v2-style multi-pass yields publication-quality drafts without human touch. |
| 15 | Negative-result reuse beyond logging (curriculum, anti-blacklist) | partial (`_build_blacklist` only) | yes | AlphaProof | 3 | 2 | 4 | Use rejected proposals as **hard negatives** when training novelty embedder; near-misses become positive-anchor data for next proposer. |

---

## Top 6 by Score (≥6)

1. **Premise retrieval** (DPR/dense over Mathlib + lab_c001) — score 8
2. **Persistent Lean kernel** — score 8
3. **NL→Lean autoformalization pair logging + corpus** — score 8
4. **FunSearch island per conjecture** — score 7

(5-9 tied around 5.)

## Costed estimates for top-6 (rough)

| # | Item | ETA | LOC | New deps |
|---|------|-----|-----|----------|
| 1 | Retrieval module | 1.5 days | ~350 | `sentence-transformers`, `faiss-cpu` |
| 2 | LeanDojo integration | 2 days | ~250 | `lean-dojo` |
| 3 | NL→Lean dataset pipeline | 0.5 day | ~120 | none |
| 4 | FunSearch islands | 2.5 days | ~500 | none (multiproc) |
| 5 | VLM figure critique | 0.5 day | ~80 | router already supports vision |
| 6 | Symbolic deducer (CNF / width / tw) | 5 days+ | ~1200 | none (pure Python) |
