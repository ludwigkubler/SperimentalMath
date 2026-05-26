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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank

    def generate_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
        return bp

    def compute_k_theory_rank(bp):
        n = len(bp)
        A = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if bp[i] == bp[j]:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
            A[i][n] = 1
        return gaussian_elimination(A)

    def size(bp):
        return sum(1 for x in bp if x == 1)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            bp = generate_bp(n)
            rank = compute_k_theory_rank(bp)
            size_val = size(bp)
            if rank < log(size_val):
                return {
                    "metric_name": "rho_K(P)",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"bp={bp}, rank={rank}, size={size_val}"
                }
            results.append({"n": n, "rank": rank, "size": size_val})
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["rank"] <= log(result["size"])) / len(results)
    
    return {
        "metric_name": "rho_K(P)",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - math.log(result["instances_tested"])) > 3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - math.log(result["instances_tested"])) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"|rho_K(P) - log(size(P))| > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")