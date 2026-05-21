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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def degree_matrix(edges, n):
        deg = [0] * n
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
            M[u][v] = 1
            M[v][u] = 1
        return M
    
    def laplacian_matrix(M):
        n = len(M)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = deg[i]
            for j in range(i + 1, n):
                L[i][j] = -M[i][j]
                L[j][i] = -M[i][j]
        return L
    
    def eigenvalues(M):
        n = len(M)
        if n == 0:
            return []
        
        # Gaussian elimination to find eigenvalues
        A = [row[:] for row in M]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i + 1, n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        eigenvals = [A[i][i] for i in range(n)]
        return eigenvals
    
    def sos_moment_matrix(edges, d):
        n = len(edges)
        M_d = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in edges:
            M_d[u][v] += 1
            M_d[v][u] += 1
        for i in range(n):
            M_d[i][i] += 2
        return M_d
    
    def integrality_gap(gap):
        return gap <= 0.878
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    L = laplacian_matrix(degree_matrix(edges, n))
    
    # Compute eigenvalues of the Laplacian matrix
    lambda_min_L = min(eigenvalues(L))
    
    # Compute SOS moment matrices and their eigenvalues
    sos_gaps = []
    for d in [2, 3, 4]:
        M_d = sos_moment_matrix(edges, d)
        lambda_min_M_d = min(eigenvalues(M_d))
        gap = 1 - lambda_min_M_d
        sos_gaps.append(gap)
    
    # Check the conjecture conditions
    conjecture_holds = all(lambda_min_L >= epsilon for epsilon in [0.878, 0.756, 0.634])
    counterexample = "" if conjecture_holds else "lambda_min_L < 0.878"
    
    return {
        "metric_name": "Integrality Gap",
        "metric_value": lambda_min_L,
        "instances_tested": len(sos_gaps),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"lambda_min_L < 0.878\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")