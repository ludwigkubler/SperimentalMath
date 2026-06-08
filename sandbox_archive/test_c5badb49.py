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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
            rank += 1
            for j in range(i + 1, m):
                if matrix[j][pivot_col] != 0:
                    factor = matrix[j][pivot_col] / matrix[i][pivot_col]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity_matrix(f, n):
        m = 2**n
        C = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if f[i ^ j] == 1:
                    C[i][j] += 1
        return C
    
    def min_non_degenerate_representation(f):
        n = int(math.log2(len(f)))
        V = [f[x.index(0)] for x in range(2**n)]
        rank = matrix_rank([V])
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        sigma_min = min_non_degenerate_representation(f)
        C = communication_complexity_matrix(f, n)
        rank_variance = variance([matrix_rank(row) for row in C])
        results.append({
            "n": n,
            "sigma_min": sigma_min,
            "rank_variance": rank_variance
        })
    
    mean_sigma_min = sum(result["sigma_min"] for result in results) / len(results)
    mean_rank_variance = sum(result["rank_variance"] for result in results) / len(results)
    ratio_mean = mean_sigma_min / mean_rank_variance
    
    return {
        "metric_name": "ratio_mean",
        "metric_value": ratio_mean,
        "instances_tested": len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": ratio_mean <= n ** 2,  # Polynomially bounded by n^2
        "counterexample": "" if ratio_mean <= n ** 2 else f"ratio_mean={ratio_mean} > {n**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio_mean = sum(result["metric_value"] for result in results) / len(results)
    std_ratio_mean = math.sqrt(sum((result["metric_value"] - mean_ratio_mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio_mean} std={std_ratio_mean} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_mean > n^2' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")