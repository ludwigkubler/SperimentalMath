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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        for j in range(i, n + 1):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(i, n + 1):
                    matrix[j][k] -= factor * matrix[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        factor = matrix[i][i]
        if factor == 0:
            return 0
        det *= factor
        for j in range(i+1, n):
            matrix[j][i] /= factor
        for j in range(i+1, n):
            for k in range(i+1, n+1):
                matrix[j][k] -= matrix[i][k] * matrix[j][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random quantum 2-complex G with n vertices
    n = random.randint(10, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the quantum torsion α(G)
    alpha_G = 0
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                det = determinant([[G[k][l] for l in range(n) if k != i and k != j and l != i and l != j] for k in range(n) if k != i and k != j])
                alpha_G += abs(det)
    
    # Construct the associated Tseitin formula F_G from G
    m = n * (n - 1) // 2
    F_G = [[0 for _ in range(m + n)] for _ in range(m + n)]
    for i in range(n):
        F_G[i][i] = 1
    for k in range(m):
        i, j = divmod(k, n)
        if G[i][j]:
            F_G[n + k][i] = 1
            F_G[n + k][n + j] = 1
            F_G[k][n + k] = 1
    
    # Measure the resolution proof length for F_G
    resolution_length = 0
    while True:
        try:
            gaussian_elimination(F_G)
            break
        except ValueError:
            resolution_length += 1
            F_G = matrix_multiply([[random.choice([0, 1]) for _ in range(m + n)] for _ in range(m + n)], F_G)
    
    # Compute the metric value log^2(n) / log(α(G))
    if alpha_G == 0:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "alpha_G is zero"
        }
    
    metric_value = math.log(n)**2 / math.log(alpha_G)
    
    # Check if the conjecture holds
    if resolution_length >= metric_value:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"resolution_length ({resolution_length}) < metric_value ({metric_value})"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if r['metric_value'] is not None]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r['metric_value'] > mean + 3 * std for r in results):
        first_failing_seed = next(r['seed'] for r in results if r['metric_value'] > mean + 3 * std)
        print(f"RESULT: FALSIFIED counterexample='resolution_length > mean + 3*std' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")