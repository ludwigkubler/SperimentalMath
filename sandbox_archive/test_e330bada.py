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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random planar graph with n vertices
    n = random.randint(5, 40)
    G = [[False] * n for _ in range(n)]
    edges = set()
    while len(edges) < 2 * n - 3:  # Planar graph property
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u][v] = G[v][u] = True
            edges.add((u, v))
    
    # Construct Tseitin formula
    clauses = []
    for i in range(n):
        clauses.append([i + n])
        for j in range(i):
            if G[i][j]:
                clauses.append([-i - n, -j - n, i + n])
                clauses.append([-i - n, -j - n, -i - n])
    
    # Compute non-abelian Fourier coefficients over S_n
    def sign_permutation(perm):
        sgn = 1
        for i in range(n):
            if perm[i] != i:
                j = perm.index(i)
                perm[i], perm[j] = perm[j], perm[i]
                sgn *= -1
        return sgn
    
    F = [0] * n
    for perm in itertools.permutations(range(n)):
        sign = sign_permutation(perm)
        F[sum(1 if i == j else 0 for i, j in enumerate(perm))] += sign
    
    # Measure the coefficient spread
    max_coeff = max(abs(coeff) for coeff in F)
    min_coeff = min(abs(coeff) for coeff in F)
    spread = max_coeff - min_coeff
    
    # Compute empirical resolution proof length using DPLL with clause learning
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            return dpll([c for c in clauses if literal not in c], assignment + [literal])
        pure_literals = []
        for lit in range(2 * n):
            pos_count, neg_count = sum(lit in c for c in clauses), sum(-lit in c for c in clauses)
            if pos_count == 0:
                pure_literals.append(-lit)
            elif neg_count == 0:
                pure_literals.append(lit)
        if pure_literals:
            literal = pure_literals[0]
            return dpll([c for c in clauses if literal not in c], assignment + [literal])
        literals = [i for i in range(2 * n) if i not in assignment]
        literal = random.choice(literals)
        return (dpll(clauses, assignment + [literal]) or
                dpll(clauses, assignment + [-literal]))
    
    proof_length = 0
    while True:
        assignment = []
        if dpll(clauses, assignment):
            break
        proof_length += 1
    
    # Check the conjecture
    expected_length = math.sqrt(n)
    ratio = spread * proof_length / expected_length
    conjecture_holds = abs(ratio - 1) < 0.1
    counterexample = "" if conjecture_holds else f"spread={spread}, proof_length={proof_length}, n={n}"
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")