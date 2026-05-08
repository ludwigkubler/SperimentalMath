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
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back-substitute to get upper triangular matrix
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            A[i][j] = 0
        
        # Normalize the diagonal element
        A[i][i] = 1 / A[i][i]
        
        # Eliminate above
        for j in range(i-1, -1, -1):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def max_cut(G, n):
    E = len(G)
    cuts = [0] * (1 << n)
    for mask in range(1 << n):
        cut_value = 0
        for u in range(n):
            if mask & (1 << u):
                for v in G[u]:
                    if not (mask & (1 << v)):
                        cut_value += 1
        cuts[mask] = cut_value
    return max(cuts)

def bonami_beckner_kurtosis(G, n, K=20000):
    A = [[G[i].count(j) for j in range(n)] for i in range(n)]
    E_g4 = 0
    E_g2 = 0
    for _ in range(K):
        x = [random.choice([-1, 1]) for _ in range(n)]
        g4 = sum(x[i] * A[i][j] * x[j] * A[j][i] for i in range(n) for j in range(i+1, n))
        g2 = sum(x[i] * A[i][j] * x[j] for i in range(n) for j in range(i+1, n))
        E_g4 += g4
        E_g2 += g2
    E_g4 /= K
    E_g2 /= K
    return (E_g4 / E_g2**2 - 3)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([10, 14, 18, 20])
    G = [[] for _ in range(n)]
    degrees = [3] * n
    while any(deg > 0 for deg in degrees):
        u = random.randint(0, n-1)
        if degrees[u] == 0:
            continue
        v = random.choice([i for i in range(n) if i != u and len(G[i]) < 3])
        G[u].append(v)
        G[v].append(u)
        degrees[u] -= 1
        degrees[v] -= 1
    
    n_edges = sum(len(neighbors) for neighbors in G) // 2
    max_cut_value = max_cut(G, n)
    A = [[G[i].count(j) for j in range(n)] for i in range(n)]
    DP_G = n_edges / 2 + n * min(eigenvalue.real for eigenvalue in gaussian_elimination(A).diagonal()) / 4
    κ_G = bonami_beckner_kurtosis(G, n)
    
    metric_value = (DP_G - max_cut_value) / n_edges
    conjecture_holds = metric_value <= 0.5 * max(κ_G, 1/n)**0.25
    
    return {
        "metric_name": "Goemans-Williamson integrality gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")