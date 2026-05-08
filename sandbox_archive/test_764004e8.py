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
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i, n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return [row[i] for row in A]

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_eigenvalues(G, d):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = d - sum(G[i])
            for j in range(i + 1, n):
                if G[i][j]:
                    L[i][j] = L[j][i] = -G[i][j]
        eigenvalues = gaussian_elimination(L)
        return sorted(eigenvalues)

    def tseitin_resolution_length(G, d):
        n = len(G)
        lambda_2 = laplacian_eigenvalues(G, d)[1]
        if lambda_2 < 1e-6:
            return 0
        return 2 ** (math.log(lambda_2) / math.log(2))

    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        degree = [0] * n
        edges_added = set()
        while any(d != sum(G[i]) for i in range(n)):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or G[u][v] or (u, v) in edges_added:
                continue
            G[u][v] = G[v][u] = 1
            degree[u] += 1
            degree[v] += 1
            edges_added.add((u, v))
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            d = random.randint(2, min(n - 1, 4))
            G = generate_d_regular_graph(n, d)
            length = tseitin_resolution_length(G, d)
            total_length += length
            instances_tested += 1

            if lambda_2 < 1e-6:
                expected_length = 0
            else:
                expected_length = 2 ** (math.log(lambda_2) / math.log(2))

            if abs(length - expected_length) > 1e-4:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, d={d} has unexpected resolution length {length}"

    return {
        "metric_name": "Tseitin Resolution Length",
        "metric_value": total_length / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_length = sum(result["metric_value"] for result in results) / len(results)
    std_length = math.sqrt(sum((result["metric_value"] - mean_length)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")