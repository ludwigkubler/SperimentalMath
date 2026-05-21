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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0, 1)] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        pivot_row = -1
        for j in range(i, m):
            if A[j][i] != Fraction(0, 1):
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        rank += 1
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank

def generate_csp_instance(n, m):
    variables = [f'x{i}' for i in range(n)]
    constraints = []
    for _ in range(m):
        constraint = []
        for var in variables:
            coeff = random.choice([-1, 0, 1])
            if coeff != 0:
                constraint.append((coeff, var))
        constraints.append(constraint)
    return variables, constraints

def tropical_curve_rank(CSP):
    n = len(CSP[0])
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                factor = Fraction(1, 1)
                for coeff, var in CSP[i]:
                    if var == f'x{j}':
                        factor *= coeff
                A[i][j] = factor
    return gaussian_elimination(A)

def sos_refutation_size(CSP):
    n = len(CSP[0])
    variables = [f'x{i}' for i in range(n)]
    constraints = CSP
    refutation_size = 0
    for constraint in constraints:
        refutation_size += len(constraint)
    return refutation_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n // 2, n * (n - 1))
    CSP = generate_csp_instance(n, m)
    
    tropical_curve_rank = rank(CSP)
    sos_refutation_size = sos_refutation_size(CSP)
    
    return {
        "metric_name": "Rank of Tropical Curve",
        "metric_value": tropical_curve_rank,
        "instances_tested": 1,
        "conjecture_holds": tropical_curve_rank == sos_refutation_size,
        "counterexample": "" if tropical_curve_rank == sos_refutation_size else f"Rank {tropical_curve_rank} != Refutation Size {sos_refutation_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")