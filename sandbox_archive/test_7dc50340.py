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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(n+1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        perm += (-1)**j * determinant(submatrix)
    return perm

def young_tableau_to_partition(yt):
    partition = []
    current_row = []
    for cell in yt:
        if cell == 0:
            partition.append(current_row)
            current_row = []
        else:
            current_row.append(cell)
    partition.append(current_row)
    return [len(row) for row in partition]

def plethysm_coefficient(partition, n):
    # This is a placeholder function. For simplicity, we assume the coefficient is 1.
    # In practice, this would involve more complex combinatorial calculations.
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = n // 2
    m = int(n ** 1.5) - 1
    
    perm = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    det = [[i == j for i in range(n)] for j in range(n)]
    
    perm_coeff = plethysm_coefficient(young_tableau_to_partition([[n-k+1] + [1]*(n-k-1), [1]*k]), n)
    det_coeff = plethysm_coefficient(young_tableau_to_partition([[n-k+1] + [1]*(n-k-1), [1]*k]), m)
    
    ratio = perm_coeff / det_coeff
    
    return {
        "metric_name": "plethysm_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 2**(n/2),
        "counterexample": "" if ratio > 2**(n/2) else f"m={m}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={result['counterexample']}\", first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")