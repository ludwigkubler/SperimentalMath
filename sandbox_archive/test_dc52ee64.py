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

def lu_decomposition(A):
    n = len(A)
    L = [[0 for _ in range(n)] for _ in range(n)]
    U = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        U[i][i] = A[i][i]
        for j in range(i+1, n):
            sum_upper = sum(L[j][k] * U[k][i] for k in range(i))
            U[j][i] = A[j][i] - sum_upper
        for j in range(i, n):
            if i == 0:
                L[j][i] = A[j][i]
            else:
                sum_lower = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (A[j][i] - sum_lower) / U[i][i]

    return L, U

def tensor_rank(M):
    n = len(M)
    A = [[0 for _ in range(n)] for _ in range(n)]
    B = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            A[i][j] = M[2*i][2*j]
            B[i][j] = M[2*i+1][2*j+1]

    _, U_A = lu_decomposition(A)
    _, U_B = lu_decomposition(B)

    rank_A = sum(1 for row in U_A if any(val != 0 for val in row))
    rank_B = sum(1 for row in U_B if any(val != 0 for val in row))

    return max(rank_A, rank_B)

def generate_disjointness_matrix(n):
    X = set(range(n))
    Y = set(range(n))
    M = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if (i in X and j in Y) or (i not in X and j not in Y):
                M[i][j] = 1

    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []

    for n in n_values:
        M = generate_disjointness_matrix(n)
        rank = tensor_rank(M)
        metric_values.append(rank)

    if len(metric_values) < 30:
        return {
            "metric_name": "tensor_rank",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": len(metric_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    slope, intercept = linear_regression(n_values, metric_values)
    if slope < 0.9 * n_values[0]:
        return {
            "metric_name": "tensor_rank",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": len(metric_values),
            "conjecture_holds": False,
            "counterexample": f"sublinear growth: slope={slope}"
        }

    return {
        "metric_name": "tensor_rank",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n

    return slope, intercept

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sublinear growth\" first_failing_seed={first_failing_seed}")