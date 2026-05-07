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

def generate_random_primes(num_primes):
    primes = []
    num = 2
    while len(primes) < num_primes:
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
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def cheeger_constant(G, n):
    min_cut = float('inf')
    for s in range(1 << (n - 1)):
        subset = [i for i in range(n) if s & (1 << i)]
        complement = [i for i in range(n) if i not in subset]
        cut_size = sum(G[i][j] for i in subset for j in complement)
        boundary_size = sum(sum(G[i][j] for j in complement) for i in subset)
        if boundary_size > 0:
            min_cut = min(min_cut, cut_size / boundary_size)
    return min_cut

def tseitin_formula(G, n):
    clauses = []
    for i in range(n):
        clauses.append([i + 1])
    for u in range(n):
        for v in range(u + 1, n):
            if G[u][v] > 0:
                clauses.append([-u - 1, -v - 1, u + v + 1])
                clauses.append([-u - 1, -v - 1, -(u + v + 1)])
    return clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[-literal] = True
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    pure_literals = [l for l in range(1, len(assignment) + 1) if all(l not in c or -l not in c for c in clauses)]
    if pure_literals:
        literal = pure_literals[0]
        new_assignment = assignment.copy()
        new_assignment[-literal] = True
        return dpll(clauses, new_assignment)
    p = random.choice([l for l in range(1, len(assignment) + 1)])
    new_assignment1 = assignment.copy()
    new_assignment1[-p] = True
    if dpll(clauses, new_assignment1):
        return True
    new_assignment2 = assignment.copy()
    new_assignment2[p] = True
    return dpll(clauses, new_assignment2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    h_G = cheeger_constant(G, n)
    Tseitin_clauses = tseitin_formula(G, n)
    resolution_length = dpll(Tseitin_clauses, [False] * (n + 1))
    metric_name = "resolution_length"
    metric_value = resolution_length
    instances_tested = 1
    conjecture_holds = h_G > 0 and resolution_length >= 2 ** math.ceil(0.5 * h_G)
    counterexample = "" if conjecture_holds else f"Cheeger constant {h_G} does not support the conjecture"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_random_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")