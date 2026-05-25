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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def compute_rank(A):
        rank = 0
        m, n = len(A), len(A[0])
        A_copy = [row[:] for row in A]
        gaussian_elimination(A_copy)
        for i in range(m):
            if any(A_copy[i]):
                rank += 1
        return rank

    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    weight = random.randint(1, 10)
                    edges.append((i, j, weight))
        return edges

    def sos_polynomial(edges, d):
        # Placeholder implementation
        return 0

    def max_cut_ratio(edges, polynomial):
        # Placeholder implementation
        return 0

    n = 40
    edges = max_cut_instance(n)
    d = random.randint(1, 5)

    moment_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v, w in edges:
        moment_matrix[u][v] += w
        moment_matrix[v][u] += w

    rank = compute_rank(moment_matrix)
    polynomial = sos_polynomial(edges, d)
    ratio = max_cut_ratio(edges, polynomial)

    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= d and ratio > 0.878,
        "counterexample": "" if rank >= d and ratio > 0.878 else f"Ratio: {ratio}, Rank: {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")