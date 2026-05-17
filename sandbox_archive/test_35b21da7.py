# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction

def matrix_multiply(a, b):
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_transpose(a):
    return [list(row) for row in zip(*a)]

def matrix_trace(a):
    return sum(a[i][i] for i in range(len(a)))

def build_disj_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            x = i ^ j
            if x & (x - 1) == 0 and x != 0:
                matrix[i][j] = 1
    return matrix

def build_eq_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if i == j:
                matrix[i][j] = 1
    return matrix

def build_ip_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if bin(i).count('1') == bin(j).count('1'):
                matrix[i][j] = 1
    return matrix

def build_nand_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if not (i and j):
                matrix[i][j] = 1
    return matrix

def build_product_matrix(n):
    a = [random.randint(0, 1) for _ in range(2**n)]
    b = [random.randint(0, 1) for _ in range(2**n)]
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            matrix[i][j] = a[i] * b[j]
    return matrix

def build_random_matrix(n):
    return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]

def compute_powers(M, k):
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    for _ in range(30):
        S = random.sample(range(len(M)), k)
        T = random.sample(range(len(M[0])), k)
        A = [[M[i][j] for j in T] for i in S]
        A_transpose = matrix_transpose(A)
        A_power = A
        for _ in range(1):
            A_power = matrix_multiply(A_power, A)
        p1 += matrix_trace(A_power) / k
        A_power = matrix_multiply(A_power, A)
        p2 += matrix_trace(A_power) / k
        A_power = matrix_multiply(A_power, A)
        p3 += matrix_trace(A_power) / k
        A_power = matrix_multiply(A_power, A)
        p4 += matrix_trace(A_power) / k
    p1 /= 30
    p2 /= 30
    p3 /= 30
    p4 /= 30
    return p1, p2, p3, p4

def compute_kappa4(p1, p2, p3, p4):
    return p4 - 4 * p1 * p3 - 2 * p2**2 + 10 * p1**2 * p2 - 5 * p1**4

def compute_rho(p1, p2, p3, p4):
    kappa4 = compute_kappa4(p1, p2, p3, p4)
    denominator = max(p1**4, 1e-12)
    return kappa4 / denominator

def compute_cc_r(matrix_type, n):
    if matrix_type == "DISJ":
        return math.log2(2**n) / 20
    elif matrix_type == "EQ":
        return n
    elif matrix_type == "IP":
        return n
    elif matrix_type == "NAND":
        return 1
    elif matrix_type == "PRODUCT":
        return 1
    else:
        return 1

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    matrix_types = ["DISJ", "EQ", "IP", "NAND", "PRODUCT", "RANDOM"]
    results = []
    for n in n_values:
        k = n
        for matrix_type in matrix_types:
            if matrix_type == "DISJ":
                M = build_disj_matrix(n)
            elif matrix_type == "EQ":
                M = build_eq_matrix(n)
            elif matrix_type == "IP":
                M = build_ip_matrix(n)
            elif matrix_type == "NAND":
                M = build_nand_matrix(n)
            elif matrix_type == "PRODUCT":
                M = build_product_matrix(n)
            else:
                M = build_random_matrix(n)
            p1, p2, p3, p4 = compute_powers(M, k)
            rho = compute_rho(p1, p2, p3, p4)
            cc_r = compute_cc_r(matrix_type, n)
            bound = (1/20) * math.log2(1 + abs(rho))
            conjecture_holds = bound <= 2 * cc_r
            counterexample = ""
            if not conjecture_holds:
                counterexample = f"matrix_type={matrix_type}, n={n}, seed={seed}, bound={bound}, cc_r={cc_r}"
            results.append({
                "matrix_type": matrix_type,
                "n": n,
                "rho": rho,
                "cc_r": cc_r,
                "bound": bound,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    metric_value = sum(r["rho"] for r in results if r["matrix_type"] == "DISJ") / len([r for r in results if r["matrix_type"] == "DISJ"])
    instances_tested = len(results)
    conjecture_holds_all = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    return {
        "metric_name": "mean_log2_rho_DISJ",
        "metric_value": math.log2(abs(metric_value)) if metric_value != 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        trials.append(result)
    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")