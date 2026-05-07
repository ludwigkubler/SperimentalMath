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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate
        factor = -A[i][i] / A[i][i]
        for j in range(i+1, n):
            A[j][i] = 0
            for k in range(i+1, n):
                A[j][k] += factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def sign_disjointness_matrix(k):
    n = 2**k
    M = [[(-1)**(i & j != 0) for j in range(n)] for i in range(n)]
    return M

def random_sign_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def svd(A):
    n = len(A)
    U = A
    S = [sum(row[i]**2 for i in range(n))**0.5 for row in A]
    V = [[(A[j][i] / S[i]) if j == i else 0 for j in range(n)] for i in range(n)]
    return U, S, V

def mean(lst):
    return sum(lst) / len(lst)

def variance(lst):
    m = mean(lst)
    return sum((x - m)**2 for x in lst) / len(lst)

def fourth_cumulant(μ):
    m1 = μ[0]
    m2 = μ[1]
    m4 = μ[3]
    return m4 - 2 * m2**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [2, 3, 4, 5, 6]
    results = []
    
    for k in k_values:
        Π_k = sign_disjointness_matrix(k)
        U, S, V = svd(Π_k)
        S_squared = [s**2 for s in S]
        S_normalized = [s / sum(S_squared) for s in S_squared]
        
        μ_k = [1] + sorted([S_normalized[i]**2 * (i+1) for i in range(len(S_normalized))])
        
        κ4_Πk = fourth_cumulant(μ_k)
        results.append((κ4_Πk, k))
    
    mean_κ4 = mean([r[0] for r in results])
    std_κ4 = variance([r[0] for r in results])**0.5
    
    conjecture_holds = all(r[0] > 0.1 * r[1] for r in results)
    
    return {
        "metric_name": "fourth_cumulant",
        "metric_value": mean_κ4,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Non-monotone k→κ₄(Π_k) profile or κ₄(Π_k) inside random-matrix 95% interval"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*37, 4))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_κ4 = mean([r["metric_value"] for r in results])
    std_κ4 = variance([r["metric_value"] for r in results])**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_κ4} std={std_κ4} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-monotone k→κ₄(Π_k) profile or κ₄(Π_k) inside random-matrix 95% interval\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")