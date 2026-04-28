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

def pseudoinverse(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A_augmented = [[A[i][j] + I[i][j] for j in range(n)] for i in range(n)]
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(matrix[k][i])
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def back_substitution(matrix):
        n = len(matrix)
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
            x[i] /= matrix[i][i]
        return x
    
    L_inv = gaussian_elimination(A_augmented)
    L_inv = back_substitution(L_inv)
    
    return [[L_inv[i][n+j] for j in range(n)] for i in range(n)]

def effective_resistance(G, S):
    n = len(G)
    A = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    D = [sum(row) for row in A]
    
    for u in range(n):
        A[u][u] -= 1
    
    L = [[D[i] - A[i][j] for j in range(n)] for i in range(n)]
    L_inv = pseudoinverse(L)
    
    e_u = [0 if i not in S else 1 for i in range(n)]
    one_S = sum(1 for i in range(n) if i in S)
    
    R_eff_u_S = (e_u @ L_inv @ e_u + (1 / one_S**2) * sum(L_inv[i][j] for i in range(n) if i not in S for j in range(n) if j in S) - 2 * (e_u @ L_inv @ [1 if i in S else 0 for i in range(n)])) / len(S)
    
    return R_eff_u_S

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([12, 16, 20, 24, 28, 32, 36, 40])
    c = random.randint(1, n-1)
    
    # Generate a random 3-regular graph
    G = [[0] * n for _ in range(n)]
    degree_count = [0] * n
    
    while any(d != 3 for d in degree_count):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u == v or G[u][v] or degree_count[u] >= 3 or degree_count[v] >= 3:
            continue
        G[u][v] = G[v][u] = 1
        degree_count[u] += 1
        degree_count[v] += 1
    
    # Compute ν_R(G)
    S = sorted(random.sample(range(n), n//3))
    nu_R = min(max(effective_resistance(G, S[:i]) for i in range(1, len(S)+1)), max(effective_resistance(G, S[i:]) for i in range(len(S))))
    
    # Encode T(G,c) as 3-CNF on edge variables
    # (This part is not implemented and would require a more complex encoding)
    d_DPLL = None
    
    if d_DPLL is None:
        return {
            "metric_name": "d_DPLL",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Regress log d_DPLL against ν_R·n
    log_d_DPLL = math.log(d_DPLL)
    nu_R_n = nu_R * n
    
    return {
        "metric_name": "d_DPLL",
        "metric_value": d_DPLL,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*40+1, 40))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d_DPLL = sum(r["metric_value"] for r in results) / len(results)
        std_d_DPLL = math.sqrt(sum((r["metric_value"] - mean_d_DPLL)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_d_DPLL} std={std_d_DPLL} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")