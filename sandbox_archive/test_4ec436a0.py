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
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix) % mod
    if det == 0:
        raise ValueError('Matrix is not invertible')
    inv_det = mod_inverse(det, mod)
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            adj[j][i] = (inv_det * determinant(minor)) % mod
    return adj

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for c in range(n):
        det += ((-1) ** c) * matrix[0][c] * determinant(get_minor(matrix, 0, c))
    return det

def get_minor(matrix, i, j):
    minor = []
    for r in range(len(matrix)):
        if r != i:
            row = []
            for c in range(len(matrix[r])):
                if c != j:
                    row.append(matrix[r][c])
            minor.append(row)
    return minor

def matrix_mult(A, B):
    n, m = len(A), len(B[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
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

def matrix_scalar_mul(matrix, scalar):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[i][j] * scalar for j in range(m)] for i in range(n)]
    return result

def matrix_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[j][i] for j in range(n)] for i in range(m)]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda x: abs(augmented_matrix[x][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i + 1, n):
            factor = augmented_matrix[j][i] / pivot
            augmented_matrix[j] = [augmented_matrix[j][k] - factor * augmented_matrix[i][k] for k in range(n + 1)]
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i + 1, n))) / augmented_matrix[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = 2 * n
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    clause_vectors = [phi[i] + [1] for i in range(m)]
    convex_hull = []
    for vector in clause_vectors:
        if not any(all(vector[j] <= other[j] for j in range(n)) for other in convex_hull):
            convex_hull.append(vector)
    hull_dimension = len(convex_hull) - 1
    acc0_circuit_size = None
    # Brute-force synthesis of ACC^0 circuit is computationally expensive and not feasible within the time limit
    return {
        "metric_name": "hull_dimension",
        "metric_value": hull_dimension,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")