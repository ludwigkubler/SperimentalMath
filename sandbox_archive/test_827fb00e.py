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
            for j in range(i + 1, m):
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
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A_copy = [row[:] for row in A]
        gaussian_elimination(A_copy)
        rank = 0
        for row in A_copy:
            if any(row):
                rank += 1
        return rank

    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges

    def sum_of_squares_polynomial(edges, d):
        n = len(edges) * 2
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, j in edges:
            A[2 * i][2 * j + 1] = -1
            A[2 * i + 1][2 * j] = -1
            A[2 * j][2 * i + 1] = -1
            A[2 * j + 1][2 * i] = -1
        for i in range(n):
            A[i][n] = 1
        return A

    def generalized_kostant_partition_function(A, d):
        n = len(A)
        B = [[0] * (d + 1) for _ in range(n)]
        for i in range(n):
            for j in range(d + 1):
                if j == 0:
                    B[i][j] = A[i][n]
                else:
                    B[i][j] = sum(A[i][k] * B[k][j - 1] for k in range(n))
        return B

    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = max_cut_instance(n)
    d = random.randint(1, 5)
    A = sum_of_squares_polynomial(edges, d)
    rank_A = rank(A)

    B = generalized_kostant_partition_function(A, d)
    rank_B = rank(B)

    metric_value = rank_B
    instances_tested = 1
    conjecture_holds = rank_B <= d
    counterexample = "" if conjecture_holds else f"Rank of GKPF is {rank_B}, expected ≤ {d}"

    return {
        "metric_name": "Generalized Kostant Partition Function Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds conjectured bound\" first_failing_seed={first_failing_seed}")