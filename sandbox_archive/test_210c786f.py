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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_matrix(G):
        n = len(G)
        D = [sum(1 for v in G[u]) for u in G]
        L = [[0] * n for _ in range(n)]
        for u in G:
            for v in G[u]:
                L[u][v] = -1
                L[v][u] = -1
            L[u][u] = D[u]
        return L

    def eigenvalues(matrix):
        n = len(matrix)
        if n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            det = a * d - b * c
            trace = a + d
            lambda1 = (trace + math.sqrt(trace**2 - 4 * det)) / 2
            lambda2 = (trace - math.sqrt(trace**2 - 4 * det)) / 2
            return [lambda1, lambda2]
        else:
            A = matrix.copy()
            for i in range(n):
                A[i][i] -= 1e-6
            identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            A_inv = gaussian_elimination(matrix_multiply(A, identity))
            lambda2 = sum(A_inv[i][i] for i in range(n)) / n
            return [lambda2]

    def tseitin_resolution_bound(lambda2):
        if lambda2 <= 0:
            return float('inf')
        return 2 ** (1 / lambda2)

    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    for _ in range(random.randint(int(n * (n - 1) / 4), int(n * (n - 1) / 2))):
        u, v = random.sample(range(n), 2)
        if v not in G[u]:
            G[u].add(v)
            G[v].add(u)

    L = laplacian_matrix(G)
    lambda_values = eigenvalues(L)
    lambda2 = min(lambda_values[1:]) if len(lambda_values) > 1 else float('inf')
    
    resolution_bound = tseitin_resolution_bound(lambda2)
    return {
        "metric_name": "Resolution Bound",
        "metric_value": resolution_bound,
        "instances_tested": 1,
        "conjecture_holds": resolution_bound >= 2 ** (0.5 / n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2 ** (0.5 / n)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 2 ** (0.5 / n) for r in results):
        counterexample = "Resolution bound does not scale exponentially with 1/lambda_2(G)"
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")