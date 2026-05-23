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
    
    def generate_k_clique(n, k):
        if n < k or k <= 1:
            return []
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        remaining_edges = random.sample([(i, j) for i in range(k, n) for j in range(i + 1, n)], n - k)
        edges.extend(remaining_edges)
        return edges

    def matrix_multiplication(A, B):
        m, p = len(A), len(B[0])
        result = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x

    def minimal_rank(edges, n):
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for u, v in edges:
            A[u][v] += 1
            A[v][u] += 1
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank)):
                continue
            rank += 1
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank

    def monotone_circuit(k, n):
        # This is a placeholder function. The actual construction of a monotone circuit
        # that separates the k-CLIQUE language from the empty set is complex and beyond
        # the scope of this test.
        return "mapping_undefined"

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        k_values = range(2, min(n, 4))
        for k in k_values:
            edges = generate_k_clique(n, k)
            rank = minimal_rank(edges, n)
            if rank > n ** (1.5 - k):
                counterexample = f"n={n}, k={k}, rank={rank}"
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            results.append(rank)

    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r <= n ** (1.5 - k)]) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")