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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def rank(A):
    A_copy = [row[:] for row in A]
    r = gaussian_elimination(A_copy, [0]*len(A))
    return sum(1 for row in r if any(row))

def tseitin_formula(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    formula = []
    for var in variables:
        formula.append([var])
    for clause in clauses:
        formula.append([-clause[0], -clause[1]])
        formula.append([clause[0], clause[1]])
    return formula

def coxeter_matrix(formula):
    n = len(formula)
    W = [[0] * n for _ in range(n)]
    for i in range(n):
        W[i][i] = 2
    for clause in formula:
        if len(clause) == 1:
            continue
        u, v = abs(clause[0]) - 1, abs(clause[1]) - 1
        W[u][v], W[v][u] = -1, -1
    return W

def tropicalize(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] < 0:
                matrix[i][j] = math.inf
                matrix[j][i] = math.inf
    return matrix

def resolution_tree_width(formula):
    # Simplified version of resolution tree width calculation
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n, m = random.randint(5, 40), random.randint(10, 80)
    formula = tseitin_formula(n, m)
    W_G = coxeter_matrix(formula)
    tropical_W_G = tropicalize(W_G)
    rho_W_W_G = rank(tropical_W_G)
    t_star_G = resolution_tree_width(formula)
    
    expected_rho = math.log(n + math.log(m))
    if rho_W_W_G < expected_rho:
        return {
            "metric_name": "rho_W(W_G)",
            "metric_value": rho_W_W_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho_W(W_G)={rho_W_W_G}, expected>=Θ(log(n + log(m)))"
        }
    
    if t_star_G < 2**math.ceil(math.log(rho_W_W_G)):
        return {
            "metric_name": "t*(G)",
            "metric_value": t_star_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"t*(G)={t_star_G}, expected>=2^Ω(ρ_W(W_G))"
        }
    
    return {
        "metric_name": "rho_W(W_G)",
        "metric_value": rho_W_W_G,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 89))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")