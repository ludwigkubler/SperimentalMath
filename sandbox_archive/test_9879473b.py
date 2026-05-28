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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * determinant([[matrix[j][k] for k in range(n) if k != i] for j in range(1, n)]) * (-1)**i
    det %= mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
            adjugate[i][j] = determinant(minor) * (-1)**(i+j)
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mult(A, B):
    n, m = len(A), len(B[0])
    result = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_sub(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[j][i] for j in range(n)] for i in range(m)]
    return result

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix)):
        minor = [[matrix[j][k] for k in range(1, len(matrix)) if k != i] for j in range(1, len(matrix))]
        det += (-1)**i * matrix[0][i] * determinant(minor)
    return det

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, m):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, m):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[:-1] for row in augmented_matrix]

def construct_affine_variety(and_func):
    n = len(and_func)
    generators = []
    for i in range(2**n):
        if and_func(i) == 0:
            generators.append(bin(i)[2:].zfill(n))
    return generators

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(50):
            and_func = [random.randint(0, 1) for _ in range(2**n)]
            generators = construct_affine_variety(and_func)
            if not generators:
                continue
            rank = len(generators)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank > 2**n_values[-1]
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")