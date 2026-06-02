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
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(A[i][i])
        for k in range(i+1, n):
            A[k][i] /= factor
        
        # Eliminate above
        for k in range(i):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    
    return [A[i][i] for i in range(n)]

def normalize_matrix(A):
    n = len(A)
    sum_of_squares = 0
    for row in A:
        for val in row:
            sum_of_squares += val ** 2
    
    norm_factor = math.sqrt(sum_of_squares) / n
    normalized_A = [[A[i][j] / norm_factor for j in range(n)] for i in range(n)]
    
    return normalized_A

def smallest_non_zero_eigenvalue_normalized(L):
    eigenvalues = gaussian_elimination(normalize_matrix(L))
    non_zero_eigenvalues = [eig for eig in eigenvalues if eig != 0]
    if not non_zero_eigenvalues:
        return None
    return min(non_zero_eigenvalues)

def communication_complexity_rank(G):
    degrees = [sum(1 for _ in neighbors) for _, neighbors in G.items()]
    return min(degrees)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * (n - 1) // 2 < len(results):
            continue
        
        # Generate a random communication complexity function
        G = {i: set() for i in range(n)}
        edges = random.sample(range(n * (n - 1)), min(n * (n - 1), 30))
        for u, v in edges:
            if u != v and u not in G[v]:
                G[u].add(v)
                G[v].add(u)
        
        # Compute the normalized Laplacian
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = len(G[i])
            L[i][i] = degree / n - 1 / n
            for j in G[i]:
                L[i][j] = 1 / n
        
        # Compute the communication complexity rank
        r_f = communication_complexity_rank(G)
        
        if r_f == 0:
            continue
        
        # Compute the ratio of the smallest non-zero eigenvalue to log(n)
        lambda_min = smallest_non_zero_eigenvalue_normalized(L)
        if lambda_min is None or lambda_min <= 0:
            continue
        
        results.append((lambda_min, math.log(r_f)))
    
    if not results:
        return {
            "metric_name": "Ratio of smallest non-zero eigenvalue to log(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lambda_min_avg = sum(result[0] for result in results) / len(results)
    log_r_f_avg = sum(result[1] for result in results) / len(results)
    correlation_coefficient = (sum((result[0] - lambda_min_avg) * (result[1] - log_r_f_avg) for result in results) /
                               math.sqrt(sum((result[0] - lambda_min_avg) ** 2 for result in results) *
                                         sum((result[1] - log_r_f_avg) ** 2 for result in results)))
    
    return {
        "metric_name": "Ratio of smallest non-zero eigenvalue to log(n)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5 * math.log(max(n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds if "conjecture_holds" in trial_result and trial_result["conjecture_holds"]]
    support_fraction = len(results) / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(trial['metric_value'] for trial in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(trial["conjecture_holds"] == False for trial in results):
        first_failing_seed = next(seed for seed, trial in enumerate(seeds) if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")