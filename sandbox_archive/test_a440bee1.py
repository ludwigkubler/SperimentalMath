# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

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
    n = len(matrix)
    if n == 0:
        return 0
    rank = 0
    for col in range(n):
        if rank >= n:
            break
        pivot = rank
        while pivot < n and matrix[pivot][col] == 0:
            pivot += 1
        if pivot == n:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for i in range(rank + 1, n):
            factor = matrix[i][col] / matrix[rank][col]
            for j in range(col, n):
                matrix[i][j] -= factor * matrix[rank][j]
        rank += 1
    return rank

def generate_nw_design(n, M, k, seed):
    random.seed(seed)
    design = []
    while len(design) < M:
        S = set(random.sample(range(n * n), n))
        valid = True
        for S_t in design:
            if len(S & S_t) > k:
                valid = False
                break
        if valid:
            design.append(S)
    return design

def generate_perm_n(n):
    variables = [(i, j) for i in range(n) for j in range(n)]
    terms = list(itertools.permutations(range(n)))
    perm = defaultdict(int)
    for term in terms:
        monomial = tuple(variables[i * n + term[i]] for i in range(n))
        perm[monomial] = 1 if sum(1 for i in range(n) if term[i] < i) % 2 == 0 else -1
    return perm

def generate_padded_det(n, m, seed):
    random.seed(seed)
    variables = [(i, j) for i in range(n) for j in range(n)]
    L = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
    det = defaultdict(int)
    for term in itertools.permutations(range(m)):
        sign = 1 if sum(1 for i in range(m) if term[i] < i) % 2 == 0 else -1
        monomial = tuple(variables[i * n + L[i][term[i]]] for i in range(m))
        det[monomial] = sign
    return det

def restrict_poly(poly, S):
    restricted = defaultdict(int)
    for monomial, coeff in poly.items():
        if all(var in S for var in monomial):
            restricted[monomial] = coeff
    return restricted

def compute_rho_D(poly, design):
    restrictions = [restrict_poly(poly, S) for S in design]
    variables = set()
    for r in restrictions:
        variables.update(r.keys())
    variables = sorted(variables)
    var_to_idx = {var: idx for idx, var in enumerate(variables)}
    matrix = []
    for r in restrictions:
        row = [0] * len(variables)
        for var, coeff in r.items():
            row[var_to_idx[var]] = coeff
        matrix.append(row)
    return matrix_rank(matrix)

def run_trial(seed):
    n_values = [4, 5, 6]
    M_values = []
    for n in n_values:
        M_values.append([n, int(n ** 1.25), int(n ** 1.5)])
    results = []
    for n_idx, n in enumerate(n_values):
        for M in M_values[n_idx]:
            k = math.ceil(math.log2(n))
            design = generate_nw_design(n, M, k, seed)
            perm_n = generate_perm_n(n)
            m = int(n ** 1.5)
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
        trials.append({"seed": seed, **result})
        print(f"TRIAL: {trials[-1]}")
    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")