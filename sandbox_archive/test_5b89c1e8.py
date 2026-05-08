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

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_multiply(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_rank(A, mod):
    n = len(A)
    rank = 0
    for i in range(n):
        if A[i][i]:
            for j in range(i+1, n):
                factor = (A[j][i] * mod_inverse(A[i][i], mod)) % mod
                for k in range(n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
            rank += 1
    return rank

def generate_polynomial(N, d, variables):
    if d == 0:
        return {(): Fraction(1)}
    elif d == 1:
        return {(var,): random.choice([Fraction(-1), Fraction(1)]) for var in variables}
    else:
        result = {}
        for i in range(len(variables)):
            new_vars = variables[:i] + variables[i+1:]
            for term, coeff in generate_polynomial(N, d-1, new_vars).items():
                result[(variables[i],) + term] = coeff * random.choice([Fraction(-1), Fraction(1)])
        return result

def expand_polynomial(poly):
    n = len(poly)
    expanded = {}
    for term, coeff in poly.items():
        monomial = 1
        for var, exp in term:
            monomial *= var**exp
        expanded[monomial] = coeff
    return expanded

def compute_rLS(f, N):
    x = [Fraction(0)] * N
    df = [(sum(coeff * var**(exp-1) for var, exp in term.items()) for term, coeff in f.items()) for _ in range(N)]
    A = [[0] * (N**2) for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                A[i][j*N + k] = df[j][i] * x[k]
    return N**2 - 1 - matrix_rank(A, mod=10007)

def generate_formulas(N, d, s):
    variables = [Fraction(1)] * N
    formulas = []
    for _ in range(s):
        formula = generate_polynomial(N, d, variables)
        if all(coeff != Fraction(0) for coeff in formula.values()):
            formulas.append(formula)
    return formulas

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for N, d in [(4, 3), (6, 3), (6, 4), (9, 3)]:
        for s in [3, 5, 8, 12, 16, 24, 32]:
            formulas = generate_formulas(N, d, s)
            for formula in formulas:
                f = expand_polynomial(formula)
                rLS = compute_rLS(f, N)
                results.append((s, rLS))
    max_diff = max(rLS - 4 * s for s, rLS in results)
    conjecture_holds = max_diff <= 0
    counterexample = "" if conjecture_holds else f"max_diff={max_diff}"
    return {
        "metric_name": "rLS - 4s",
        "metric_value": max_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample='max_diff={max(r['metric_value'] - 4 * s for s, rLS in results)}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data to make a definitive conclusion")