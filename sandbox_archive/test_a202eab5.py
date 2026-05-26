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
        # Generate a random function in P with read-twice branching program width n
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_random_function(n // 2)
            right = generate_random_function(n // 2)
            return [left[i] ^ right[i] for i in range(len(left))]
    
    def geometric_quantization_matrix(f):
        n = len(f)
        M = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    M[i][j] = 1
                else:
                    M[i][j] = -1
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(n):
                if j == i:
                    matrix[pivot_row][j] /= matrix[pivot_row][i]
                else:
                    matrix[pivot_row][j] -= matrix[pivot_row][i] * matrix[j][i]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        M = geometric_quantization_matrix(f)
        rank = min_rank(M)
        results.append({
            "n": n,
            "rank": rank
        })
    
    if len(results) < 30:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ranks = [result["rank"] for result in results]
    n_values = [result["n"] for result in results]
    
    def spearman_rank_correlation(ranks, n_values):
        rank_ranks = {x: i + 1 for i, x in enumerate(sorted(set(ranks)))}
        n_value_ranks = {x: i + 1 for i, x in enumerate(sorted(set(n_values)))}
        
        rank_diffs = [rank_ranks[r] - n_value_ranks[n] for r, n in zip(ranks, n_values)]
        n = len(rank_diffs)
        
        sum_rank_diffs_squared = sum(diff ** 2 for diff in rank_diffs)
        sum_rank_diffs_cubed = sum(diff ** 3 for diff in rank_diffs)
        sum_rank_diffs_fourth = sum(diff ** 4 for diff in rank_diffs)
        
        numerator = n * sum_rank_diffs_squared - sum(rank_diffs) ** 2
        denominator = (n * sum_rank_diffs_fourth - sum_rank_diffs_cubed ** 2) ** 0.5
        
        return numerator / denominator
    
    rho = spearman_rank_correlation(ranks, n_values)
    
    if rho > 0 and rho < 1:
        return {
            "metric_name": "min_rank",
            "metric_value": rho,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_rank",
            "metric_value": rho,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "rho_not_in_range"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho_not_in_range' first_failing_seed={first_failing_seed}")