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
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_rank(matrix):
    n = len(matrix)
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

def build_nw_design(n, M, seed):
    random.seed(seed)
    max_intersection = math.ceil(math.log2(n))
    design = []
    attempts = 0
    max_attempts = 1000
    while len(design) < M and attempts < max_attempts:
        subset = random.sample(range(n * n), n)
        valid = True
        for s in design:
            if len(set(subset) & set(s)) > max_intersection:
                valid = False
                break
        if valid:
            design.append(subset)
        attempts += 1
    if len(design) < M:
        return None
    return design

def perm_n(n):
    terms = list(itertools.permutations(range(n)))
    poly = defaultdict(int)
    for term in terms:
        poly[term] = 1 if sum(1 for i in range(n) if term[i] < i) % 2 == 0 else -1
    return poly

def padded_det(n, m, seed):
    random.seed(seed)
    L = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
    ell = [random.randint(0, 1) for _ in range(n * n)]
    poly = defaultdict(int)
    for term in itertools.product(range(2), repeat=n * n):
        if sum(term) == n - m:
            sign = 1
            for i in range(n * n):
                if term[i] == 1:
                    sign *= ell[i]
            det_sign = 1
            for i in range(m):
                for j in range(m):
                    det_sign *= L[i][j]
            poly[term] = sign * det_sign
    return poly

def restrict_poly(poly, S):
    restricted = defaultdict(int)
    for term, coeff in poly.items():
        if all(i in S for i in range(len(term)) if term[i] != 0):
            restricted[term] = coeff
    return restricted

def run_trial(seed):
    n_values = [4, 5, 6]
    M_values = []
    for n in n_values:
        M_values.append([n, int(n**1.25), int(n**1.5)])
    results = []
    for n_idx, n in enumerate(n_values):
        for M in M_values[n_idx]:
            random.seed(seed)
            design = build_nw_design(n, M, seed)
            if design is None:
                continue
            perm = perm_n(n)
            m = int(n**1.5)
            det = padded_det(n, m, seed)
            perm_restrictions = []
            det_restrictions = []
            for S in design:
                perm_restrictions.append(restrict_poly(perm, S))
                det_restrictions.append(restrict_poly(det, S))
            all_terms = set()
            for r in perm_restrictions + det_restrictions:
                all_terms.update(r.keys())
            all_terms = sorted(all_terms)
            term_to_idx = {term: idx for idx, term in enumerate(all_terms)}
            perm_matrix = [[0 for _ in range(len(all_terms))] for _ in range(M)]
            det_matrix = [[0 for _ in range(len(all_terms))] for _ in range(M)]
            for i, r in enumerate(perm_restrictions):
                for term, coeff in r.items():
                    perm_matrix[i][term_to_idx[term]] = coeff
            for i, r in enumerate(det_restrictions):
                for term, coeff in r.items():
                    det_matrix[i][term_to_idx[term]] = coeff
            perm_rank = matrix_rank(perm_matrix)
            det_rank = matrix_rank(det_matrix)
            gap = perm_rank - det_rank
            conjecture_holds = (perm_rank >= 0.5 * M and det_rank <= 4 * m * math.log2(n) and gap > 0)
            counterexample = ""
            if not conjecture_holds:
                counterexample = f"n={n}, M={M}, perm_rank={perm_rank}, det_rank={det_rank}, gap={gap}"
            results.append({
                "n": n,
                "M": M,
                "metric_name": "gap",
                "metric_value": gap,
                "instances_tested": M,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    if not results:
        return {
            "metric_name": "gap",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid design found"
        }
    return results[0]

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    seeds = [int(seed) for seed in seeds]
    metric_values = []
    conjecture_holds = []
    counterexamples = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds.append(result["conjecture_holds"])
        if result["counterexample"]:
            counterexamples.append((seed, result["counterexample"]))
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)
    if counterexamples:
        first_failing_seed, first_counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")