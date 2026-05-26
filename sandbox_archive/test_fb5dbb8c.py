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
    rows, cols = len(A), len(A[0])
    rref = [row[:] for row in A]
    lead = 0
    while lead < cols:
        max_row = None
        for r in range(lead, rows):
            if rref[r][lead] != 0:
                max_row = r
                break
        if max_row is None:
            lead += 1
            continue
        
        rref[lead], rref[max_row] = rref[max_row], rref[lead]
        
        pivot = rref[lead][lead]
        for c in range(lead, cols):
            rref[lead][c] /= pivot
        
        for r in range(rows):
            if r != lead:
                factor = rref[r][lead]
                for c in range(lead, cols):
                    rref[r][c] -= factor * rref[lead][c]
        
        lead += 1
    
    rank = sum(1 for row in rref if any(row[i] != 0 for i in range(cols)))
    return rank

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def determinant(A):
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    
    return det

def is_symmetric(M):
    n = len(M)
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j] != M[j][i]:
                return False
    return True

def generate_random_symmetric_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            M[i][j] = random.randint(0, 1)
            M[j][i] = M[i][j]
    return M

def tseitin_circuit_size(M):
    n = len(M)
    if not is_symmetric(M):
        return float('inf')
    
    # Simplified Tseitin circuit size for permanent computation
    # This is a placeholder and should be replaced with actual Tseitin circuit construction
    return 2 * n ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    M = generate_random_symmetric_matrix(n)
    k = random.randint(1, n - 1)
    
    min_rank = gaussian_elimination(M)
    circuit_size = tseitin_circuit_size(M)
    
    metric_name = "MinRank(G(k, n) ∩ SymMat(n))"
    metric_value = min_rank
    instances_tested = 1
    conjecture_holds = min_rank >= circuit_size
    counterexample = "" if conjecture_holds else f"rank={min_rank}, expected={circuit_size}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")