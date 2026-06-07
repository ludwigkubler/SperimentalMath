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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        S = [(i >> j) & 1 for i in range(2**n) for j in range(n)]
        M = [[f(S[i] ^ S[j]) for j in range(n)] for i in range(n)]
        return M
    
    def geometric_fluctuation(M):
        n = len(M)
        total = sum(sum(row) for row in M)
        mean = total / (n * n)
        variance = sum((M[i][j] - mean)**2 for i in range(n) for j in range(n)) / (n * n)
        return math.sqrt(variance)
    
    def rank(M):
        n = len(M)
        A = [row[:] for row in M]
        pivot_row, pivot_col = 0, 0
        while pivot_row < n and pivot_col < n:
            if A[pivot_row][pivot_col] == 0:
                found_nonzero = False
                for i in range(pivot_row + 1, n):
                    if A[i][pivot_col] != 0:
                        found_nonzero = True
                        A[pivot_row], A[i] = A[i], A[pivot_row]
                        break
                if not found_nonzero:
                    pivot_col += 1
                    continue
            for i in range(n):
                if i != pivot_row and A[i][pivot_col] != 0:
                    factor = A[i][pivot_col] / A[pivot_row][pivot_col]
                    for j in range(n):
                        A[i][j] -= factor * A[pivot_row][j]
            pivot_row += 1
            pivot_col += 1
        rank = sum(1 for row in A if any(row))
        return rank
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        M = matrix_representation(f, n)
        G_f = geometric_fluctuation(M)
        rank_f = rank(M)
        results.append((G_f, rank_f))
    
    if len(results) < 10:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n for _, _ in results)),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    G_f_values = [x for x, _ in results]
    rank_f_values = [y for _, y in results]
    corr_coeff = correlation(G_f_values, rank_f_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n for _, _ in results)),
        "conjecture_holds": corr_coeff > 0.9,
        "counterexample": "" if corr_coeff >= 0.9 else f"correlation_coefficient={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in result for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")