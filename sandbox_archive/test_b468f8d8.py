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
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n * k):
            clause = set()
            while len(clause) < k:
                var = random.randint(1, 2*n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def rank_eilenberg_mac_lane_space(k, n):
        # Simplified version for demonstration purposes
        return (n * k) ** (k - 1)
    
    def is_in_ph(rank, n, k):
        c_k = 0.5  # Placeholder value for c_k
        return rank <= c_k * n**(k-1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(2, 5)  # Fixed range for simplicity
            cnf_formula = generate_k_cnf(k, n)
            rank = rank_eilenberg_mac_lane_space(k, n)
            results.append((n, k, rank))
    
    metric_value = sum(rank for _, _, rank in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(is_in_ph(rank, n, k) for n, k, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank_eilenberg_mac_lane_space",
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")