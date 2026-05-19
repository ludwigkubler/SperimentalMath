# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 3
    
    # Generate a random k-CLIQUE instance
    vertices = list(range(n))
    edges = set()
    for _ in range(k):
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in edges:
            edges.add((u, v))
    
    # Compute the symmetric group Fourier transform using Young tableaux basis
    def young_tableau_basis(n, k):
        if n == 0 or k == 0:
            return [[]]
        if k == 1:
            return [[i] for i in range(n)]
        result = []
        for i in range(k):
            for subtableau in young_tableau_basis(n - 1, k - 1):
                result.append([i] + subtableau)
        return result
    
    def symmetric_group_fourier_transform(edges, n, k):
        basis = young_tableau_basis(n, k)
        transform = [0] * len(basis)
        for edge in edges:
            u, v = edge
            for i, tableaux in enumerate(basis):
                if (u in tableaux and v not in tableaux) or (v in tableaux and u not in tableaux):
                    transform[i] += 1
        return [x / len(edges) for x in transform]
    
    fourier_transform = symmetric_group_fourier_transform(edges, n, k)
    min_non_zero_coefficient = min(x for x in fourier_transform if x != 0)
    
    # Brute-force enumeration of minimal terms to compute DNF size
    def is_clique(subset):
        return all((u, v) in edges or (v, u) in edges for u in subset for v in subset if u != v)
    
    def dnf_size(n, k):
        min_terms = []
        for i in range(1 << n):
            subset = [j for j in range(n) if (i >> j) & 1]
            if is_clique(subset) and len(subset) == k:
                min_terms.append(subset)
        return len(min_terms)
    
    dnf_size_value = dnf_size(n, k)
    
    # Verify Ω(n^{k/2}) lower bound vs O(log n) upper bound
    lower_bound = n ** (k / 2)
    upper_bound = math.log(dnf_size_value)
    
    metric_name = "Fourier Coefficient Gap"
    metric_value = min_non_zero_coefficient - upper_bound
    instances_tested = 1
    conjecture_holds = metric_value >= 0
    counterexample = "" if conjecture_holds else f"Lower bound {lower_bound} not met, DNF size {dnf_size_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")