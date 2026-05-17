# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

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

def trace(a):
    return sum(a[i][i] for i in range(len(a)))

def generate_disj_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if bin(i & j).count('1') % 2 == 1:
                matrix[i][j] = 1
    return matrix

def generate_eq_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if i == j:
                matrix[i][j] = 1
    return matrix

def generate_ip_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if bin(i & j).count('1') % 2 == 0:
                matrix[i][j] = 1
    return matrix

def generate_nand_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if not (i and j):
                matrix[i][j] = 1
    return matrix

def generate_product_matrix(n):
    a = [random.randint(0, 1) for _ in range(2**n)]
    b = [random.randint(0, 1) for _ in range(2**n)]
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            matrix[i][j] = a[i] * b[j]
    return matrix

def generate_random_matrix(n):
    return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]

def compute_powers(M, k):
    A = [M]
    for _ in range(1, 4):
        A.append(matrix_multiply(A[-1], M))
    return A

def compute_p(M, k, A):
    n = len(M)
    p = [0.0] * 4
    for j in range(4):
        p[j] = trace(A[j]) / (k * n)
    return p

def compute_kappa4(p):
    p1, p2, p3, p4 = p
    return p4 - 4 * p1 * p3 - 2 * p2**2 + 10 * p1**2 * p2 - 5 * p1**4

def compute_rho(M, k, A):
    p = compute_p(M, k, A)
    kappa4 = compute_kappa4(p)
    p1 = p[0]
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
        return math.log2(2**n) / 20
    elif matrix_type == "PRODUCT":
        return 1
    else:
        return 2**n

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    matrix_types = ["DISJ", "EQ", "IP", "NAND", "PRODUCT", "RANDOM"]
    results = []

    for n in n_values:
        for matrix_type in matrix_types:
            if matrix_type == "DISJ":
                M = generate_disj_matrix(n)
            elif matrix_type == "EQ":
                M = generate_eq_matrix(n)
            elif matrix_type == "IP":
                M = generate_ip_matrix(n)
            elif matrix_type == "NAND":
                M = generate_nand_matrix(n)
            elif matrix_type == "PRODUCT":
                M = generate_product_matrix(n)
            else:
                M = generate_random_matrix(n)

            k = n
            A = compute_powers(M, k)
            rho = compute_rho(M, k, A)
            cc_r = compute_cc_r(matrix_type, n)

            bound = (1/20) * math.log2(1 + abs(rho))
            conjecture_holds = bound <= 2 * cc_r
            counterexample = "" if conjecture_holds else f"Bound violated for {matrix_type} with n={n}"

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
        "metric_name": "mean_rho_DISJ",
        "metric_value": metric_value,
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
    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")