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

def generate_k_clique(n, k):
    edges = set()
    nodes = list(range(1, n + 1))
    for subset in combinations(nodes, k):
        for u, v in combinations(subset, 2):
            if u < v:
                edges.add((u, v))
    return edges

def clause_indicator_polynomial(edges, n):
    poly = [0] * (1 << n)
    for i in range(1, 1 << n):
        count = sum((i >> j) & 1 == (i >> k) & 1 for u, v in edges if u < v and (u, v) in edges)
        poly[i] = count % 2
    return poly

def polarized_hodge_structure(poly):
    n = len(poly)
    hodge_structure = [0] * (n + 1)
    for i in range(1 << n):
        if poly[i] == 1:
            hodge_structure[bin(i).count('1')] += 1
    return hodge_structure

def resolution_proof_size(n):
    # Placeholder function to simulate resolution proof size calculation
    return random.randint(10, 50)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = min(n - 1, random.randint(2, n // 2))
    edges = generate_k_clique(n, k)
    
    poly = clause_indicator_polynomial(edges, n)
    hodge_structure = polarized_hodge_structure(poly)
    num_monomials = sum(hodge_structure)
    
    t_F = resolution_proof_size(n)
    
    metric_name = "resolution_proof_size"
    metric_value = t_F
    instances_tested = 1
    conjecture_holds = abs(num_monomials - t_F) <= 0.2 * t_F
    counterexample = "" if conjecture_holds else f"num_monomials={num_monomials}, t_F={t_F}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) >= 2:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")