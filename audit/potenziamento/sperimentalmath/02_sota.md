# SOTA comparison — curation / verification pipelines for math outputs

## SOTA 1. OEIS — On-Line Encyclopedia of Integer Sequences

- **URL**: https://oeis.org/wiki/Overview_of_the_contribution_process
- **What it does**: gold-standard curated database of integer sequences (≈ 380k entries).
- **Key capabilities**:
  - **Pink-box review loop**: editors leave inline comments visible on the draft page; contributors answer in the same UI; no entry goes live without back-and-forth.
  - **Hierarchical roles**: ~130 editors; Associate Editors triage; Editor-in-Chief approves publication.
  - **Submission throttling**: limit lowered from 7 → 3 simultaneous drafts to *force severe self-curation* before submission. Forces priority.
  - **Style sheet** enforced (canonical formatting, cross-references, b-files).
  - Every entry has a permanent A-number; corrections are tracked in history not by overwrite.
- **Lesson for sperimentalmath**: submission rate limiting + pink-box dialog model would close the "no-skeptic-invoked" gap (405/707 cycles skipped review per health_report).

## SOTA 2. PolyMath Project

- **URLs**:
  - Hub: https://polymathprojects.org/
  - Wiki (Nielsen): https://michaelnielsen.org/polymath/index.php?title=Main_Page
  - General rules: https://polymathprojects.org/general-polymath-rules/
- **What it does**: open, blog-driven, massively-collaborative attempts on hard open problems (Polymath1 settled density Hales-Jewett in 37 days, 800 comments).
- **Key capabilities**:
  - **Wiki as live state**: every project has a dedicated wiki page maintaining the canonical statement, partial progress, and the **list of failed approaches** (a "dead approaches" log — very close to what `frameworks/dead/` aims to be).
  - **Numbered comments + threading**: every idea has a citation handle, makes the proof trail auditable.
  - **Explicit rules**: small atomic comments, no long preludes, attribution per-comment.
- **Lesson for sperimentalmath**: `frameworks/dead/` (currently 0 entries) should mirror PolyMath's "approaches that did not work" page format, with reasons and post-mortems.

## SOTA 3. Mathlib4 — Lean 4 community library

- **URLs**:
  - Contribute: https://leanprover-community.github.io/contribute/index.html
  - Queueboard: https://leanprover-community.github.io/queueboard/
  - Roadmap: https://mathlib-initiative.org/roadmap/
- **What it does**: monorepo of formalised mathematics (≈ 2000 open PRs as of Sept 2025).
- **Key capabilities**:
  - **Queueboard**: real-time dashboard of every PR with state (awaiting-review, awaiting-author, awaiting-CI, awaiting-maintainer-approval).
  - **Tiered reviewers**: maintainers + a separate larger Reviewers team (community members who can approve).
  - **CI enforcement**: every PR must `lake build` and pass `lint`. No exceptions.
  - **Editorial team**: paid professional triage as of Oct 2025 → Sept 2026 to clear backlog.
  - **Explicit policy on AI**: as of April 2026, Mathlib refuses LLM-generated PRs from new contributors because "AI-written code fails to meet mathlib's very high standards by a large margin".
- **Lesson for sperimentalmath**: a queueboard-style dashboard for the 1261 reviewer packs would dramatically improve human oversight. The AI-content policy is a direct warning to sperimentalmath: it has the opposite problem (all PRs are LLM-generated), so the Lean-verification gate (Gate 4) and human sign-off must be inviolable.

## SOTA 4. AlphaProof / AlphaGeometry 2 (DeepMind)

- **URLs**:
  - Blog (silver IMO): https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
  - Nature paper: https://www.nature.com/articles/s41586-025-09833-y
  - Gold IMO update: https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/
- **What they do**: RL-trained Lean prover. Auto-formalised ≈ 80 M propositions, won silver at IMO 2024 (28/42), gold-level at IMO 2025 with Gemini Deep Think.
- **Key capabilities**:
  - **Train-time + test-time RL**: at inference, generates millions of *related problem variants* and learns from them before answering the actual question. Highest investment per problem.
  - **Auto-formalisation pipeline** with Gemini (NL → Lean).
  - **Honesty about scope**: the IMO solutions still required *manual formalisation* of 5/6 problems by experts. The blog explicitly states what was automated and what was hand-done.
- **Lesson for sperimentalmath**: the test-time RL pattern is a path for the 670 INCONCLUSIVE entries — generate variants of each crashed test, learn from which fix worked. And the *honesty about what was automated* is the model: sperimentalmath's reports should clearly distinguish "engine-supported" from "Lean-verified" from "human-reviewed".

## SOTA 5. Retraction Watch + Open Science Framework

- **URLs**:
  - Retraction Watch: https://retractionwatch.com/
  - Wikipedia (history): https://en.wikipedia.org/wiki/Retraction_Watch
  - OSF retraction policy: https://cajmhe.com/index.php/journal/article/view/401
- **What it does**: public, indexed database of retracted scientific papers (32 000+ entries). OSF policy: preprints can be silently withdrawn but bibliometric metadata (title, authors, abstract) **must stay intact** so external citations don't break.
- **Key capabilities**:
  - **Public, queryable, persistent**: retraction is not deletion, it's annotation.
  - **Reason taxonomy** (not-reproducible, data-fabrication, image-duplication, …).
  - **Reverse links**: a retracted paper's DOI keeps resolving but the landing page is stamped RETRACTED.
- **Lesson for sperimentalmath**: this is exactly what is missing. `retractions.json` exists, but `supported_findings.md` still shows 4 retracted entries as SUPPORTED with no visible stamp. The OSF model — keep the page, stamp it loud — should be adopted.

---

## Bonus references

- OEIS Style Sheet (https://oeis.org/wiki/Style_Sheet) — concrete template per entry.
- Verified Compass (Lean tactic archive) — emerging convention for tracking which theorems have alternative computer-verified proofs. Marginal for sperimentalmath today but relevant if the project starts contributing back to Mathlib.
