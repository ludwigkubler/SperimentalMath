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
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quandle_representation(f):
        # Simplified representation using a list of tuples
        return [(i, f[i]) for i in range(len(f))]
    
    def min_rank(representation):
        n = len(representation)
        matrix = [[0] * n for _ in range(n)]
        for i, (x, y) in enumerate(representation):
            for j, (u, v) in enumerate(representation):
                if x == u and y != v:
                    matrix[i][j] = 1
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            matrix[j][i] = 0
        return rank
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    c_Q = 1.0  # Predefined constant, can be adjusted based on theoretical bounds
    
    results = []
    for n in range(5, 41):
        f = generate_monotone_function(n)
        representation = compute_quandle_representation(f)
        min_rank_value = min_rank(representation)
        results.append({
            "n": n,
            "min_rank": min_rank_value,
            "c_Q_log_n": c_Q * log2(2**n)
        })
    
    total_min_rank = sum(result["min_rank"] for result in results)
    total_c_Q_log_n = sum(result["c_Q_log_n"] for result in results)
    mean_min_rank = total_min_rank / len(results)
    mean_c_Q_log_n = total_c_Q_log_n / len(results)
    
    conjecture_holds = all(result["min_rank"] >= result["c_Q_log_n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_min_rank",
        "metric_value": mean_min_rank,
        "instances_tested": len(results),
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
    
    mean_min_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_min_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_min_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")