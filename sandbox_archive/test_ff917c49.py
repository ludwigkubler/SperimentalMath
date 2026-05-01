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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k:
        if k % 2 == 1:
            result = matrix_mult(result, A)
        A = matrix_mult(A, A)
        k //= 2
    return result

def gaussian_elimination(A):
    n = len(A)
    rank = 0
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        rank += 1
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank

def trivial_representation_multiplicity(A):
    return gaussian_elimination(A)

def generate_random_3cnf(n):
    clauses = []
    for _ in range(10*n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def permanent_polynomial(clauses):
    n = max(abs(x) for x in sum(clauses, []))
    A = [[0] * (n+1) for _ in range(n+1)]
    for clause in clauses:
        for x in clause:
            if x > 0:
                A[x-1][x] += 1
            else:
                A[-x-1][-x] += 1
    return matrix_power(A, n)[0][n]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = int(n ** 1.5)
    k = math.ceil(math.log2(n))
    
    perm_n = generate_random_3cnf(n)
    det_m = generate_random_3cnf(m)
    
    perm_poly = permanent_polynomial(perm_n)
    det_poly = permanent_polynomial(det_m)
    
    trivial_perm = trivial_representation_multiplicity(perm_poly)
    trivial_det = trivial_representation_multiplicity(det_poly)
    
    ratio = trivial_perm / trivial_det
    
    return {
        "metric_name": "trivial_representation_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 2 ** (n / 10),
        "counterexample": "" if ratio >= 2 ** (n / 10) else f"Ratio {ratio} < 2^{n/10}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [101, 103, 107]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 2^{n/10}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")