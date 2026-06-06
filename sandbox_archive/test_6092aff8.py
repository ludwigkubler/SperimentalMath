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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_diophantine_equation_complexity(f):
        n = len(f)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = -1
        matrix[n][n] = 1
        return gaussian_elimination(matrix)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def compute_communication_rank_variance(f):
        n = len(f)
        rank_sum = 0
        for _ in range(30):  # Sample 30 random seeds for variance calculation
            f_sampled = generate_random_function(n)
            rank_sum += gaussian_elimination([row[:] for row in f_sampled])
        return (rank_sum / 30) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        c_g = compute_diophantine_equation_complexity(f)
        crv_f = compute_communication_rank_variance(f)
        if c_g > 10:
            return {
                "metric_name": "Diophantine Equation Complexity",
                "metric_value": c_g,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "c(g) > 10"
            }
        results.append((c_g, crv_f))
    
    if not results:
        return {
            "metric_name": "Diophantine Equation Complexity",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid results"
        }
    
    c_g_avg = sum(c for c, _ in results) / len(results)
    crv_f_avg = sum(r for _, r in results) / len(results)
    correlation_coefficient = (sum((c - c_g_avg) * (r - crv_f_avg) for c, r in results) /
                               math.sqrt(sum((c - c_g_avg) ** 2 for c, _ in results) *
                                         sum((r - crv_f_avg) ** 2 for _, r in results)))
    
    return {
        "metric_name": "Diophantine Equation Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")