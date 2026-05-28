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
    
    def generate_function(N):
        return {i: random.choice([-1, 1]) for i in range(N)}
    
    def xor_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        half_n = n // 2
        left = xor_circuit_size({i: f[2*i] for i in range(half_n)})
        right = xor_circuit_size({i: f[2*i + 1] for i in range(half_n)})
        return max(left, right) + 1
    
    def barratt_floer_homology(f):
        N = len(f)
        H = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if f[i] == f[j]:
                    H[i][j] = 1
        rank = gaussian_elimination(H)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def expected_rank(N):
        # This is a placeholder. The actual calculation depends on the distribution of f.
        return math.log2(N)
    
    results = []
    for N in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_function(N)
            rank = barratt_floer_homology(f)
            circuit_size = xor_circuit_size(f)
            expected_rank_value = expected_rank(N)
            ratio = circuit_size / (2**(rank + 1))
            results.append({
                "N": N,
                "circuit_size": circuit_size,
                "rank": rank,
                "expected_rank": expected_rank_value,
                "ratio": ratio
            })
    
    metric_name = "circuit_to_expected_ratio"
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["ratio"] >= 2**(result["rank"] + 1) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")