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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_algebraic_variety(f):
        # Simplified representation of algebraic variety computation
        return sum(f[i] * (1 << i) for i in range(len(f)))
    
    def hodge_decomposition_dimension(variety):
        # Simplified Hodge decomposition dimension calculation
        return int(math.log2(variety + 1))
    
    def communication_complexity_matrix_rank(f):
        # Simplified communication complexity matrix rank calculation
        n = len(f)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                M[i][j] = f[i] ^ f[j]
                M[j][i] = M[i][j]
        rank = 0
        for row in M:
            if any(row):
                rank += 1
        return rank
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        variety = compute_algebraic_variety(f)
        dim_hodge = hodge_decomposition_dimension(variety)
        rank_comm = communication_complexity_matrix_rank(f)
        results.append((n, rank_comm, dim_hodge))
    
    if not all(results):
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [rank for _, rank, _ in results]
    dims = [dim for _, _, dim in results]
    corr_coeff = pearson_correlation_coefficient(ranks, dims)
    
    max_diff = max(abs(rank - dim) for rank, dim in zip(ranks, dims))
    conjecture_holds = corr_coeff >= 0.8 and max_diff <= 3
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_diff={max_diff}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_diff_exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")