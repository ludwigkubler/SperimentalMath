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
    variables = list(range(n))
    terms = []
    for _ in range(m):
        term_size = random.randint(2, min(max_term_size, n))
        term = random.sample(variables, term_size)
        terms.append(set(term))
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
                    path = [neighbor, node]
                    while parent is not None:
                        path.append(parent)
                        parent = matching.get(parent, None)
                    return path
                if matching[neighbor] not in visited:
                    stack.append((matching[neighbor], neighbor))
        return None

    matching = {}
    for node in graph:
        if node not in matching:
            path = find_augmenting_path(graph, matching, node)
            if path:
                for i in range(0, len(path) - 1, 2):
                    matching[path[i]] = path[i + 1]
                    matching[path[i + 1]] = path[i]
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

def generate_k_clique_dnf(v, k):
    variables = list(itertools.combinations(range(v), 2))
    terms = []
    for clique in itertools.combinations(range(v), k):
        term = set(itertools.combinations(clique, 2))
        terms.append(term)
    return terms

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 25, 36]
    v_values = [6, 8, 10, 12, 14]
    results = []

    # Test (i) and (ii)
    for n in n_values:
        m = int(n**1.5)
        max_term_size = 2 * math.log2(n)
        terms = generate_dnf(n, m, max_term_size)
        mu = compute_mu(terms)
        conjecture_holds = mu <= 4
        results.append({
            "metric_name": "mu",
            "metric_value": mu,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"mu={mu} > 4 for n={n}"
        })

    # Test (iii)
    for v in v_values:
        k = math.floor(math.log2(v))
        terms = generate_k_clique_dnf(v, k)
        mu = compute_mu(terms)
        lower_bound = v / (2 * (math.log2(v))**2)
        conjecture_holds = mu >= lower_bound
        results.append({
            "metric_name": "mu",
            "metric_value": mu,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"mu={mu} < {lower_bound} for v={v}"
        })

    # Test subadditivity
    n = 12
    m = int(n**1.5)
    max_term_size = 2 * math.log2(n)
    terms1 = generate_dnf(n, m, max_term_size)
    terms2 = generate_dnf(n, m, max_term_size)
    mu1 = compute_mu(terms1)
    mu2 = compute_mu(terms2)
    terms_conjunction = [t1.union(t2) for t1, t2 in itertools.product(terms1, terms2)]
    mu_conjunction = compute_mu(terms_conjunction)
    conjecture_holds = mu_conjunction <= mu1 + mu2
    results.append({
        "metric_name": "mu_conjunction",
        "metric_value": mu_conjunction,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mu_conjunction={mu_conjunction} > mu1+mu2={mu1+mu2} for n={n}"
    })

    # Aggregate results
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    return {
        "metric_name": "mu",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "",
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 31))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = seeds[results.index(next(r for r in results if not r["conjecture_holds"]))]
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")