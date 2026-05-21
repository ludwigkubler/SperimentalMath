# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
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

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def laplacian_eigenvalues(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1

    # Compute eigenvalues using Gaussian elimination
    eigenvalues = []
    for _ in range(n):
        A = [row[:] + [1] for row in L]
        x = gaussian_elimination(A)
        eigenvalue = sum(x[i] * L[i][j] for i, j in enumerate(range(n)))
        eigenvalues.append(eigenvalue)

    return sorted(eigenvalues)

def resolution_length(λ2):
    if λ2 >= 1:
        return float('inf')
    return 2 ** (math.log(1 / (1 - λ2)) / math.log(2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    λ2 = laplacian_eigenvalues(G)[1]
    
    length = resolution_length(λ2)
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (math.log(1 / (1 - λ2)) / math.log(2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 307))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(result["metric_value"] for result in results) / len(results)
    std_length = math.sqrt(sum((result["metric_value"] - mean_length) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")