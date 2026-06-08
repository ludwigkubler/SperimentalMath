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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
        return False
    literal = next((l for l in range(1, len(clauses) + 1) if l not in assignment and -l not in assignment), None)
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
        return True
    new_assignment[literal] = False
    if dpll([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
        return True
    return False

def tseitin_formula(G, n):
    m = len(G)
    clauses = []
    for i in range(m):
        for j in range(n):
            clauses.append([-(i * n + j + 1)])
        for j in range(n):
            for k in range(j + 1, n):
                clauses.append([-i * n - j - 1, -i * n - k - 1])
    for i in range(m):
        for j in range(n):
            if G[i][j]:
                clauses.append([i * n + j + 1] + [-(k * n + l + 1) for k, l in enumerate(G[i]) if k != j and G[k][l]])
    return clauses

def minimal_tropical_motivic_rank(clauses):
    m = len(clauses)
    n = max(abs(l) for c in clauses for l in c)
    A = [[0] * (n + 1) for _ in range(m)]
    b = [0] * m
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                A[i][literal - 1] += 1
            else:
                A[i][-1] -= 1
        b[i] = 1
    try:
        x = gaussian_elimination(A, b)
        return max(x[:-1])
    except ZeroDivisionError:
        return math.inf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    G = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = True
        degree = sum(G[i])
        if degree < d:
            j = random.randint(0, n - 1)
            while j == i or G[i][j]:
                j = random.randint(0, n - 1)
            G[i][j] = True
            G[j][i] = True
    clauses = tseitin_formula(G, n)
    mtr_G = minimal_tropical_motivic_rank(clauses)
    w_phi_G = dpll(clauses)
    if not w_phi_G:
        return {
            "metric_name": "mtr/G",
            "metric_value": mtr_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver failed to find a proof"
        }
    ratio = mtr_G / w_phi_G
    return {
        "metric_name": "mtr/G",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")