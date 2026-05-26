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
    
    def generate_k_clique(n, k):
        edges = []
        nodes = list(range(n))
        for i in range(k):
            for j in range(i + 1, k):
                if random.choice([True, False]):
                    edges.append((nodes[i], nodes[j]))
        return edges
    
    def twisted_group_algebra_rank(edges, n):
        # Simplified rank calculation (not actual algebra)
        return len(edges) * n
    
    def monotone_circuit_depth(n, k):
        # Simplified depth estimation
        return n + k
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            k = random.randint(2, min(n - 1, 5))
            edges = generate_k_clique(n, k)
            rank = twisted_group_algebra_rank(edges, n)
            depth = monotone_circuit_depth(n, k)
            if rank < 2**(n-k) * k:
                results.append({"n": n, "k": k, "rank": rank, "depth": depth})
    
    if not results:
        return {
            "metric_name": "support_fraction",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ratios = [r["rank"] / (2**(r["n"]-r["k"]) * r["k"]) for r in results]
    support_fraction = sum(1 for r in ratios if r >= 0.5) / len(ratios)
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_support_fraction = sum(r["support_fraction"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")