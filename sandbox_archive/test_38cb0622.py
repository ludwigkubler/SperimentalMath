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

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= mod
    return C

def matrix_pow(A, p, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        p //= 2
    return result

def char_poly(P, n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    poly = [1]
    for i in range(1, n+1):
        P_i = matrix_pow(P, i, 2**31-1)
        det = 0
        for perm in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in zip(perm, sorted(perm)))
            minor = [[P_i[i][j] for j in range(n) if j not in perm] for i in range(n) if i not in perm]
            det += sign * P_i[0][0] * matrix_det(minor)
        poly.append(-det % 2**31-1)
    return poly

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        minor = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1)**j * A[0][j] * matrix_det(minor)
    return det

def eichler_series(P, n):
    series = [1]
    for k in range(1, n+1):
        P_k = matrix_pow(P, k, 2**31-1)
        term = sum(P_k[i][j] * (i + j) % 2 for i in range(n) for j in range(n)) / n
        series.append(term)
    return series

def modular_function(φ):
    P = [[0 if i != j else 1 for j in range(len(φ))] for i in range(len(φ))]
    for i, clause in enumerate(φ):
        for var in clause:
            if var > 0:
                P[i][var-1] += 1
            else:
                P[i][-var-1] -= 1
    return char_poly(P, len(φ))

def dpll_search_tree_height(φ):
    def dfs(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)-1] = literal > 0
            return 1 + dfs([c for c in clauses if literal not in c], new_assignment)
        pure_literals = [l for l in range(1, len(clauses)+1) if sum(c.count(l) - c.count(-l) for c in clauses) != 0]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal-1] = literal > 0
            return 1 + dfs([c for c in clauses if literal not in c], new_assignment)
        lits = [l for c in clauses for l in c if l not in assignment]
        literal = random.choice(lits)
        new_assignment = assignment.copy()
        new_assignment[abs(literal)-1] = literal > 0
        return 1 + max(dfs([c for c in clauses if literal not in c], new_assignment), dfs([c for c in clauses if -literal not in c], new_assignment))
    return dfs(φ, [False] * len(φ))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    φ = [[random.choice([-1, 1]) for _ in range(random.randint(1, n))] for _ in range(n)]
    N_root = len(set(modular_function(φ)))
    h = dpll_search_tree_height(φ)
    return {
        "metric_name": "N_root vs h",
        "metric_value": float(N_root),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": N_root == h,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")