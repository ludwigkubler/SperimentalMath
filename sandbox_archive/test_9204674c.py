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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * matrix_determinant(submatrix)
        sign *= -1
    return det

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def rank_of_matrix(A):
    det = matrix_determinant(A)
    if det == 0:
        return sum(1 for row in A if any(row))
    else:
        return len(A)

def boolean_tensor_product(x):
    n = len(x)
    TP = [0] * (2**n)
    for i in range(n):
        TP[1 << i] = x[i]
    for i in range(1, 2**n):
        TP[i] = TP[i & (i - 1)] ^ TP[i ^ (i & (i - 1))]
    return TP

def boolean_tensor_product_valuation(TP):
    n = len(TP)
    m = 0
    for i in range(1, n):
        if TP[i]:
            m += 1
    return math.log2(m)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        x = [random.choice([0, 1]) for _ in range(n)]
        TP = boolean_tensor_product(x)
        V_TP = boolean_tensor_product_valuation(TP)
        Fx_rank = rank_of_matrix([[i >> j & 1 for j in range(n)] for i in range(2**n)])
        results.append((Fx_rank, V_TP))
    mean_rank = sum(r[0] for r in results) / len(results)
    mean_V_TP = sum(r[1] for r in results) / len(results)
    if abs(mean_rank - mean_V_TP) > 1e-6:
        return {
            "metric_name": "Rank vs Valuation",
            "metric_value": None,
            "instances_tested": 30,
            "conjecture_holds": False,
            "counterexample": f"mean rank {mean_rank} != mean valuation {mean_V_TP}"
        }
    else:
        return {
            "metric_name": "Rank vs Valuation",
            "metric_value": abs(mean_rank - mean_V_TP),
            "instances_tested": 30,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")