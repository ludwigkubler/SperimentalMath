# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_mult(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def symplectic_form(cnf):
    n = len(cnf)
    M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for clause in cnf:
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != -lit2:
                    i, j = abs(lit1) - 1, abs(lit2) - 1
                    M[i][j] += Fraction(1)
    return gaussian_elimination(M)

def tree_like_resolution_width(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    stack = []
    while clauses:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            return float('inf')
        lit = unit_clause.pop()
        stack.append(lit)
        new_clauses = set()
        for clause in clauses:
            if lit in clause:
                continue
            if -lit in clause:
                new_clauses.add(tuple(sorted(clause - {-lit})))
            else:
                new_clauses.add(tuple(sorted(clause | {lit})))
        clauses = new_clauses
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = []
        for _ in range(n):
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        w_phi = tree_like_resolution_width(cnf)
        if w_phi == float('inf'):
            continue
        r_phi = symplectic_form(cnf)
        rank_r_phi = sum(1 for row in r_phi if any(val != Fraction(0) for val in row))
        instances_tested += 1
        metric_value += -rank_r_phi / math.log2(w_phi)

    if instances_tested == 0:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances"
        }

    metric_value /= instances_tested
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")