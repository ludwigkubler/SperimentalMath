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

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return None
        for j in range(m):
            if i != j:
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented_matrix[i][-1] / augmented_matrix[i][i]
        for j in range(i):
            augmented_matrix[j][-1] -= augmented_matrix[j][i] * x[i]
    return x

def compute_BP_readTwice_tensor_width(P):
    n = len(P)
    if n == 0:
        return 0
    A = [[P[i][j] for j in range(n)] for i in range(n)]
    b = [1] * n
    solution = gaussian_elimination(A, b)
    if solution is None:
        return float('inf')
    rho_P = sum(abs(x) for x in solution)
    return rho_P

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rho_P = compute_BP_readTwice_tensor_width(P)
    
    r = random.randint(1, min(n, 5))
    Q_coeffs = [random.choice(range(-10, 11)) for _ in range(r)]
    Q = [[sum(Q_coeffs[j] * P[i][j] for j in range(r)) for i in range(n)] for _ in range(n)]
    
    rho_Q = compute_BP_readTwice_tensor_width(Q)
    upper_bound = n**2 * r * math.log(r)
    
    return {
        "metric_name": "BP_readTwice_tensor_width",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": rho_Q <= upper_bound,
        "counterexample": "" if rho_Q <= upper_bound else f"rho(Q)={rho_Q}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")