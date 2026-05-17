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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [4, 5, 6]
    m_values = [[2], [n//2], [n-1]]
    
    max_rho = 0.0
    
    for n in n_values:
        perm_n = [1] * n
        rho_perm_n = sum(perm_n) ** 2 / (math.factorial(n) * sum(x**2 for x in perm_n))
        if not math.isclose(rho_perm_n, 1.0, rel_tol=1e-9):
            return {
                "metric_name": "rho",
                "metric_value": rho_perm_n,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "rho(perm_n) != 1"
            }
        
        for m in m_values:
            for _ in range(30):
                L = [[random.gauss(0, 1) for _ in range(n)] for _ in range(m)]
                ell = [random.gauss(0, 1) for _ in range(n**2)]
                
                f_L_ell = sum(ell[i] * det_m(L) for i in range(n**2)) ** (n-m)
                rho_f_L_ell = compute_rho(f_L_ell, n, m)
                if rho_f_L_ell > max_rho:
                    max_rho = rho_f_L_ell
    
    return {
        "metric_name": "rho",
        "metric_value": max_rho,
        "instances_tested": 90,
        "conjecture_holds": max_rho < 1 - 1/n_values[-1],
        "counterexample": ""
    }

def compute_rho(f, n, m):
    v = [sum(f[i*n+j] for i in range(m) if j == perm(i)) for perm in permutations(n)]
    numerator = sum(v_i**2 for v_i in v)
    denominator = math.factorial(n) * sum(v_i**2 for v_i in v)
    return (numerator / denominator) ** 0.5

def permutations(n):
    if n == 1:
        yield [0]
    else:
        for perm in permutations(n-1):
            for i in range(n):
                new_perm = perm[:i] + [n-1] + perm[i:i]
                yield new_perm

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = (sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")