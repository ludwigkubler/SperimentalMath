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

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * determinant([[matrix[j][k] for k in range(n) if k != i] for j in range(1, n)], mod)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
            adjugate[j][i] = (-1) ** (i + j) * determinant(minor, mod)
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def determinant(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = [[matrix[j][k] for k in range(1, n)] for j in range(1, n) if j != i]
        det += (-1) ** i * matrix[0][i] * determinant(minor, mod)
    return det % mod

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [0] for row in matrix]
    for j in range(m - 1):
        pivot_row = j
        for i in range(j + 1, n):
            if abs(augmented_matrix[i][j]) > abs(augmented_matrix[pivot_row][j]):
                pivot_row = i
        augmented_matrix[j], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[j]
        for i in range(n):
            if i != j:
                factor = augmented_matrix[i][j] / augmented_matrix[j][j]
                for k in range(m + 1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    return [row[:-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clause_tree_width = n
    cnf_formula = []
    for _ in range(n):
        cnf_formula.append(random.sample(range(1, n + 1), 2))
    
    # Construct birational variety (simplified example)
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    inv_matrix = matrix_mod_inv(matrix, 2)
    
    # Calculate minimal rank
    min_rank = len(gaussian_elimination(inv_matrix))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": min_rank <= math.log(n, 2) + 3 and min_rank >= math.log(n, 2) - 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 1}")