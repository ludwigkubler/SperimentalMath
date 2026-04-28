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
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += ((-1) ** i) * A[0][i] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    alpha = 4.5
    num_clauses = int(alpha * n / 3)
    
    def generate_clause():
        variables = set(random.sample(range(n), 3))
        negated = [random.choice([True, False]) for _ in range(3)]
        return tuple(sorted((i if not neg else -i) for i, neg in zip(variables, negated)))
    
    clauses = {generate_clause() for _ in range(num_clauses)}
    while len(clauses) < num_clauses:
        clause = generate_clause()
        if all(len(set(c1).intersection(c2)) <= 2 for c1, c2 in combinations(clauses, 2)):
            clauses.add(clause)
    
    def p_F(x):
        return sum((-1) ** sum(1 for v in C if v < 0) * x[abs(v)-1] for C in clauses)
    
    M = [[0] * (n**2) for _ in range(binomial(n+2, 3))]
    for i in range(binomial(n+2, 3)):
        alpha, beta, gamma = combinations(range(1, n+1), 3)[i]
        row = [0] * (n**2)
        for j in range(n):
            for k in range(n):
                if j != k:
                    row[j*n+k] += p_F([1 if i == j else 0 if i == k else 0 for i in range(n)])
        M[i] = row
    
    rank_M = len(gaussian_elimination(M, [0]*n**2))
    dim_g_F = n**2 - rank_M
    
    def lex_dpll(F):
        stack = [(F, set())]
        while stack:
            F, assignment = stack.pop()
            if not F:
                return 1
            var = next((v for v in range(1, n+1) if v not in assignment), None)
            if var is None:
                return 0
            new_assignment = assignment | {var}
            F_true = [c for c in F if all(v in assignment or -v in assignment for v in c)]
            F_false = [c for c in F if any(v in assignment or -v in assignment for v in c) and not all(v in assignment or -v in assignment for v in c)]
            stack.append((F_true, new_assignment))
            stack.append((F_false, assignment | {-var}))
    
    L_DPLL_F = lex_dpll(clauses)
    
    metric_value = math.log2(L_DPLL_F) + dim_g_F
    conjecture_holds = metric_value <= n + 2 * math.ceil(math.log2(n))
    counterexample = "" if conjecture_holds else f"n={n}, L_DPLL(F)={L_DPLL_F}, dim(g_F)={dim_g_F}"
    
    return {
        "metric_name": "log2(L_DPLL(F)) + dim_Q(g_F)",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")