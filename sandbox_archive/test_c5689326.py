# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(matrix):
        n = len(matrix)
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i]):
                rank += 1
        return rank

    def generate_k_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i+1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges

    n = random.randint(5, 40)
    vertices, edges = generate_k_clique_instance(n, n // 2)

    # Construct the affine scheme
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        A[i][i] = Fraction(1)
        A[n][i] = Fraction(-1)
    for u, v in edges:
        A[u][v] = Fraction(1)
        A[v][u] = Fraction(1)

    # Tropicalize the affine scheme
    tropicalized_A = [[max(A[i][j], 0) for j in range(n + 1)] for i in range(n + 1)]

    # Compute the rank of the tropicalized affine scheme
    rank_T = rank(tropicalized_A)
    
    return {
        "metric_name": "Tropicalized Rank",
        "metric_value": rank_T,
        "instances_tested": 1,
        "conjecture_holds": True if n**0.25 <= rank_T <= n**0.25 else False,
        "counterexample": "" if n**0.25 <= rank_T <= n**0.25 else f"n={n}, rank={rank_T}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_rank = sum(res["metric_value"] for res in results if "metric_value" in res)
    mean_rank = Fraction(total_rank, len(results))
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))

    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")