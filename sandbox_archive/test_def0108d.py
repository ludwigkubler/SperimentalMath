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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if i < n:
            pivot_row = i
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            A[i], A[pivot_row] = A[pivot_row], A[i]
        for j in range(m):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank += 1
    return rank

def local_induction_dimension(P):
    n = len(P)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if P[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    return gaussian_elimination(A)

def communication_complexity_rank_variance(P):
    n = len(P)
    ranks = [0] * n
    for i in range(n):
        rank = 0
        visited = set()
        stack = [i]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                rank += 1
                for j in range(n):
                    if P[node][j] and j not in visited:
                        stack.append(j)
        ranks[i] = rank
    return sum((r - n / 2) ** 2 for r in ranks) / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            P[i][i] = 0
        l_id = local_induction_dimension(P)
        v = communication_complexity_rank_variance(P)
        results.append((l_id, v))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    l_ids, vs = zip(*results)
    mean_l_id = sum(l_ids) / len(l_ids)
    mean_v = sum(vs) / len(vs)
    covariance = sum((l_ids[i] - mean_l_id) * (vs[i] - mean_v) for i in range(len(l_ids))) / len(l_ids)
    variance_l_id = sum((l_ids[i] - mean_l_id) ** 2 for i in range(len(l_ids))) / len(l_ids)
    variance_v = sum((vs[i] - mean_v) ** 2 for i in range(len(vs))) / len(vs)
    pearson_corr = covariance / math.sqrt(variance_l_id * variance_v)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(l_ids),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= pearson_corr < 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")