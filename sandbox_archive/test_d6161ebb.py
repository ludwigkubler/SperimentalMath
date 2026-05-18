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

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

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
        for c in range(col, m):
            matrix[rank][c] = Fraction(matrix[rank][c], pivot_val)
        for r in range(n):
            if r != rank and matrix[r][col] != 0:
                factor = matrix[r][col]
                for c in range(col, m):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def build_nw_design(n, M, seed):
    random.seed(seed)
    max_k = math.ceil(math.log2(n))
    design = []
    while len(design) < M:
        S = random.sample(range(n * n), n)
        valid = True
        for S_t in design:
            if len(set(S) & set(S_t)) > max_k:
                valid = False
                break
        if valid:
            design.append(S)
    return design

def perm_n(n):
    variables = [(i, j) for i in range(n) for j in range(n)]
    terms = list(itertools.permutations(variables, n))
    poly = {}
    for term in terms:
        sign = 1
        for i in range(n):
            for j in range(i + 1, n):
                if term[j][0] < term[i][0]:
                    sign *= -1
        poly[term] = sign
    return poly

def random_linear_form(n, seed):
    random.seed(seed)
    coeffs = [random.randint(-10, 10) for _ in range(n * n)]
    variables = [(i, j) for i in range(n) for j in range(n)]
    return sum(coeffs[i] * variables[i] for i in range(n * n))

def det_m(m, n, seed):
    random.seed(seed)
    L = [[random_linear_form(n, seed + i * m + j) for j in range(m)] for i in range(m)]
    det = 0
    for perm in itertools.permutations(range(m)):
        sign = 1
        for i in range(m):
            for j in range(i + 1, m):
                if perm[j] < perm[i]:
                    sign *= -1
        term = sign
        for i in range(m):
            term *= L[i][perm[i]]
        det += term
    return det

def padded_det(n, m, seed):
    random.seed(seed)
    ell = random_linear_form(n, seed)
    det = det_m(m, n, seed + 1)
    return (ell ** (n - m)) * det

def restrict_poly(poly, S):
    restricted = {}
    for term, coeff in poly.items():
        if all((i, j) in S for i, j in term):
            restricted[term] = coeff
    return restricted

def poly_to_matrix(poly, variables):
    matrix = []
    for term, coeff in poly.items():
        row = [0] * len(variables)
        for var in term:
            row[variables.index(var)] += 1
        matrix.append(row)
    return matrix

def run_trial(seed):
    n_values = [4, 5, 6]
    M_values = [n, int(n ** 1.25), int(n ** 1.5)]
    results = []
    for n in n_values:
        for M in M_values:
            if M < n or M > int(n ** 1.5):
                continue
            random.seed(seed)
            design = build_nw_design(n, M, seed)
            perm = perm_n(n)
            m = int(n ** 1.5)
            pad_det = padded_det(n, m, seed)
            variables = [(i, j) for i in range(n) for j in range(n)]
            perm_matrix = []
            pad_det_matrix = []
            for S in design:
                restricted_perm = restrict_poly(perm, S)
                restricted_pad_det = restrict_poly(pad_det, S)
                perm_matrix.extend(poly_to_matrix(restricted_perm, variables))
                pad_det_matrix.extend(poly_to_matrix(restricted_pad_det, variables))
            rho_perm = matrix_rank(perm_matrix)
            rho_pad_det = matrix_rank(pad_det_matrix)
            gap = rho_perm - rho_pad_det
            conjecture_holds = (rho_perm >= 0.5 * M) and (rho_pad_det <= 4 * m * math.log2(n)) and (gap > 0)
            counterexample = ""
            if not conjecture_holds:
                if rho_perm < 0.5 * M:
                    counterexample = f"rho_perm={rho_perm} < 0.5*M={0.5*M}"
                elif rho_pad_det > 4 * m * math.log2(n):
                    counterexample = f"rho_pad_det={rho_pad_det} > 4*m*log2(n)={4*m*math.log2(n)}"
                else:
                    counterexample = f"gap={gap} <= 0"
            results.append({
                "n": n,
                "M": M,
                "rho_perm": rho_perm,
                "rho_pad_det": rho_pad_det,
                "gap": gap,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    metric_value = sum(r["gap"] for r in results) / len(results)
    instances_tested = len(results)
    all_hold = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    return {
        "metric_name": "average_gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all_hold,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        trials.append(result)
    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, t in enumerate(trials) if not t["conjecture_holds"]), -1)
        counterexample = next((t["counterexample"] for t in trials if not t["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")