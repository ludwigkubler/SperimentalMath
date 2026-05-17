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
        return 2 ** n - 1
    if k == n - 1:
        return 1
    if k == n:
        return 0
    return (k + 1) * eulerian_number(n, k - 1) + (n - k) * eulerian_number(n, k)

def compute_entropy(n):
    coefficients = [eulerian_number(n, k) for k in range(n)]
    total = sum(coefficients)
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
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
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

def expand_polynomial(matrix, padding):
    n = len(matrix)
    m = len(padding) + 1
    det = matrix_determinant(matrix[:m][:m])
    for form in padding:
        det *= sum(form[i] * matrix[i][i] for i in range(n))
    return det

def compute_padded_entropy(n, m, seed):
    L = generate_sparse_matrix(m, n, seed)
    p = generate_sparse_padding(n, m, seed)
    det = expand_polynomial(L, p)
    coefficients = [0] * n
    for sigma in permutations(range(n)):
        monomial = tuple(sigma[i] for i in range(n))
        if monomial in det:
            k = sum(1 for i in range(n - 1) if sigma[i] > sigma[i + 1])
            coefficients[k] += det[monomial] ** 2
    total = sum(coefficients)
    if total == 0:
        return 0.0
    normalized = [Fraction(c, total) for c in coefficients]
    entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in normalized)
    return float(entropy)

def permutations(elements):
    if len(elements) <= 1:
        yield elements
    else:
        for perm in permutations(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

def run_trial(seed):
    n = random.randint(4, 8)
    entropy = compute_entropy(n)
    conjecture_holds = entropy >= 1.0
    counterexample = "" if conjecture_holds else f"n={n} entropy={entropy}"

    m = min(2, int(math.sqrt(n)))
    padded_entropy = compute_padded_entropy(n, m, seed)
    padded_bound = math.log2(2 * m + 1)
    padded_holds = padded_entropy <= padded_bound
    if not padded_holds:
        conjecture_holds = False
        counterexample = f"n={n} m={m} padded_entropy={padded_entropy} bound={padded_bound}"

    return {
        "metric_name": "entropy",
        "metric_value": entropy,
        "instances_tested": 1,
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
        failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{failing['counterexample']}\" first_failing_seed={failing['seed']}")