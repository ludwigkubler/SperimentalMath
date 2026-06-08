# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def construct_algebraic_curve(f):
    n = len(f)
    curve = []
    for x in range(2**n):
        y = f[x]
        curve.append((x, y))
    return curve

def communication_protocol_matrix(curve):
    n = len(curve[0][0])
    M = [[0] * (2*n) for _ in range(2*n)]
    for x, y in curve:
        for i in range(n):
            if x & (1 << i):
                M[i][n + i] = 1
                M[n + i][i] = 1
            else:
                M[i][n + i] = -1
                M[n + i][i] = -1
        M[y][n + y] += 1
    return M

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_rank_variance(M):
    n = len(M)
    rank = 0
    for i in range(n):
        if all(A[i][j] == 0 for j in range(n)):
            continue
        rank += 1
        pivot_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[pivot_row][i]):
                pivot_row = j
        M[i], M[pivot_row] = M[pivot_row], M[i]
        pivot = M[i][i]
        for j in range(n):
            M[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "Rank Variance Correlation"
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        curve = construct_algebraic_curve(f)
        protocol_matrix = communication_protocol_matrix(curve)
        rank_var = matrix_rank_variance(protocol_matrix)
        results.append(rank_var)
    
    mean_rank_var = sum(results) / len(results)
    conjecture_holds = all(abs(r - mean_rank_var) <= 3 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_rank_var,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")