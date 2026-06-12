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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return b

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A, mod):
    n = len(A)
    I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    A_augmented = [row + col for row, col in zip(A, I)]
    det = gaussian_elimination(A_augmented, [0] * n)[-1]
    if det == 0:
        return None
    inv_det = pow(det, mod - 2, mod)
    for i in range(n):
        for j in range(n):
            A_augmented[i][j] *= inv_det
    return [row[n:] for row in A_augmented]

def p_adic_divergence(f):
    n = len(f)
    count = [0] * (1 << n)
    for x in range(1 << n):
        count[f(x)] += 1
    p_adic_sum = 0
    for c in count:
        if c > 0:
            p_adic_sum += c / (c + 1) * math.log2(c + 1)
    return p_adic_sum

def communication_complexity_rank_variance(f):
    n = len(f)
    rank_var = 0
    for x in range(1 << n):
        for y in range(x, 1 << n):
            if f(x) != f(y):
                rank_var += 1
    return rank_var / (n * (2 ** n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        instances_tested = 0
        p_adic_values = []
        rank_var_values = []
        for _ in range(30):
            f = [random.randint(0, 1) for _ in range(1 << n)]
            p_adic_val = p_adic_divergence(f)
            rank_var_val = communication_complexity_rank_variance(f)
            p_adic_values.append(p_adic_val)
            rank_var_values.append(rank_var_val)
            instances_tested += 1
        if len(p_adic_values) < 30:
            return {
                "metric_name": "p_adic_divergence",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        pearson_corr = sum((x - mean(p_adic_values)) * (y - mean(rank_var_values)) for x, y in zip(p_adic_values, rank_var_values)) / (len(p_adic_values) * stdev(p_adic_values) * stdev(rank_var_values))
        results.append({
            "n": n,
            "pearson_corr": pearson_corr
        })
    mean_corr = sum(result["pearson_corr"] for result in results) / len(results)
    return {
        "metric_name": "p_adic_divergence",
        "metric_value": mean_corr,
        "instances_tested": 30 * len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(result["pearson_corr"] >= 0.7 for result in results) and all(result["pearson_corr"] >= 0.5 for result in results),
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def stdev(lst):
    avg = mean(lst)
    return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / len(results)
    std_corr = stdev([result["metric_value"] for result in results if result["conjecture_holds"]])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_corr\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")