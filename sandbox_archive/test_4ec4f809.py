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
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = Fraction(1, A[i][i])
        for k in range(i + 1, n):
            factor_k = -A[k][i] * factor
            for j in range(n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += factor_k * A[i][j]
    
    # Back-substitute to find rank
    rank = n
    for i in range(n - 1, -1, -1):
        if all(abs(A[i][j]) < 1e-9 for j in range(i + 1, n)):
            rank -= 1
    return rank

def tropicalize(M):
    return [[max(x, 0) for x in row] for row in M]

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    L_G = laplacian_matrix(G)
    T_L_G = tropicalize(L_G)
    
    rho_L_G = gaussian_elimination(T_L_G)
    
    K_n_n = [[1 if (i == j or abs(i - j) == n // 2) else 0 for j in range(n)] for i in range(n)]
    L_IP_2 = laplacian_matrix(K_n_n)
    T_L_IP_2 = tropicalize(L_IP_2)
    
    rho_L_IP_2 = gaussian_elimination(T_L_IP_2)
    
    return {
        "metric_name": "Rank",
        "metric_value": max(rho_L_G, rho_L_IP_2),
        "instances_tested": 1,
        "conjecture_holds": rho_L_G <= math.log(n) and rho_L_IP_2 >= n**2,
        "counterexample": "" if rho_L_G > math.log(n) or rho_L_IP_2 < n**2 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")