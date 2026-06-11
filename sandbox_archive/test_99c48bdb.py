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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            if factor == 0:
                continue
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def communication_complexity_rank_variance(G, n):
        matroid_matrix = [[0] * (n + 1) for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if G[u][v]:
                    matroid_matrix[u][v] = 1
                    matroid_matrix[v][u] = 1
        matroid_matrix[n][n] = 1
        return rank(matroid_matrix)

    def local_induction_dimension(G, n):
        ind_set = [0]
        for i in range(1, n):
            if G[0][i]:
                ind_set.append(i)
        return len(ind_set) - 1

    d = random.randint(2, 5)
    n = random.randint(5, 30)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        neighbors = random.sample(range(n), d)
        for j in neighbors:
            if i != j:
                G[i][j] = G[j][i] = 1

    lind_G = local_induction_dimension(G, n)
    rank_var_M_G = communication_complexity_rank_variance(G, n)

    if rank_var_M_G == 0:
        return {
            "metric_name": "lind(G)/rank_var(M_G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank_var_M_G is zero"
        }

    ratio = lind_G / rank_var_M_G
    return {
        "metric_name": "lind(G)/rank_var(M_G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 2 * mean_value for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] > 2 * mean_value)
        print(f"RESULT: FALSIFIED counterexample=\"lind(G)/rank_var(M_G) exceeds 2C\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")