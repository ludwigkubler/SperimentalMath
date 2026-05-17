# auto-injected by SEC sandbox
import itertools
import collections
import json
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
from fractions import Fraction

def eulerian_number(n, k):
    if k == 0:
        return 1
    if k == 1:
        return (n - k) * eulerian_number(n, k - 1)
    return (k + 1) * eulerian_number(n, k - 1) + (n - k) * eulerian_number(n, k)

def compute_entropy(n):
    coefficients = [eulerian_number(n, k) for k in range(n)]
    total = sum(coefficients)
    if total == 0:
        return 0.0
    normalized = [Fraction(c, total) for c in coefficients]
    entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in normalized)
    return float(entropy)

def generate_sparse_matrix(m, n, seed):
    random.seed(seed)
    matrix = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for _ in range(3):
            j = random.randint(0, n - 1)
            matrix[i][j] = random.choice([-1, 1])
    return matrix

def generate_sparse_padding(n, m, seed):
    random.seed(seed + 1)
    padding = []
    for _ in range(n - m):
        form = [0] * n
        for _ in range(3):
            j = random.randint(0, n - 1)
            form[j] = random.choice([-1, 1])
        padding.append(form)
    return padding

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * matrix_determinant(minor)
    return det

def compute_padded_determinant(L, p, m, n):
    det_m = matrix_determinant(L[:m][:m])
    for form in p:
        det_m *= sum(form[i] * L[i][j] for i in range(n) for j in range(n))
    return det_m

def run_trial(seed):
    n_values = [4, 5, 6, 7, 8]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Test part (i)
        entropy = compute_entropy(n)
        if entropy < 1.0:
            conjecture_holds = False
            counterexample = f"n={n} violates part (i): entropy={entropy} < 1.0"

        # Test part (ii)
        m_values = [1, 2, int(math.sqrt(n))]
        for m in m_values:
            L = generate_sparse_matrix(m, n, seed)
            p = generate_sparse_padding(n, m, seed)
            det_padded = compute_padded_determinant(L, p, m, n)
            if det_padded > math.log2(2 * m + 1):
                conjecture_holds = False
                counterexample = f"n={n}, m={m} violates part (ii): det_padded={det_padded} > log2(2m+1)"

    return {
        "metric_name": "entropy",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
        "instances_tested": len(n_values) * len(m_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")