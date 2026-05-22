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

def matrix_mult(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda x: abs(augmented[x][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for k in range(m):
            if k != i:
                factor = augmented[k][i]
                for j in range(n + 1):
                    augmented[k][j] -= factor * augmented[i][j]
    return [row[-1] for row in augmented]

def matroid_polynomial(M):
    n = len(M)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i, j in M:
        A[i][j], A[j][i] = 1, 1
    A[n][n] = 1
    return gaussian_elimination(A, [1] * (n + 1))[n]

def permanent_encoding_circuit_size(M):
    n = len(M)
    A = [[0] * n for _ in range(n)]
    for i, j in M:
        A[i][j], A[j][i] = 1, 1
    return sum(1 for row in A if all(x == 1 for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = set()
        while len(M) < n * (n - 1) // 2:
            i, j = random.sample(range(n), 2)
            if (i, j) not in M and (j, i) not in M:
                M.add((i, j))
        
        rho_M = matroid_polynomial(M)
        circuit_size = permanent_encoding_circuit_size(M)
        
        results.append({
            "n": n,
            "rho_M": rho_M,
            "circuit_size": circuit_size
        })
    
    if not results:
        return {
            "metric_name": "Minimal Monomial Degree Invariant / Circuit Size",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [result["rho_M"] / result["circuit_size"] for result in results]
    avg_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - avg_ratio) ** 2 for r in ratios) / len(ratios))
    
    return {
        "metric_name": "Minimal Monomial Degree Invariant / Circuit Size",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(r >= 2**(n/2 - 0.1) for n, r in zip(n_values, ratios)),
        "counterexample": "" if all(r >= 2**(n/2 - 0.1) for n, r in zip(n_values, ratios)) else f"Ratio {min(ratios)} < 2^{n_values[ratios.index(min(ratios))]/2 - 0.1}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    avg_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - avg_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")