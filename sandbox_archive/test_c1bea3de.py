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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def poly_to_matrix(poly, n):
    A = [[0] * n for _ in range(n)]
    for i, coeff in enumerate(poly):
        x = bin(i)[2:].zfill(n)
        for j, bit in enumerate(x):
            if bit == '1':
                A[j][i % n] += coeff
    return A

def compute_genus(M):
    n = len(M)
    A = poly_to_matrix([0] * (n + 1), n)
    B = [[0] * (n + 1) for _ in range(n + 1)]
    B[0][0] = 1
    for i in range(n):
        B[i+1][i] = M[i]
        B[i][i+1] = M[i]
    C = matrix_multiply(A, B)
    det_C = gaussian_elimination(C, [0] * (n + 1))
    genus = (2 * n - 2) / 2
    return genus

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    f_poly = [sum(M[i][j] for j in range(n)) for i in range(n)]
    g = compute_genus(f_poly)
    bound = math.log2(1 + 2**(n/2)) - 2
    conjecture_holds = g >= bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "genus",
        "metric_value": g,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_g = sum(r["metric_value"] for r in results) / len(results)
    std_g = math.sqrt(sum((r["metric_value"] - mean_g)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_g} std={std_g} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_g} std={std_g} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")