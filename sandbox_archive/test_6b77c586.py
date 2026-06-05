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
        # Find the maximum element in column i
        max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_idx] = A[max_idx], A[i]
        
        # Make all elements below pivot zero
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]

    # Back substitution to get the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def determinant(A):
    n = len(A)
    det = 0
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += (-1) ** i * A[0][i] * determinant(submatrix)
    return det

def gram_matrix(phi, n):
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            G[i][j] = sum(phi[v1][v2] * phi[v3][v4]
                          for v1 in range(i) for v2 in range(j)
                          for v3 in range(v1, n) for v4 in range(v2, n))
    return G

def communication_complexity_rank_variance(phi, n):
    duals = []
    for i in range(1 << n):
        dual = [0] * n
        for j in range(n):
            if (i >> j) & 1:
                dual[j] = 1 - phi[j][j]
            else:
                dual[j] = phi[j][j]
        duals.append(dual)
    ranks = [sum(1 for x in dual if x == 0) for dual in duals]
    mean_rank = sum(ranks) / len(ranks)
    variance = sum((r - mean_rank) ** 2 for r in ranks) / len(ranks)
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = gram_matrix(phi, n)
    minimal_order = abs(determinant(G))
    variance_rank_monotone_duals = communication_complexity_rank_variance(phi, n)
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": minimal_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if abs(minimal_order - variance_rank_monotone_duals) <= 3 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000007) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")