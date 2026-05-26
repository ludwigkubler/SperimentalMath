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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def tensor_product(f, g):
        n = len(f)
        m = len(g)
        result = []
        for i in range(2**(n+m)):
            bin_i = format(i, f'0{n+m}b')
            x, y = int(bin_i[:n], 2), int(bin_i[n:], 2)
            result.append(f[x] * g[y])
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def compute_brauer_group_rank(f, g):
        n = len(f)
        tensor_valuation = tensor_product(f, g)
        matrix = [[tensor_valuation[i * (2**n) + j] for i in range(2**n)] for j in range(2**n)]
        return gaussian_elimination(matrix)
    
    def spearman_correlation(ranks, expected):
        n = len(ranks)
        ranks_diff = [r - expected for r in ranks]
        ranks_diff_squared = [d**2 for d in ranks_diff]
        return 1 - (6 * sum(ranks_diff_squared)) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        f = generate_boolean_function(n)
        g = generate_boolean_function(n)
        rank = compute_brauer_group_rank(f, g)
        ranks.append(rank)
    
    expected_rank = [n**(2/3) for n in n_values]
    correlation_coefficient = spearman_correlation(ranks, expected_rank)
    
    metric_name = "Brauer Group Rank"
    metric_value = sum(ranks) / len(ranks)
    instances_tested = len(n_values)
    conjecture_holds = all(0.33 * n**(2/3) <= rank <= 3 * n**(2/3) for rank, n in zip(ranks, n_values)) and correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7 or rank out of bounds"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7 or rank out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")