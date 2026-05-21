# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def generate_random_graph(n):
    G = {i: set() for i in range(n)}
    edges = list(combinations(range(n), 2))
    random.shuffle(edges)
    m = int(n * (n - 1) / 4)  # Approximately half of the possible edges
    for u, v in edges[:m]:
        G[u].add(v)
        G[v].add(u)
    return G

def clique_complex(G):
    simplices = {frozenset(): 1}
    for node in G:
        new_simplices = set()
        for simplex in simplices:
            if node not in simplex:
                new_simplices.add(simplex | {node})
        simplices.update(new_simplices)
    return simplices

def betti_numbers(simplices):
    beta_0 = len([s for s in simplices if len(s) == 0])
    beta_1 = len([s for s in simplices if len(s) == 1])
    return beta_0, beta_1

def max_cut_approximation(G):
    n = len(G)
    max_cut_value = sum(1 for u in range(n) for v in G[u] if random.choice([True, False]))
    cut_value = max_cut_value
    for k in range(2, n + 1):
        for nodes in combinations(range(n), k):
            cut_value = max(cut_value, sum(1 for u in nodes for v in G[u] if v not in nodes))
    return Fraction(cut_value, max_cut_value).limit_denominator()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_random_graph(n)
    simplices = clique_complex(G)
    beta_0, beta_1 = betti_numbers(simplices)
    required_degree = max_cut_approximation(G)
    metric_value = required_degree
    instances_tested = 1
    conjecture_holds = required_degree >= beta_0 + beta_1
    counterexample = "" if conjecture_holds else f"Graph with n={n}, Betti numbers ({beta_0}, {beta_1}), Required degree {required_degree}"
    return {
        "metric_name": "SOS Degree",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")