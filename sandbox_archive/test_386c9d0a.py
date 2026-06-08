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
    
    def communication_complexity_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0] * (1 << n) for _ in range(1 << n)]
        for x in range(1 << n):
            for y in range(1 << n):
                if f[x] == f[y]:
                    matrix[x][y] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        row_echelon_form = [row[:] for row in matrix]
        lead = 0
        for r in range(m):
            if lead >= n:
                break
            i = r
            while row_echelon_form[i][lead] == 0:
                i += 1
                if i == m:
                    i = r
                    lead += 1
                    if lead == n:
                        return r
            row_echelon_form[r], row_echelon_form[i] = row_echelon_form[i], row_echelon_form[r]
            for i in range(m):
                if i != r and row_echelon_form[i][lead] != 0:
                    factor = -row_echelon_form[i][lead] / row_echelon_form[r][lead]
                    for j in range(n):
                        row_echelon_form[i][j] += factor * row_echelon_form[r][j]
            lead += 1
        return r + 1
    
    def min_non_degenerate_representation_order(f):
        n = int(math.log2(len(f)))
        vector_space = [f[i:i+n] for i in range(0, len(f), n)]
        basis = []
        for v in vector_space:
            if all(all(v[j] == w[j] for j in range(n)) for w in basis):
                basis.append(v)
        return len(basis)
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        C = communication_complexity_matrix(f)
        sigma_min = min_non_degenerate_representation_order(f)
        rank_C = rank(C)
        results.append((n, sigma_min, rank_C))
    
    if len(results) < 30:
        return {
            "metric_name": "sigma_min / Var(Rank(C))",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    sigma_min_values = [sigma_min for _, sigma_min, _ in results]
    rank_C_values = [rank_C for _, _, rank_C in results]
    variance_rank_C = variance(rank_C_values)
    
    ratio = sum(sigma_min / variance_rank_C for sigma_min in sigma_min_values) / len(sigma_min_values)
    
    return {
        "metric_name": "sigma_min / Var(Rank(C))",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(ratio) <= 10 * n_values[-1],
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")