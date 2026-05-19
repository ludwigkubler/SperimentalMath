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
        edges = set()
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in edges and (j, i) not in edges:
                    edges.add((i, j))
        return edges
    
    def dnf_size(edges):
        n = len(edges)
        size = 0
        for i in range(1 << n):
            clause = True
            for j in range(n):
                if i & (1 << j) and (j, j + 1) not in edges:
                    clause = False
                    break
            if clause:
                size += 1
        return size
    
    def log_size(size):
        if size == 0:
            return -math.inf
        return math.log2(size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        k = random.randint(2, min(n // 2, 5))
        edges = generate_k_clique(n, k)
        dnf_size_A = dnf_size(edges)
        dnf_size_B = dnf_size(edges)  # Same DNF for simplicity
        log_dnf_size_A = log_size(dnf_size_A)
        log_dnf_size_B = log_size(dnf_size_B)
        log_dnf_size_AB = log_size(dnf_size_A + dnf_size_B)
        
        results.append({
            "n": n,
            "k": k,
            "dnf_size_A": dnf_size_A,
            "dnf_size_B": dnf_size_B,
            "log_dnf_size_A": log_dnf_size_A,
            "log_dnf_size_B": log_dnf_size_B,
            "log_dnf_size_AB": log_dnf_size_AB
        })
    
    total_dnf_size = sum(r["dnf_size_A"] for r in results)
    mean_dnf_size = total_dnf_size / len(results)
    
    if mean_dnf_size < 10:
        return {
            "metric_name": "mean_dnf_size",
            "metric_value": mean_dnf_size,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mean_dnf_size is too small"
        }
    
    conjecture_holds = all(r["log_dnf_size_AB"] <= r["log_dnf_size_A"] + r["log_dnf_size_B"] for r in results)
    counterexample = "" if conjecture_holds else "submodularity_violation"
    
    return {
        "metric_name": "mean_dnf_size",
        "metric_value": mean_dnf_size,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_dnf_size) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"submodularity_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")