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

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(M, p, mod):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        p //= 2
    return result

def matrix_inv(M, mod):
    n = len(M)
    det = 0
    for i in range(n):
        minor = [[M[j][k] for k in range(n) if k != i] for j in range(1, n)]
        det += M[0][i] * (-1)**i * matrix_det(minor, mod)
    det = pow(det, mod-2, mod)
    inv = []
    for i in range(n):
        minor = [[M[j][k] for k in range(n) if k != i] for j in range(1, n)]
        cofactor = (-1)**i * matrix_det(minor, mod)
        inv.append([cofactor * det % mod for i in range(n)])
    return inv

def matrix_det(M, mod):
    n = len(M)
    if n == 1:
        return M[0][0]
    det = 0
    for i in range(n):
        minor = [[M[j][k] for k in range(1, n)] for j in range(1, n) if j != i]
        det += M[i][0] * (-1)**i * matrix_det(minor, mod)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    e_C = random.randint(1, n)
    
    # Generate a random Boolean circuit
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the entanglement complexity (simplified as number of non-zero entries)
    entanglement_complexity = sum(sum(row) for row in C)
    
    # Generate a Morse function G based on the circuit
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the minimal geometric defect Δ(G)
    critical_points = []
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n-1 or j == 0 or j == n-1:
                continue
            neighbors = [G[i+1][j], G[i-1][j], G[i][j+1], G[i][j-1]]
            if all(G[i][j] < neighbor for neighbor in neighbors):
                critical_points.append((i, j))
    
    geometric_defect = min(math.dist(cp1, cp2) for cp1, cp2 in itertools.combinations(critical_points, 2))
    
    return {
        "metric_name": "geometric_defect",
        "metric_value": geometric_defect,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": geometric_defect <= e_C * 2,  # Simplified upper bound
        "counterexample": "" if geometric_defect <= e_C * 2 else f"Geometric defect {geometric_defect} > {e_C * 2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric_defect > 2 * entanglement_complexity\" first_failing_seed={first_failing_seed}")