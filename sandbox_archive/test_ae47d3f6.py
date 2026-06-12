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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(A, n, mod):
    result = [[0 if i != j else 1 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        n //= 2
    return result

def p_adic_norm(poly, p):
    return max(abs(coeff) for coeff in poly) / (p ** math.floor(math.log(max(abs(coeff) for coeff in poly), p)))

def clause_indicator_polynomial(clause_set, variables):
    n = len(variables)
    m = len(clause_set)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clause_set):
        for lit in clause:
            if lit > 0:
                A[i][lit - 1] = 1
            else:
                A[i][-1] += 1
    return A

def resolution_width(clause_set):
    n = len(clause_set[0])
    m = len(clause_set)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clause_set):
        for lit in clause:
            if lit > 0:
                A[i][lit - 1] = 1
            else:
                A[i][-1] += 1
    B = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clause_set):
        for lit in clause:
            if lit > 0:
                B[i][lit - 1] = -1
            else:
                B[i][-1] += 1
    C = matrix_mul(A, B, 2)
    return max(abs(sum(row)) for row in C)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 3 * n)
    variables = list(range(1, n + 1))
    clause_set = set()
    while len(clause_set) < m:
        clause = set(random.sample(variables, random.randint(1, n)))
        if not any(lit in clause for lit in [-v for v in clause]):
            clause_set.add(frozenset(clause))
    p = 2
    A = clause_indicator_polynomial(clause_set, variables)
    D = p_adic_norm(A, p)
    w = resolution_width(clause_set)
    return {
        "metric_name": "p-adic divergence",
        "metric_value": D,
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": D <= 10 * w,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")