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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_k_cliques(v, k):
    cliques = set()
    edges = list(range(1, v))
    for i in range(k):
        clique = set(random.sample(edges, 2))
        cliques.add(frozenset(clique))
    return cliques

def bin_pairs_by_intersection(cliques):
    orbit_count = {}
    for a in cliques:
        for b in cliques:
            if a < b:  # Ensure each pair is counted only once
                intersection_size = len(a & b)
                if intersection_size not in orbit_count:
                    orbit_count[intersection_size] = []
                orbit_count[intersection_size].append((a, b))
    return orbit_count

def forman_ricci_curvature(w_a, w_b, w_ab, n):
    term1 = sum(w_a / math.sqrt(w_ab * w_f) for f in range(1, w_a))
    term2 = sum(w_b / math.sqrt(w_ab * w_f) for f in range(1, w_b))
    return w_a + w_b - term1 - term2

def estimate_mu(v, k):
    cliques = generate_k_cliques(v, k)
    orbit_count = bin_pairs_by_intersection(cliques)
    
    mu = 0
    total_orbit_weight = 0
    for j, pairs in orbit_count.items():
        O_j = len(pairs) * math.comb(v, k) * math.comb(k, j) * math.comb(v - k, k - j) / 2
        F_j = forman_ricci_curvature(j + 1, j + 1, j + 1, 1)
        mu += O_j * F_j
        total_orbit_weight += O_j
    
    return mu / total_orbit_weight

def run_trial(seed: int) -> dict:
    random.seed(seed)
    v_values = [10, 16, 20, 24, 30, 40]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        mu = estimate_mu(v, k)
        
        if mu < v / 4:
            return {
                "metric_name": "mu",
                "metric_value": mu,
                "instances_tested": 1,
                "n_max": k,
                "conjecture_holds": False,
                "counterexample": f"v={v}, mu={mu} < v/4"
            }
        
        gap = mu - v / 4
        results.append((gap, k))
    
    mean_gap = sum(gap for gap, _ in results) / len(results)
    std_gap = math.sqrt(sum((gap - mean_gap) ** 2 for gap, _ in results) / len(results))
    support_fraction = all(0.05 * k <= gap / k <= 5 for _, k in results)
    
    return {
        "metric_name": "mu",
        "metric_value": mean_gap,
        "instances_tested": len(v_values),
        "n_max": max(k for _, k in results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")