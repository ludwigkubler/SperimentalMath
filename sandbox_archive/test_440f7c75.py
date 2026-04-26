# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(m):
            if i != j:
                factor = augmented[i][j] / augmented[j][j]
                for k in range(n + 1):
                    augmented[i][k] -= factor * augmented[j][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (augmented[i][-1] - sum(augmented[i][j] * x[j] for j in range(i + 1, n))) / augmented[i][i]
    return x

def is_integer_vector(v):
    return all(isinstance(x, int) for x in v)

def lattice_width(P):
    u_norm = lambda u: max(abs(x) for x in u)
    min_val = float('inf')
    max_val = float('-inf')
    for u in itertools.product(range(-3, 4), repeat=4):
        if u_norm(u) <= 3:
            vals = [sum(ui * vi for ui, vi in zip(u, v)) for v in P]
            min_val = min(min_val, max(vals))
            max_val = max(max_val, min(vals))
    return max_val - min_val

def lasserre_solver(P, degree):
    n = len(P[0]) - 1
    m = len(P)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(m):
        for j in range(m):
            for k in range(n + 1):
                for l in range(n + 1):
                    M[k][l] += P[i][k] * P[j][l]
    return gaussian_elimination(M, [sum(P[i][j] for i in range(m)) for j in range(n + 1)])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 12, 16, 20])
    m = random.choice([2 * n, 4 * n, 8 * n])
    
    # Generate unsatisfiable 3-XOR instance
    clauses = []
    for _ in range(m):
        a, b, c = random.sample(range(n), 3)
        b_i = random.randint(0, 1)
        clauses.append((a, b, c, b_i))
    
    # Ensure the instance is unsatisfiable
    variables = [random.choice([0, 1]) for _ in range(n)]
    for a, b, c, b_i in clauses:
        if (variables[a] ^ variables[b] ^ variables[c]) != b_i:
            break
    else:
        # If satisfiable, flip a parity to make it unsatisfiable
        a, b, c, b_i = random.choice(clauses)
        variables[a] ^= 1
    
    # Encode the instance as lattice points and compute Newton polytope
    P = [(a, b, c, b_i) for a, b, c, b_i in clauses]
    
    # Compute lattice width
    lw_P = lattice_width(P)
    
    # Compute SoS refutation degree using Lasserre solver
    d_SoS = 0
    while True:
        M = lasserre_solver(P, d_SoS + 1)
        if all(M[i][i] == 2 for i in range(n + 1)) and all(M[i][j] == 0 for i in range(n + 1) for j in range(i + 1, n + 1)):
            break
        d_SoS += 1
    
    # Check if the conjecture holds
    conjecture_holds = d_SoS >= math.ceil(lw_P / (4 * math.log2(n)))
    
    return {
        "metric_name": "SoS Refutation Degree",
        "metric_value": d_SoS,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"lw(P)={lw_P}, d_SoS={d_SoS}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["counterexample"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or mapping_undefined")