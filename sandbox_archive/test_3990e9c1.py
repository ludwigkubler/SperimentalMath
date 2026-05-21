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

def generate_disjointness_matrix(n):
    if n <= 0:
        raise ValueError("n must be greater than 0")
    A = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**(n-1)):
        for j in range(i+1, 2**(n-1)):
            A[i][j] = 1
            A[j][i] = 1
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(M, b):
    n = len(M)
    M_b = [row + [b[i]] for i, row in enumerate(M)]
    
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        
        # Swap rows
        M_b[i], M_b[max_row] = M_b[max_row], M_b[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = M_b[j][i] / M_b[i][i]
            for k in range(n + 1):
                M_b[j][k] -= factor * M_b[i][k]
    
    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M_b[i][-1] / M_b[i][i]
        for j in range(i-1, -1, -1):
            M_b[j][-1] -= M_b[j][i] * x[i]
    
    return x

def rank_of_matrix(M):
    n = len(M)
    M_copy = [row[:] for row in M]
    rank = 0
    for i in range(n):
        if M_copy[i][i] != 0:
            rank += 1
            for j in range(i+1, n):
                factor = M_copy[j][i] / M_copy[i][i]
                for k in range(n):
                    M_copy[j][k] -= factor * M_copy[i][k]
        else:
            found_nonzero = False
            for j in range(i+1, n):
                if M_copy[j][i] != 0:
                    M_copy[i], M_copy[j] = M_copy[j], M_copy[i]
                    rank += 1
                    found_nonzero = True
                    break
            if not found_nonzero:
                continue
        
        for j in range(n):
            if j != i and M_copy[j][i] != 0:
                factor = M_copy[j][i] / M_copy[i][i]
                for k in range(n):
                    M_copy[j][k] -= factor * M_copy[i][k]
    
    return rank

def secant_variety_dimension(matrix, n):
    identity = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    A = matrix
    B = identity
    count = 0
    
    while True:
        C = matrix_multiplication(A, B)
        rank_C = rank_of_matrix(C)
        
        if rank_C == n:
            return count
        
        D = [[C[i][j] - A[i][j] for j in range(2**n)] for i in range(2**n)]
        E = [[C[i][j] - B[i][j] for j in range(2**n)] for i in range(2**n)]
        
        if rank_of_matrix(D) == n and rank_of_matrix(E) == n:
            count += 1
            A, B = C, identity
        else:
            break
    
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        try:
            A = generate_disjointness_matrix(n)
            secant_dim = secant_variety_dimension(A, n)
            
            if secant_dim < n:
                conjecture_holds = False
                counterexample = f"n={n}, secant dimension={secant_dim}"
                break
            
            total_metric_value += secant_dim
            instances_tested += 1
        except Exception as e:
            print(f"Exception in run_trial with seed {seed} and n={n}: {e}")
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results if result["instances_tested"] > 0)
    instances_tested = sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")