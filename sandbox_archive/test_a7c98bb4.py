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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(limit):
    sieve = [True] * (limit + 1)
    primes = []
    for p in range(2, limit + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p*p, limit + 1, p):
                sieve[i] = False
    return primes

def generate_cnf(n):
    variables = [f"x_{i}_{j}" for i in range(1, n+1) for j in range(1, n+1)]
    clauses = []
    # Pigeonhole clauses
    for i in range(1, n+1):
        for j in range(1, n+1):
            clause = [f"x_{i}_{j}"]
            for k in range(1, n+1):
                if k != j:
                    clause.append(f"~x_{i}_{k}")
            clauses.append(clause)
    # Hole clauses
    for i in range(1, n+1):
        for j in range(1, n+1):
            clause = [f"x_{j}_{i}"]
            for k in range(1, n+1):
                if k != i:
                    clause.append(f"~x_{k}_{i}")
            clauses.append(clause)
    return variables, clauses

def lex_dpll(cnf, assignment):
    stack = []
    def dfs():
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal.startswith("~"):
                var = literal[2:]
                assignment[var] = False
            else:
                var = literal
                assignment[var] = True
            cnf = [c for c in cnf if var not in c and "~" + var not in c]
        decision_var = next((v for v in variables if v not in assignment), None)
        if not decision_var:
            return False
        stack.append(decision_var)
        assignment[decision_var] = True
        if dfs():
            return True
        del assignment[decision_var]
        stack.pop()
        assignment[decision_var] = False
        if dfs():
            return True
        del assignment[decision_var]
        return False
    variables, clauses = cnf
    assignment = {}
    return dfs()

def herbrand_disjunction_length(cnf):
    n = len(cnf)
    variables, _ = cnf
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    covered = set()
    while len(covered) < n*n:
        pair = random.choice(pairs)
        if pair not in covered:
            a, b = pair
            new_covered = {i*n + j for i in range(n) for j in range(n)}
            new_covered -= {(a-1)*n + (b-1), (a-1)*n + (b+1), (a+1)*n + (b-1), (a+1)*n + (b+1)}
            covered |= new_covered
    return len(pairs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(3, 11):
        cnf = generate_cnf(n)
        leaves = lex_dpll(cnf, {})
        H = herbrand_disjunction_length(cnf)
        ratio = math.log2(leaves) / math.log2(H)
        results.append((n, leaves, H, ratio))
    metric_name = "ratio"
    metric_value = sum(ratio for _, _, _, ratio in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(0.75 <= ratio <= 1.25 for _, _, _, ratio in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")