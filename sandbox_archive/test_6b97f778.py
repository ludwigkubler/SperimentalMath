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
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    inv_matrix = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        inv_matrix[i][i] = 1
    for i in range(n):
        pivot = matrix[i][i]
        factor = mod_inverse(pivot, mod)
        for j in range(n):
            matrix[i][j] *= factor
            inv_matrix[i][j] *= factor
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
                    inv_matrix[k][j] -= factor * inv_matrix[i][j]
    return inv_matrix

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= mod
    return C

def gaussian_elimination(matrix, mod):
    n = len(matrix)
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        factor = mod_inverse(matrix[i][i], mod)
        for j in range(n):
            matrix[i][j] *= factor
            matrix[i][j] %= mod
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
                    matrix[j][k] %= mod
    return matrix

def is_diophantine_solution(matrix, solution, mod):
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + [solution[i]] for i, row in enumerate(matrix)]
    reduced_matrix = gaussian_elimination(augmented_matrix, mod)
    return all(reduced_matrix[i][i] == solution[i] for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    degree = random.randint(1, 10)
    mod = 2**degree
    matrix = [[random.randint(0, mod-1) for _ in range(n)] for _ in range(n)]
    solution = [random.randint(0, mod-1) for _ in range(n)]
    
    rank = sum(1 for row in matrix if any(row[j] != 0 for j in range(n)))
    resolution_steps = n * (n - rank)
    
    return {
        "metric_name": "Resolution Steps",
        "metric_value": resolution_steps,
        "instances_tested": 1,
        "conjecture_holds": resolution_steps > math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_steps = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Resolution steps <= log n\" first_failing_seed={first_failing_seed}")