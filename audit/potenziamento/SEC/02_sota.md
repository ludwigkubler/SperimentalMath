# SOTA comparison — 5 systems vs SEC

Date: 2026-05-13. 5 WebSearch queries used.

---

## 1. Aviary (FutureHouse) — agent gym for scientific tasks

- Repo: https://github.com/Future-House/aviary
- Paper: https://arxiv.org/abs/2412.21154 (HTML: https://arxiv.org/html/2412.21154v1)
- Announcement: https://www.futurehouse.org/research-announcements/aviary

**What it is.** A Gym-style framework where language agents (named *Crows*) face multi-step scientific tasks with tool use. Five environments shipped: 3 scientific (incl. **SeqQA**, **LitQA2**, **protein stability**) + GSM8k + hotpotQA. Companion library **LDP** (Language Decision Processes) defines agent compute graphs that can be trained/optimized.

**Capability chiave.** `env.reset()` / `env.step(action)` interface; tools/tasks are *part of the environment*, the agent is a compute graph that can be optimized end-to-end. Agents exceed zero-shot frontier LLMs on SeqQA/hotpotQA/LitQA2/protein-stability; **exceed human performance on SeqQA and LitQA2**.

**Cosa SEC potrebbe imparare.**
1. *Reproducible benchmark harness*: SEC has scattered metrics but no Gym-like env that re-runs the same scientific tasks before/after a change. A `sec-gym` with `step/reset` semantics around the conjecture graph would let any code change be A/B'd on a fixed task suite — the roadmap's "non-negotiable measurability" principle.
2. *LitQA2-style literature-grounding benchmark* for `pvsnp_explorer` regression testing.
3. *Compute-graph view of agents*: SEC's orchestrator is currently a hand-coded pipeline; Aviary shows how to lift it to a graph that's trainable.

---

## 2. AI Scientist v2 (Sakana AI) — end-to-end automated paper writing

- Repo: https://github.com/SakanaAI/AI-Scientist-v2
- Paper PDF: https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf
- HuggingFace: https://huggingface.co/papers/2504.08066

**What it is.** Successor to AI Scientist v1; removes hand-written templates. End-to-end agentic loop: hypothesis → tree-searched experiments → analysis → manuscript draft → peer-review-style critique.

**Capability chiave.**
- **Agentic Tree Search** (ATS): the research process itself is a tree; a `experiment_manager_agent` expands nodes, prunes dead branches.
- **VLM (Vision-Language Model) feedback** on figures/plots.
- **Parallel experiment execution** with shared budget.
- One v2 manuscript scored 6.33 average at the ICBINB workshop (ICLR 2025) — above human acceptance threshold.

**Cosa SEC potrebbe imparare.**
1. *Tree search over research moves.* SEC has `conjecture_graph.py` but transitions are linear (OPEN→FORMALIZING→...). AI Scientist v2 treats each (hypothesis, experiment, ablation) as an explorable tree node with cost+reward.
2. *VLM critic*: SEC produces matplotlib plots in `lab_c001/` but never has the system *look* at them. A small VLM (Qwen2-VL, MiniCPM-V) running locally could flag broken/uninformative figures.
3. *Paper-writer reviewer pack*: SEC has `pvsnp_reviewer_pack.py` (a positive sign) — extend it with AI-Scientist-style **automated reviewer agent** that scores draft sections 1-10 and produces revision diffs.

---

## 3. AutoGen v0.4 → Microsoft Agent Framework — multi-agent orchestration

- Repo: https://github.com/microsoft/autogen
- New successor: https://github.com/microsoft/agent-framework
- v0.4 redesign blog: https://www.microsoft.com/en-us/research/project/autogen/
- 2026 explainer: https://sanj.dev/post/autogen-microsoft-multi-agent-framework

**What it is.** v0.4 (Jan 2025) rewrote the framework around an **asynchronous actor model**; March 2026 split into **Microsoft Agent Framework (MAF)** as the production line and **AutoGen v0.7.x** as the research/prototyping fork.

**Capability chiave.**
- Async messaging between actors (request/response + event-driven).
- **First-class OpenTelemetry** integration (tracing across agent boundaries).
- **Distributed agent networks** across organizational boundaries.
- Pluggable memory, tools, models.

**Cosa SEC potrebbe imparare.**
1. *OpenTelemetry across the bus*. SEC has `observability.py` mimicking OTel "shape" but no real export. The roadmap mentions "OpenTelemetry tracing on agent dispatch" as non-negotiable trans-roadmap debt — AutoGen v0.4 shows the canonical wiring.
2. *Actor handles vs direct method calls.* SEC's `communication/bus.py` is a single-process pub/sub; AutoGen's runtime supports same-process and distributed actor handles transparently. SEC will need this if it spawns sub-agents (`agent_spawner.py`).
3. *Group chat / round-robin patterns* (RoundRobinGroupChat, SelectorGroupChat) — SEC's orchestrator is pipeline-only; group chat enables debate/critic patterns.

---

## 4. Smallville / Generative Agents (Park 2023)

- Paper: https://arxiv.org/abs/2304.03442
- ACM (UIST): https://dl.acm.org/doi/10.1145/3586183.3606763
- Stanford HAI: https://hai.stanford.edu/news/computational-agents-exhibit-believable-humanlike-behavior

**What it is.** 25 NPCs in a sandbox town; each has a *memory stream* of natural-language observations, a *reflection* module that periodically synthesizes higher-level insights, and a *retrieval* function `recency·importance·relevance` that pulls the top-k memories for any prompt.

**Capability chiave.**
- **Reflection** loop: when sum of recent memory importance crosses a threshold, the agent asks itself "what are 3 high-level questions I can ask?" → answers them → stores the answers back as new memories with their own importance scores.
- **Importance assignment at write time** (LLM rates each new memory 1–10).
- **Plan-tree** for daily activities, recursively decomposed.

**Cosa SEC potrebbe imparare.**
1. *Reflection loop*: SEC has `scoring.py` (the retrieval formula) and `dreamscape.py` + `consolidation.py` but **no Park-style threshold-triggered reflection generator** that explicitly produces new high-level memories. Worth wiring — it's the missing half of "weighted retrieval".
2. *Plan tree*: SEC plans tasks atomically; Smallville's hierarchical plan (day → hour → minute) maps nicely onto SEC's research roadmaps (week → sprint → obligation).
3. *Importance at write time* — confirm it's actually called on every memory write (the `scoring.py` defaults `importance=5` for legacy, so probably under-utilized).

---

## 5. Voyager (NVIDIA, Wang 2023)

- Paper: https://arxiv.org/abs/2305.16291
- Repo: https://github.com/MineDojo/Voyager
- Project page: https://voyager.minedojo.org/

**What it is.** First LLM-powered lifelong-learning Minecraft agent. Three components: (1) **automatic curriculum** that picks next task to maximize exploration, (2) **skill library** of executable JavaScript snippets, (3) **iterative prompting** with environment feedback + self-verification.

**Capability chiave.**
- Skills are **executable code** with parameters; new skills are *composed* from old ones.
- **Self-verification** via a critic LLM that decides if a task succeeded based on game state diff.
- **Curriculum** balances exploration (new biomes) vs exploitation (refining known recipes).
- 3.3× more items than prior SOTA, 15.3× faster tech-tree milestones.

**Cosa SEC potrebbe imparare.**
1. *Self-verification critic*: SEC's `learning_hooks` uses a hard quality threshold (`0.7`), but Voyager's verifier is *task-aware* — knows what "success" means for *this specific* task. SEC could specialize the verifier per agent type (coder, math, research).
2. *Executable skills* (SEC currently stores skills as *prompt templates only* — explicitly noted in `skills.py` comment: *"we skip the code-execution component"*). Re-introducing safe executable skills (Python snippets in a sandbox) is the biggest power-up — a *parametric* skill becomes a callable function, not text.
3. *Automatic curriculum*: SEC's `autonomy.py` schedules behaviors with intervals + MAB, but doesn't pick tasks that *extend skill frontier*. The roadmap Phase-1 Voyager-lite section explicitly plans this; not yet wired.
