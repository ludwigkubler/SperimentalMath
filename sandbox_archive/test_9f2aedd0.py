# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
    return x

def degree_d_sos_moment_matrix(G, d):
    n = len(G)
    A = [[0] * (n*(d+1)) for _ in range(n*(d+1))]
    
    # Fill the matrix
    for i in range(n):
        for j in range(i, n):
            if G[i][j] == 1:
                for k in range(d+1):
                    A[i*(d+1) + k][j*(d+1) + (k-1)] = 1
                    A[j*(d+1) + k][i*(d+1) + (k-1)] = 1
    
    # Add identity matrix
    for i in range(n):
        A[i*(d+1) + d][i*(d+1) + d] = 1
    
    return A

def max_cut_instance(n):
    G = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if random.random() < 0.5:
            G[u][v] = G[v][u] = 1
    return G

def integrality_gap(G, d):
    # Placeholder for actual implementation
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    G = max_cut_instance(n)
    integrality_bound = 2.0  # Placeholder for Goemans-Williamson bound
    
    negative_eigenvalue_count = 0
    for d in range(1, 6):
        A = degree_d_sos_moment_matrix(G, d)
        try:
            gaussian_elimination(A)
            for row in A:
                if row[-1] < 0:
                    negative_eigenvalue_count += 1
        except ZeroDivisionError:
            return {
                "metric_name": "Negative Eigenvalue Count",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    integrality_gap_val = integrality_gap(G, d)
    if integrality_gap_val is not None and integrality_gap_val <= integrality_bound * 2:
        conjecture_holds = negative_eigenvalue_count <= math.log(n)
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "Negative Eigenvalue Count",
        "metric_value": negative_eigenvalue_count,
        "instances_tested": 5,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")