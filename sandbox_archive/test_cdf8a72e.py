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

def generate_dnf(n, m, max_term_size):
    terms = []
    for _ in range(m):
        term_size = random.randint(2, min(max_term_size, n))
        term = random.sample(range(n), term_size)
        terms.append(term)
    return terms

def build_co_occurrence_graph(terms):
    graph = defaultdict(set)
    for term in terms:
        for u, v in itertools.combinations(term, 2):
            graph[u].add(v)
            graph[v].add(u)
    return graph

def max_matching(graph):
    def find_augmenting_path(graph, matching, start):
        visited = set()
        stack = [(start, None)]
        while stack:
            node, parent = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if neighbor not in matching:
                    return [neighbor, node]
                else:
                    stack.append((matching[neighbor], neighbor))
        return None

    matching = {}
    for node in graph:
        if node not in matching:
            path = find_augmenting_path(graph, matching, node)
            if path:
                for i in range(0, len(path), 2):
                    matching[path[i]] = path[i+1]
                    matching[path[i+1]] = path[i]
    return len(matching) // 2

def compute_mu(terms):
    if not terms:
        return 0.0
    graph = build_co_occurrence_graph(terms)
    match_size = max_matching(graph)
    m = len(terms)
    denominator = math.ceil(math.log2(1 + m))
    if denominator == 0:
        return 0.0
    return match_size / denominator

def generate_dnf_pair(n, seed):
    random.seed(seed)
    m = int(n ** 1.5)
    max_term_size = 2 * math.log2(n)
    terms1 = generate_dnf(n, m, max_term_size)
    terms2 = generate_dnf(n, m, max_term_size)
    return terms1, terms2

def expand_dnf_conjunction(terms1, terms2):
    expanded_terms = []
    for t1 in terms1:
        for t2 in terms2:
            expanded_term = list(set(t1) | set(t2))
            expanded_terms.append(expanded_term)
    return expanded_terms

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 25, 36]
    v_values = [6, 8, 10, 12, 14]

    # Test (i): Subadditivity
    n = 12
    terms1, terms2 = generate_dnf_pair(n, seed)
    expanded_terms = expand_dnf_conjunction(terms1, terms2)
    mu_fg = compute_mu(expanded_terms)
    mu_f = compute_mu(terms1)
    mu_g = compute_mu(terms2)
    subadditivity_holds = mu_fg <= mu_f + mu_g

    # Test (ii): μ(F) ≤ 4 for log-width DNFs
    log_width_holds = True
    for n in n_values:
        m = int(n ** 1.5)
        max_term_size = 2 * math.log2(n)
        terms = generate_dnf(n, m, max_term_size)
        mu = compute_mu(terms)
        if mu > 4:
            log_width_holds = False
            break

    # Test (iii): μ(F_{v,k}) ≥ v/(2*(log2 v)^2) for k-CLIQUE DNFs
    k_clique_holds = True
    for v in v_values:
        k = math.floor(math.log2(v))
        n = v * (v - 1) // 2
        terms = []
        for i in range(v):
            for j in range(i + 1, v):
                term = [i * v + j for i, j in itertools.combinations(range(v), k + 1)]
                terms.append(term)
        mu = compute_mu(terms)
        lower_bound = v / (2 * (math.log2(v) ** 2))
        if mu < lower_bound:
            k_clique_holds = False
            break

    conjecture_holds = subadditivity_holds and log_width_holds and k_clique_holds
    counterexample = ""
    if not subadditivity_holds:
        counterexample = f"Subadditivity failed for n={n}"
    elif not log_width_holds:
        counterexample = f"Log-width bound failed for n={n}"
    elif not k_clique_holds:
        counterexample = f"k-CLIQUE lower bound failed for v={v}"

    return {
        "metric_name": "mu",
        "metric_value": mu_fg if subadditivity_holds else 0.0,
        "instances_tested": len(n_values) + len(v_values) + 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 31))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        mean = sum(metric_values) / len(metric_values) if metric_values else 0.0
        std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")