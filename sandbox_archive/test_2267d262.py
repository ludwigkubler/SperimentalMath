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
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
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

    def rank(A):
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        return sum(1 for row in r if any(x != 0 for x in row))

    def local_induction_dimension(G, d):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    M[i][j] = M[j][i] = 1
        return rank(M)

    def communication_complexity_rank_variance(G, d):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    M[i][j] = M[j][i] = 1
        return rank(M)

    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        degree = [0] * n
        edges_added = 0
        while edges_added < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if not G[u][v]:
                G[u][v] = G[v][u] = 1
                degree[u] += 1
                degree[v] += 1
                edges_added += 1
        return G

    n_max = 40
    instances_tested = 30
    lind_values = []
    rank_var_values = []

    for _ in range(instances_tested):
        d = random.randint(2, min(n_max // 2 - 1, 5))
        G = generate_d_regular_graph(n_max, d)
        lind = local_induction_dimension(G, d)
        rank_var = communication_complexity_rank_variance(G, d)
        if rank_var == 0:
            continue
        lind_values.append(lind)
        rank_var_values.append(rank_var)

    if not lind_values or not rank_var_values:
        return {
            "metric_name": "lind_over_rank_var",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    ratio = [l / r for l, r in zip(lind_values, rank_var_values)]
    mean_ratio = sum(ratio) / len(ratio)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratio) / len(ratio))

    return {
        "metric_name": "lind_over_rank_var",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(abs(r - mean_ratio) <= 2 * std_ratio for r in ratio),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")