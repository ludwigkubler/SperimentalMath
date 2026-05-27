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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def rank(A):
    n, m = len(A), len(A[0])
    A_augmented = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(A)]
    _, b = gaussian_elimination(A_augmented, [0] * n)
    return sum(1 for x in b if x != 0)

def generate_k_clique_cnf(n, k):
    variables = list(range(n))
    clauses = []
    for subset in itertools.combinations(variables, k):
        clause = [-x-1 for x in subset]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [30, 35, 40]
    results = []
    
    for n in n_values:
        k = min(n // 2, 5)  # Ensure k is at least 1
        cnf = generate_k_clique_cnf(n, k)
        
        rank_sum = 0
        expected_rank = sum(2**i for i in range(k))
        
        for _ in range(30):
            A = [[0] * n for _ in range(n)]
            b = [0] * n
            
            for clause in cnf:
                for x in clause:
                    if x > 0:
                        A[x-1][x-1] += 1
                    else:
                        A[-x-1][-x-1] += 1
            
            rank_sum += rank(A)
        
        mean_rank = rank_sum / 30
        results.append({
            "n": n,
            "rank": mean_rank,
            "expected_rank": expected_rank
        })
    
    correlation_coefficient = (sum((result["rank"] - sum(result["rank"] for result in results) / len(results)) * 
                                   (result["rank"] - sum(result["expected_rank"] for result in results) / len(results)) 
                                   for result in results) /
                              sum((result["rank"] - sum(result["rank"] for result in results) / len(results))**2 
                                  for result in results))
    
    if correlation_coefficient >= 0.8:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_d = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_d)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")