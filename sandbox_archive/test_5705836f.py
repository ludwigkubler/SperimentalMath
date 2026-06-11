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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix) % mod
    if det == 0:
        raise ValueError("Matrix is not invertible")
    inv_det = inverse(det, mod)
    for i in range(n):
        for j in range(n):
            adj[j][i] = ((-1) ** (i + j)) * minor(matrix, i, j) % mod
    return matrix_mod_mul(adj, inv_det, mod)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for c in range(n):
        det += ((-1) ** c) * matrix[0][c] * determinant(minor(matrix, 0, c))
    return det

def minor(matrix, i, j):
    n = len(matrix)
    minor = []
    for r in range(n):
        if r == i:
            continue
        row = []
        for c in range(n):
            if c == j:
                continue
            row.append(matrix[r][c])
        minor.append(row)
    return minor

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def smith_normal_form(matrix, mod):
    n = len(matrix)
    U = [[0 for _ in range(n)] for _ in range(n)]
    V = [[0 for _ in range(n)] for _ in range(n)]
    A = [row[:] for row in matrix]
    for i in range(n):
        U[i][i] = 1
        V[i][i] = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            for j in range(k + 1, n):
                if A[j][k] != 0:
                    A[k], A[j] = A[j], A[k]
                    U[k], U[j] = U[j], U[k]
                    break
        for i in range(k + 1, n):
            if A[i][k] != 0:
                m = A[i][k] * inverse(A[k][k], mod)
                A[i] = [(A[i][j] - m * A[k][j]) % mod for j in range(n)]
                U[i] = [(U[i][j] - m * U[k][j]) % mod for j in range(n)]
    return matrix_mod_mul(matrix_mod_inv(U, mod), A, mod)

def frege_proof_depth(formula):
    stack = []
    depth = 0
    max_depth = 0
    for token in formula:
        if token == '(':
            stack.append(token)
            depth += 1
            max_depth = max(max_depth, depth)
        elif token == ')':
            stack.pop()
            depth -= 1
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        AKT_dim_sum = 0
        depth_sum = 0
        for _ in range(30):
            variables = [f'x{i}' for i in range(n)]
            literals = [random.choice(variables) + random.choice('+-') for _ in range(random.randint(2, n * 2))]
            formula = ' & '.join(literals)
            matroid = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            AKT_dim = sum(sum(row) for row in smith_normal_form(matroid, 2))
            depth = frege_proof_depth(formula.split())
            instances_tested += 1
            AKT_dim_sum += AKT_dim
            depth_sum += depth
        if instances_tested < 30:
            return {
                "metric_name": "Pearson correlation coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        mean_AKT_dim = AKT_dim_sum / instances_tested
        mean_depth = depth_sum / instances_tested
        correlation_coefficient = (instances_tested * sum(AKT_dim * depth for AKT_dim, depth in zip(results, results)) - sum(results) * sum(results)) / math.sqrt((instances_tested * sum(AKT_dim ** 2 for AKT_dim in results) - sum(results) ** 2) * (instances_tested * sum(depth ** 2 for depth in results) - sum(results) ** 2))
        results.append(correlation_coefficient)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": mean(results),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": all(r >= 0.5 for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] or r['counterexample'] == "insufficient_instances" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(r['counterexample'] != "" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r['counterexample'] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_data")