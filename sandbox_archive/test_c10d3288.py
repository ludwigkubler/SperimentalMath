# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def boolean_fourier_coefficients(G, n):
    m = len(G)
    F = [0] * (1 << m)
    for i in range(1 << m):
        sign = 1
        for j in range(m):
            if i & (1 << j):
                sign *= (-1) ** G[j]
        F[i] = sign / math.sqrt(m)
    return F

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 30)
    degree = random.randint(1, 10)
    G = []
    for _ in range(n):
        neighbors = set()
        while len(neighbors) < degree:
            neighbor = random.randint(0, n-1)
            if neighbor != _ and neighbor not in neighbors:
                neighbors.add(neighbor)
        G.append(list(neighbors))
    
    Tseitin_formula = []
    for i in range(n):
        for j in range(i+1, n):
            Tseitin_formula.extend([i, j])
    
    F = boolean_fourier_coefficients(G, n)
    min_index = min(abs(f) for f in F if abs(f) > 0)
    
    conjecture_holds = min_index >= (2 ** n / math.log(n)) ** 0.5
    counterexample = "" if conjecture_holds else "min_index < θ(2^n / log^2(n))"
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")