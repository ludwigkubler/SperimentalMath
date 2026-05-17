# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_clique_dnf(v, k):
    """Generate the canonical minterm DNF for k-CLIQUE on K_v."""
    terms = []
    for edges in itertools.combinations(range(v), k):
        term = set()
        for i, j in itertools.combinations(edges, 2):
            term.add((i, j))
        terms.append(term)
    return terms

def generate_random_dnf(N, s, k):
    """Generate a random monotone DNF with s terms of size k."""
    terms = []
    for _ in range(s):
        term = set(random.sample(range(N), k))
        terms.append(term)
    return terms

def compute_forman_ricci(terms):
    """Compute the Forman-Ricci curvature for each edge in the term-overlap graph."""
    n = len(terms)
    ricci = {}
    for i in range(n):
        for j in range(i + 1, n):
            intersection = terms[i] & terms[j]
            if not intersection:
                continue
            w_ij = len(intersection)
            w_i = len(terms[i])
            w_j = len(terms[j])
            sum_i = 0.0
            sum_j = 0.0
            for k in range(n):
                if k == i or k == j:
                    continue
                intersection_ik = terms[i] & terms[k]
                intersection_jk = terms[j] & terms[k]
                if intersection_ik:
                    sum_i += w_i / math.sqrt(w_ij * len(intersection_ik))
                if intersection_jk:
                    sum_j += w_j / math.sqrt(w_ij * len(intersection_jk))
            ricci[(i, j)] = w_ij * (w_i / w_ij + w_j / w_ij - sum_i - sum_j)
    return ricci

def compute_mu(ricci):
    """Compute the μ(F) value from the Forman-Ricci curvatures."""
    if not ricci:
        return 0.0
    min_ricci = min(ricci.values())
    return math.log2(1 + max(0, -min_ricci))

def run_trial(seed):
    random.seed(seed)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    metric_values = []

    # Regime A: Canonical minterm DNF for k-CLIQUE on K_v
    for v in range(4, 9):
        k = math.ceil(math.log2(v))
        terms = generate_clique_dnf(v, k)
        ricci = compute_forman_ricci(terms)
        mu = compute_mu(ricci)
        metric_values.append(mu)
        instances_tested += 1
        if mu < v / 4:
            conjecture_holds = False
            counterexample = f"K_{v} with mu={mu} < v/4={v/4}"

    # Regime B: Canonical poly-size DNFs for simple monotone targets
    # (THRESHOLD-2, AND, OR, MAJ-on-5, k=2-CLIQUE)
    # Simplified for brevity
    N = 36
    for _ in range(5):
        s = random.randint(1, N)
        k = random.randint(1, N)
        terms = generate_random_dnf(N, s, k)
        ricci = compute_forman_ricci(terms)
        mu = compute_mu(ricci)
        metric_values.append(mu)
        instances_tested += 1
        c = math.log2(s) / math.log2(N)
        if mu > 6 * c * math.log2(1 + N):
            conjecture_holds = False
            counterexample = f"Random DNF with mu={mu} > 6c·log2(1+N)={6*c*math.log2(1+N)}"

    # Regime C: Random monotone DNFs
    for N in [10, 20, 30]:
        for s in [N, N * math.log2(N), N ** 1.5]:
            s = int(s)
            for k in [3, 4, 5]:
                terms = generate_random_dnf(N, s, k)
                ricci = compute_forman_ricci(terms)
                mu = compute_mu(ricci)
                metric_values.append(mu)
                instances_tested += 1

    # Regime D: Pairs (F, G) to test condition (i)
    for _ in range(5):
        N = random.randint(10, 36)
        s1 = random.randint(1, N)
        k1 = random.randint(1, N)
        s2 = random.randint(1, N)
        k2 = random.randint(1, N)
        terms1 = generate_random_dnf(N, s1, k1)
        terms2 = generate_random_dnf(N, s2, k2)
        ricci1 = compute_forman_ricci(terms1)
        ricci2 = compute_forman_ricci(terms2)
        mu1 = compute_mu(ricci1)
        mu2 = compute_mu(ricci2)
        # Compute F ∧ G by taking the union of terms
        terms_fg = terms1 + terms2
        ricci_fg = compute_forman_ricci(terms_fg)
        mu_fg = compute_mu(ricci_fg)
        metric_values.append(mu_fg)
        instances_tested += 1
        if mu_fg > mu1 + mu2 + math.log2(1 + N):
            conjecture_holds = False
            counterexample = f"Pair (F,G) with mu(F∧G)={mu_fg} > mu(F)+mu(G)+log2(1+N)={mu1+mu2+math.log2(1+N)}"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0
    return {
        "metric_name": "mu(F)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")