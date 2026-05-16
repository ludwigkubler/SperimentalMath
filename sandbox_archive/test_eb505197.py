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

def generate_dnf(n, m, max_term_size, seed):
    random.seed(seed)
    terms = []
    for _ in range(m):
        term_size = random.randint(2, min(max_term_size, n))
        term = random.sample(range(1, n + 1), term_size)
        terms.append(term)
    return terms

def generate_dnf_pair(n, seed):
    random.seed(seed)
    m = int(n ** 1.5)
    max_term_size = 2 * math.ceil(math.log2(n))
    terms1 = generate_dnf(n, m, max_term_size, seed)
    terms2 = generate_dnf(n, m, max_term_size, seed + 1)
    return terms1, terms2

def build_co_occurrence_graph(terms):
    graph = defaultdict(set)
    for term in terms:
        for u, v in itertools.combinations(term, 2):
            graph[u].add(v)
            graph[v].add(u)
    return graph

def find_maximum_matching(graph):
    matching = {}
    for u in graph:
        if u not in matching:
            for v in graph[u]:
                if v not in matching:
                    matching[u] = v
                    matching[v] = u
                    break
    return len(matching) // 2

def compute_mu(terms):
    if not terms:
        return 0.0
    graph = build_co_occurrence_graph(terms)
    max_matching = find_maximum_matching(graph)
    m = len(terms)
    denominator = math.ceil(math.log2(1 + m))
    if denominator == 0:
        return 0.0
    return max_matching / denominator

def generate_canonical_k_clique_dnf(v, k):
    terms = []
    for edges in itertools.combinations(range(1, v + 1), k):
        term = []
        for i, j in itertools.combinations(edges, 2):
            term.append(i * v + j)
        terms.append(term)
    return terms

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 25, 36]
    v_values = [6, 8, 10, 12, 14]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    # Test (i): Subadditivity
    n = 12
    m = int(n ** 1.5)
    max_term_size = 2 * math.ceil(math.log2(n))
    terms1, terms2 = generate_dnf_pair(n, seed)
    expanded_terms = [list(set(t1) | set(t2)) for t1, t2 in itertools.product(terms1, terms2)]
    mu_fg = compute_mu(expanded_terms)
    mu_f = compute_mu(terms1)
    mu_g = compute_mu(terms2)
    if mu_fg > mu_f + mu_g:
        conjecture_holds = False
        counterexample = f"Subadditivity failed: mu(F∧G)={mu_fg} > mu(F)+mu(G)={mu_f + mu_g}"

    # Test (ii): Log-width bound
    for n in n_values:
        m = int(n ** 1.5)
        max_term_size = 2 * math.ceil(math.log2(n))
        terms = generate_dnf(n, m, max_term_size, seed)
        mu = compute_mu(terms)
        if mu > 4:
            conjecture_holds = False
            counterexample = f"Log-width bound failed: mu={mu} > 4 for n={n}"

    # Test (iii): k-CLIQUE bound
    for v in v_values:
        k = math.floor(math.log2(v))
        terms = generate_canonical_k_clique_dnf(v, k)
        mu = compute_mu(terms)
        lower_bound = v / (2 * (math.log2(v) ** 2))
        if mu < lower_bound:
            conjecture_holds = False
            counterexample = f"k-CLIQUE bound failed: mu={mu} < {lower_bound} for v={v}"

    return {
        "metric_name": "mu",
        "metric_value": mu_fg if conjecture_holds else 0.0,
        "instances_tested": len(n_values) + len(v_values) + 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [i for i in range(30)]
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