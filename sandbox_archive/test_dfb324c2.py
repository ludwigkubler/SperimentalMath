# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_rank(matrix):
    if not matrix:
        return 0
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for col in range(m):
        pivot = -1
        for row in range(rank, n):
            if matrix[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_val = matrix[rank][col]
        for j in range(col, m):
            matrix[rank][j] = Fraction(matrix[rank][j], pivot_val)
        for i in range(n):
            if i != rank and matrix[i][col] != 0:
                factor = matrix[i][col]
                for j in range(col, m):
                    matrix[i][j] -= factor * matrix[rank][j]
        rank += 1
    return rank

def generate_nw_design(n, M, seed):
    random.seed(seed)
    variables = [(i, j) for i in range(n) for j in range(n)]
    k = math.ceil(math.log2(n))
    design = []
    attempts = 0
    max_attempts = 1000
    while len(design) < M and attempts < max_attempts:
        subset = random.sample(variables, n)
        valid = True
        for S in design:
            if len(set(S) & set(subset)) > k:
                valid = False
                break
        if valid:
            design.append(subset)
        attempts += 1
    if len(design) < M:
        return None
    return design

def generate_perm_n(n):
    variables = [(i, j) for i in range(n) for j in range(n)]
    perm = {}
    for perm_indices in itertools.permutations(range(n)):
        monomial = tuple(variables[i * n + j] for i, j in enumerate(perm_indices))
        perm[monomial] = 1 if sum(perm_indices[i] < perm_indices[j] for i in range(n) for j in range(i+1, n)) % 2 == 0 else -1
    return perm

def generate_padded_det(n, m, seed):
    random.seed(seed)
    variables = [(i, j) for i in range(n) for j in range(n)]
    L = [[random.randint(0, n-1) for _ in range(m)] for _ in range(m)]
    linear_forms = [random.randint(0, n-1) for _ in range(n - m)]
    padded_det = {}
    for term in itertools.product(range(m), repeat=m):
        if len(set(term)) < m:
            continue
        monomial = tuple(variables[i * n + L[i][term[i]]] for i in range(m))
        sign = 1 if sum(term[i] < term[j] for i in range(m) for j in range(i+1, m)) % 2 == 0 else -1
        padded_det[monomial] = sign
    for term in itertools.product(range(n), repeat=n-m):
        monomial = tuple(variables[i * n + term[i]] for i in range(n - m))
        padded_det[monomial] = 1
    return padded_det

def restrict_polynomial(poly, subset):
    restricted = {}
    subset_set = set(subset)
    for monomial, coeff in poly.items():
        if all(var in subset_set for var in monomial):
            restricted[monomial] = coeff
    return restricted

def compute_rho_D(poly, design):
    restrictions = [restrict_polynomial(poly, S) for S in design]
    variables = set()
    for r in restrictions:
        variables.update(var for monomial in r for var in monomial)
    variables = sorted(variables)
    var_to_idx = {var: i for i, var in enumerate(variables)}
    matrix = []
    for r in restrictions:
        row = [0] * len(variables)
        for monomial, coeff in r.items():
            idx = 0
            for var in monomial:
                idx = idx * len(variables) + var_to_idx[var]
            row[idx] += coeff
        matrix.append(row)
    return matrix_rank(matrix)

def run_trial(seed):
    n_values = [4, 5, 6]
    M_values = [n, int(n**1.25), int(n**1.5)]
    results = []
    for n in n_values:
        for M in M_values:
            if M < n or M > n**1.5:
                continue
            design = generate_nw_design(n, M, seed)
            if design is None:
                continue
            perm_n = generate_perm_n(n)
            m = int(n**1.5)
            padded_det = generate_padded_det(n, m, seed)
            rho_perm = compute_rho_D(perm_n, design)
            rho_pad = compute_rho_D(padded_det, design)
            gap = rho_perm - rho_pad
            conjecture_holds = (rho_perm >= 0.5 * M) and (rho_pad <= 4 * m * math.log2(n)) and (gap > 0)
            counterexample = ""
            if not conjecture_holds:
                if rho_perm < 0.5 * M:
                    counterexample = f"rho_perm={rho_perm} < 0.5*M={0.5*M}"
                elif rho_pad > 4 * m * math.log2(n):
                    counterexample = f"rho_pad={rho_pad} > 4*m*log2(n)={4*m*math.log2(n)}"
                else:
                    counterexample = f"gap={gap} <= 0"
            results.append({
                "n": n,
                "M": M,
                "rho_perm": rho_perm,
                "rho_pad": rho_pad,
                "gap": gap,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    if not results:
        return {
            "metric_name": "gap",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "design_generation_failed"
        }
    avg_gap = sum(r["gap"] for r in results) / len(results)
    all_hold = all(r["conjecture_holds"] for r in results)
    first_counterexample = next((r for r in results if not r["conjecture_holds"]), None)
    return {
        "metric_name": "gap",
        "metric_value": avg_gap,
        "instances_tested": len(results),
        "conjecture_holds": all_hold,
        "counterexample": first_counterexample["counterexample"] if first_counterexample else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    holds_counts = 0
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            holds_counts += 1
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = holds_counts / len(seeds)
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={seeds[holds_counts]}")