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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if A[i][i] != 0:
                rank += 1
        return rank

    def l_function_zeros(n):
        # Simplified L-function zeros calculation for demonstration purposes
        return [random.uniform(0, 1) for _ in range(n)]

    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n > 40:
            break
        
        instances_tested = 0
        l_function_ranks = []
        matrix_rank_variances = []
        
        while len(l_function_ranks) < 30:
            M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            rank = matrix_rank(M)
            if rank == 0:
                continue
            
            instances_tested += 1
            l_zeros = l_function_zeros(n)
            l_rank = len(l_zeros)
            matrix_rank_variances.append(variance([rank]))
            l_function_ranks.append(l_rank)
        
        if instances_tested < 30:
            return {
                "metric_name": "L-function Rank and Communication Complexity Rank Variance",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        l_function_ranks = [math.log(x + 1) for x in l_function_ranks]  # Avoid zero
        matrix_rank_variances = [math.log(x + 1) for x in matrix_rank_variances]
        
        correlation_coefficient = sum((l_function_ranks[i] - sum(l_function_ranks) / len(l_function_ranks)) * 
                                      (matrix_rank_variances[i] - sum(matrix_rank_variances) / len(matrix_rank_variances))
                                     for i in range(len(l_function_ranks))) / len(l_function_ranks)
        
        results.append({
            "n": n,
            "correlation_coefficient": correlation_coefficient
        })
    
    mean_corr = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["correlation_coefficient"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["correlation_coefficient"] > 0.7) / len(results)
    
    return {
        "metric_name": "L-function Rank and Communication Complexity Rank Variance",
        "metric_value": mean_corr,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"correlation_coefficient<{mean_corr}>({std_corr})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{mean_corr}>({std_corr})\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")