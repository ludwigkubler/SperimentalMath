# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def eulerian_number(n, k):
    if k < 0 or k >= n:
        return 0
    if k == 0:
        return 1
    if k == n - 1:
        return 1
    return (k + 1) * eulerian_number(n, k - 1) + (n - k) * eulerian_number(n, k)

def compute_entropy(n, coefficients):
    total = sum(coefficients)
    if total == 0:
        return 0.0
    normalized = [Fraction(c, total) for c in coefficients]
    entropy = 0.0
    for p in normalized:
        if p > 0:
            entropy -= float(p * math.log2(p))
    return entropy

def generate_random_matrix(m, n, seed):
    random.seed(seed)
    matrix = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for _ in range(3):
            j = random.randint(0, n - 1)
            matrix[i][j] = random.choice([-1.0, 1.0])
    return matrix

def generate_random_padding(n, m, seed):
    random.seed(seed)
    padding = []
    for _ in range(n - m):
        form = [0.0 for _ in range(n)]
        for _ in range(3):
            j = random.randint(0, n - 1)
            form[j] = random.choice([-1.0, 1.0])
        padding.append(form)
    return padding

def matrix_multiply(a, b):
    result = [[0.0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0.0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * matrix_determinant(minor)
    return det

def apply_padding(det, padding):
    result = {}
    for monomial, coeff in det.items():
        for form in padding:
            new_monomial = tuple(monomial[i] + form[i] for i in range(len(monomial)))
            if new_monomial in result:
                result[new_monomial] += coeff
            else:
                result[new_monomial] = coeff
    return result

def expand_determinant(matrix):
    n = len(matrix)
    if n == 1:
        return {(0,): matrix[0][0]}
    det = {}
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        minor_det = expand_determinant(minor)
        for monomial, coeff in minor_det.items():
            new_monomial = (col,) + tuple(x + 1 if x >= col else x for x in monomial)
            if new_monomial in det:
                det[new_monomial] += ((-1) ** col) * matrix[0][col] * coeff
            else:
                det[new_monomial] = ((-1) ** col) * matrix[0][col] * coeff
    return det

def run_trial(seed):
    n_values = [4, 5, 6, 7, 8]
    results = []
    for n in n_values:
        # Part (i): Check ρ(perm_n) ≥ 1
        coefficients = [eulerian_number(n, k) for k in range(n)]
        entropy = compute_entropy(n, coefficients)
        if entropy < 1.0:
            return {
                "metric_name": "entropy",
                "metric_value": entropy,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n} ρ(perm_n)={entropy} < 1.0"
            }

        # Part (ii): Check ρ(det_m(L(y))·p) ≤ log_2(2m+1)
        m_values = [1, 2, int(math.isqrt(n))]
        for m in m_values:
            L = generate_random_matrix(m, n, seed)
            padding = generate_random_padding(n, m, seed)
            det = expand_determinant(L)
            padded_det = apply_padding(det, padding)
            coefficients = [0.0 for _ in range(n)]
            for monomial, coeff in padded_det.items():
                if len(monomial) == n:
                    k = sum(1 for i in range(n-1) if monomial[i] > monomial[i+1])
                    coefficients[k] += coeff ** 2
            entropy = compute_entropy(n, coefficients)
            bound = math.log2(2 * m + 1)
            if entropy > bound:
                return {
                    "metric_name": "entropy",
                    "metric_value": entropy,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n} m={m} ρ(det_m(L(y))·p)={entropy} > log_2(2m+1)={bound}"
                }
            results.append(entropy)

    return {
        "metric_name": "entropy",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            break

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if x >= 1.0) / len(metric_values)

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')