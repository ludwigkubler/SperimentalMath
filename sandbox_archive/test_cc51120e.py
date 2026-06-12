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

def mod_inv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Modular inverse does not exist")

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_pow(A, k, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        k //= 2
    return result

def dpll_width(phi):
    stack = []
    assignment = {}
    for clause in phi:
        if all(lit in assignment and assignment[lit] == True for lit in clause):
            continue
        elif any(lit in assignment and assignment[lit] == False for lit in clause):
            return 0
        else:
            var = next(lit for lit in clause if lit not in assignment)
            stack.append((phi, assignment.copy()))
            assignment[var] = True
            phi = [c for c in phi if var not in c and -var not in c]
            assignment[-var] = False
            phi = [c for c in phi if -var not in c and var not in c]
    return 1 + max(dpll_width(phi) for phi, _ in stack)

def tseitin_transform(phi):
    n = len(phi)
    literals = set()
    for clause in phi:
        literals.update(clause)
    m = len(literals)
    T = [[0] * (n + m + 1) for _ in range(n + m + 1)]
    for i, lit in enumerate(literals):
        T[i][i + n] = 1
        T[n + i][-1] = -1
    for i, clause in enumerate(phi):
        T[-1][n + i] = 1
        for lit in clause:
            T[i + n][abs(lit) - 1] = 1 if lit > 0 else -1
    return T

def hord(T):
    n = len(T)
    mod = 2**31 - 1
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A = matrix_mul(I, T, mod)
    B = matrix_pow(A, n - 1, mod)
    det = sum(B[i][i] for i in range(n))
    return abs(det) % mod

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.choice([-1, 1]) * (i + 1) for _ in range(random.randint(2, n))] for _ in range(n)]
    T = tseitin_transform(phi)
    hord_value = hord(T)
    width = dpll_width(phi)
    return {
        "metric_name": "hord_vs_dpll",
        "metric_value": abs(hord_value - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(hord_value - width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"hord_vs_dpll\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")