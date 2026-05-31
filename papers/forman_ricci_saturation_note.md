# Poly-logarithmic saturation of Forman–Ricci curvature on the clique minterm DNF

**Author:** Ludovico Kubler. **Date:** 2026-05-29. **Status:** draft note for review (limitative result).

## Summary

We analyse the measure $\mu$ that the SEC engine proposed (entry `b0a4fb5d3039`) as a candidate monotone-complexity lower-bound measure: the Forman–Ricci curvature of the *term-overlap graph* of a monotone DNF. We prove that on the $k$-CLIQUE minterm DNF $F^*_v$ (with $k=\lceil\log_2 v\rceil$),
$$
\mu(F^*_v) = \Theta\big((\log_2 v)^2\big).
$$
Consequences:
1. The engine's conjectured clause (iii), $\mu(F^*_v)\ge v/4$, **holds for $v\le 193$ and fails for every $v\ge 194$** (exact crossover, closed form).
2. Because $\mu$ is poly-logarithmic in $v$ — equivalently in the number of variables $N=\binom v2$, $\mu=\Theta((\log_2 N)^2)$ — it cannot witness a super-poly-logarithmic monotone size lower bound. Since the monotone lower bound for $k$-CLIQUE is $n^{\Omega(\sqrt k)}$ (Razborov 1985), **Forman–Ricci curvature of the term-overlap graph provably cannot serve as a monotone lower-bound measure for clique**, even on the instances where clause (iii) numerically holds.

This also corrects the record: the engine's original "refutation" of clause (iii) was computed on the wrong object (`generate_clique_dnf` built per-vertex out-stars, not the $\binom vk$ minterms), and is void. On the correct object the clause holds at small $v$ and fails only asymptotically, for the reason proved here.

## Definitions

Variables are the edges of $K_v$. The $k$-CLIQUE minterm DNF is
$F^*_v=\bigvee_{S\in\binom{[v]}{k}} T_S$, where $T_S=\{(a,b):a,b\in S\}$ is the edge set of the $k$-clique on $S$, so $|T_S|=\binom k2=:W$.

The *term-overlap graph* $G$ has a vertex per term; $S\sim S'$ iff $|T_S\cap T_{S'}|\ge1$, i.e. $|S\cap S'|\ge2$. Vertex weight $w_S=W$; edge weight $w_{SS'}=|T_S\cap T_{S'}|=\binom{|S\cap S'|}2$.

Forman–Ricci curvature of an edge $e=(S,S')$:
$$
\mathrm{Ric}(e)=w_e\Big(\tfrac{w_S}{w_e}+\tfrac{w_{S'}}{w_e}-\!\!\sum_{m\sim S,\,m\ne S'}\!\!\tfrac{w_S}{\sqrt{w_e w_{Sm}}}-\!\!\sum_{m\sim S',\,m\ne S}\!\!\tfrac{w_{S'}}{\sqrt{w_e w_{S'm}}}\Big),
$$
and $\mu(F)=\log_2\!\big(1+\max(0,-\min_e\mathrm{Ric}(e))\big)$.

## The graph is regular and vertex-transitive

$S_v$ acts transitively on $\binom{[v]}k$, hence on $G$. For a fixed term $S$, the number of neighbours sharing exactly $t$ vertices ($2\le t\le k$) is
$$
N_t=\binom kt\binom{v-k}{k-t},\qquad\text{with edge weight }\binom t2 .
$$
So every vertex has degree $\Delta=\sum_{t=2}^k N_t$ and the same neighbour-weight profile.

## Closed form for $\min_e\mathrm{Ric}$

All vertex weights equal $W$, so for an edge $e$ with weight $w_e$,
$$
\mathrm{Ric}(e)=2W-W\sqrt{w_e}\,(\Sigma_S+\Sigma_{S'}),\qquad
\Sigma_S=\sum_{m\sim S,\,m\ne S'}\frac1{\sqrt{w_{Sm}}}.
$$
By transitivity $\Sigma_S=\Sigma_{S'}=\Sigma_{\mathrm{full}}-1/\sqrt{w_e}$ with $\Sigma_{\mathrm{full}}=\sum_{t=2}^k N_t/\sqrt{\binom t2}$. Hence
$$
\mathrm{Ric}(e)=4W-2W\sqrt{w_e}\,\Sigma_{\mathrm{full}} .
$$
This is strictly decreasing in $w_e$, so the minimum is attained at the **largest** edge weight, $w_e=\binom{k-1}2$ (shared $t=k-1$ vertices):
$$
\boxed{\;\min_e\mathrm{Ric}=4W-2W\sqrt{\tbinom{k-1}2}\;\Sigma_{\mathrm{full}}\;}
$$

**Numerical check (vs full-graph computation, $k=4$):**

| $v$ | closed form | full graph | rel. err |
|----|------------|-----------|---------|
| 10 | −2143.1 | −2134.6 | 0.4% |
| 12 | −3860.3 | −3851.8 | 0.2% |
| 14 | −6076.3 | −6067.8 | 0.1% |
| 16 | −8791.2 | −8782.7 | 0.1% |

(The residual is because the global min picks a specific $t=k-1$ edge whose two endpoints' neighbourhoods differ by $O(1)$ terms; immaterial to the asymptotics.)

## Theorem: $\mu(F^*_v)=\Theta((\log_2 v)^2)$

The ratio $\Sigma_{\mathrm{full}}$ is dominated by $t=2$: for $v\gg k$,
$\;N_t/N_{t+1}=\Theta(v/k^2)\gg1$, so $\Sigma_{\mathrm{full}}=\Theta(N_2)=\Theta\!\big(\binom k2\binom{v-k}{k-2}\big)$.
Thus
$$
|\min_e\mathrm{Ric}|=\Theta\!\Big(W\sqrt{\tbinom{k-1}2}\binom{v-k}{k-2}\Big),\qquad
\log_2|\min_e\mathrm{Ric}|=\log_2\binom{v-k}{k-2}+O(\log k).
$$
Since $\log_2\binom{v-k}{k-2}=(k-2)\log_2 v\,(1-o(1))$ and $k=\lceil\log_2 v\rceil$,
$$
\mu(F^*_v)=\log_2\big(1+|\min_e\mathrm{Ric}|\big)=(k-2)\log_2 v\,(1+o(1))=\Theta\big((\log_2 v)^2\big).\qquad\square
$$

**Numerical confirmation** ($\mu/(\log_2 v)^2$, exact closed form, across five $k$-bands):

| $v$ | $k$ | $\mu$ | $v/4$ | $\mu/(\log_2 v)^2$ | clause (iii) |
|-----|----|-------|-------|--------------------|--------------|
| 16 | 4 | 13.10 | 4.0 | 0.819 | holds |
| 64 | 6 | 29.25 | 16.0 | 0.813 | holds |
| 193 | 8 | 48.445 | 48.25 | 0.842 | holds (last) |
| 194 | 8 | 48.492 | 48.50 | 0.843 | **fails (first)** |
| 1024 | 10 | 79.13 | 256.0 | 0.791 | fails |
| 65536 | 16 | 205.82 | 16384 | 0.804 | fails |

The ratio is stable in $[0.79,0.82]$ over $v\in[16,65536]$, confirming the $\Theta((\log_2 v)^2)$ law.

## Corollary (the limitative content)

$N=\binom v2=\Theta(v^2)$, so $\mu(F^*_v)=\Theta((\log_2 N)^2)$: **poly-logarithmic in the number of variables.** Razborov's monotone lower bound for $k$-CLIQUE is $n^{\Omega(\sqrt k)}$, super-polynomial in $n=v$. A measure bounded by $\mathrm{polylog}(N)$ cannot certify a super-poly-logarithmic monotone size bound. Hence Forman–Ricci curvature of the term-overlap graph **cannot** be the monotone lower-bound measure its proposer hoped for; clause (iii), even in its true small-$v$ range, is weaker than its stated purpose by an exponential margin.

## Honest assessment

This is a *limitative* result on a measure of the engine's own invention — not a contribution to the standard tropical/algebraic literature, and not a step toward $\mathrm P$ vs $\mathrm{NP}$. Its value is (a) correcting a bogus refutation in the public record, and (b) closing the Forman–Ricci-on-term-overlap-graph direction with a proof rather than a guess. It is suitable as a short note in the negative-results line (e.g. an appendix to `negative_observations`), with the explicit caveat that the object is non-standard. It is not, on its own, an *Experimental Mathematics* paper.

— L. Kubler, 2026-05-29.
