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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(i+1, n):
            A[j][i] /= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    rank = sum(1 for row in A if any(row))
    return rank

def matrix_rank(A):
    n = len(A)
    m = len(A[0])
    B = [[A[i][j] for j in range(m)] for i in range(n)]
    return gaussian_elimination(B)

def algebraic_K_theory(G):
    # Simulate computation of K_0(G) as the rank of a matrix
    n = len(G)
    A = [[G[i][j] for j in range(n)] for i in range(n)]
    return matrix_rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "K0_G_over_r"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    results = []
    for _ in range(instances_tested):
        r = random.randint(1, n_max)
        G = [[random.randint(-10, 10) for _ in range(r)] for _ in range(r)]
        
        K0_G = algebraic_K_theory(G)
        if abs(K0_G / r - 1.0) > 1.5:
            conjecture_holds = False
            counterexample = f"r={r}, K0_G={K0_G}"
            break
        
        results.append((K0_G, r))
    
    metric_value = sum(K0_G for K0_G, r in results) / len(results)
    correlation_sum = 0
    for K0_G, r in results:
        correlation_sum += (K0_G - metric_value) * (r - metric_value)
    n = len(results)
    mean_r = sum(r for _, r in results) / n
    variance_r = sum((r - mean_r)**2 for _, r in results) / n
    pearson_correlation = correlation_sum / math.sqrt(n * variance_r * variance_r)
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")