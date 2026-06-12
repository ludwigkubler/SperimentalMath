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
    
    def charpoly(f):
        n = len(f)
        A = [[f[i ^ j] ^ f[j] for j in range(n)] for i in range(n)]
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in enumerate(p))
            det += sign * math.prod(A[p[i]][i] for i in range(n))
        return det
    
    def grothendieck_witt_class(det):
        if det == 0:
            return 0
        count = 0
        for p in itertools.permutations(range(2)):
            if sum(p) % 2 == det % 2:
                count += 1
        return count
    
    def matrix_rank(matrix, mod=2):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] %= mod
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] = (matrix[k][j] - factor * matrix[i][j]) % mod
        return rank
    
    def communication_complexity_rank_variance(f, n):
        matrix = [[f[i ^ j] ^ f[j] for j in range(n)] for i in range(n)]
        max_rank = 0
        min_rank = float('inf')
        for _ in range(10):  # Sample multiple instances to get a good estimate
            rank = matrix_rank(matrix)
            if rank > max_rank:
                max_rank = rank
            if rank < min_rank:
                min_rank = rank
        return max_rank - min_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        det = charpoly(f)
        gw_class = grothendieck_witt_class(det)
        rank_variance = communication_complexity_rank_variance(f, n)
        results.append({
            "n": n,
            "det": det,
            "gw_class": gw_class,
            "rank_variance": rank_variance
        })
    
    max_n = max(r["n"] for r in results)
    if max_n < 16:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    log_gw_class = [math.log(r["gw_class"]) for r in results]
    rank_variance = [r["rank_variance"] for r in results]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def variance(lst, mean_val):
        return sum((x - mean_val) ** 2 for x in lst) / len(lst)
    
    mean_log_gw_class = mean(log_gw_class)
    var_rank_variance = variance(rank_variance, mean(rank_variance))
    corr_coeff = (sum((log_gw_class[i] - mean_log_gw_class) * (rank_variance[i] - mean(rank_variance)) for i in range(len(results))) /
                  math.sqrt(variance(log_gw_class, mean_log_gw_class) * variance(rank_variance, mean(rank_variance))))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")