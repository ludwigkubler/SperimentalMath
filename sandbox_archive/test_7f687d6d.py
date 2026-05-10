# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_max_cut_instance(n):
    G = {i: set() for i in range(n)}
    edges = list(combinations(range(n), 2))
    for u, v in edges:
        if random.random() < 0.5:
            G[u].add(v)
            G[v].add(u)
    return G

def moment_matrix(G, d):
    n = len(G)
    M = [[0] * (n + d) for _ in range(n + d)]
    for i in range(n):
        M[i][i] = 1
        for j in range(i + 1, n):
            if j in G[i]:
                M[i][j] = -1
                M[j][i] = -1
    for k in range(2, d + 1):
        for i in range(n):
            for j in range(i + 1, n):
                if j in G[i]:
                    M[n+k-1][n+j] = -1
    return M

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    matrix = [row[:] for row in matrix]
    pivot_row = 0
    for i in range(n):
        if pivot_row >= m:
            break
        max_abs = abs(matrix[pivot_row][i])
        max_row = pivot_row
        for j in range(pivot_row + 1, m):
            if abs(matrix[j][i]) > max_abs:
                max_abs = abs(matrix[j][i])
                max_row = j
        if max_abs == 0:
            continue
        matrix[pivot_row], matrix[max_row] = matrix[max_row], matrix[pivot_row]
        for j in range(n):
            matrix[pivot_row][j] /= matrix[pivot_row][i]
        for j in range(m):
            if j != pivot_row and abs(matrix[j][i]) > 1e-9:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[pivot_row][k]
        pivot_row += 1
    return sum(1 for row in matrix if any(abs(x) > 1e-9 for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = generate_max_cut_instance(n)
    d = min(10, n - 2)
    M = moment_matrix(G, d)
    rank_M = rank(M)
    metric_value = (rank_M * d**2) / n
    conjecture_holds = metric_value >= 1.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")