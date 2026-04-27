# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    while len(clauses) < m:
        clause = set(random.sample(variables, 3))
        if all(len(set(c).intersection(F)) == 0 for F in clauses):
            clauses.append(tuple(sorted(clause)))
    return clauses

def lex_dpll(F, assignment=None):
    if assignment is None:
        assignment = {}
    if len(assignment) == len(F[0]):
        return True
    var = next(v for v in range(1, len(F[0]) + 1) if v not in assignment)
    for val in [-1, 1]:
        assignment[var] = val
        if lex_dpll(F, assignment):
            return True
        del assignment[var]
    return False

def beck_fiala_slack(F):
    n = len(F[0])
    m = len(F)
    H_F = [[] for _ in range(m)]
    for i, clause in enumerate(F):
        for var in clause:
            H_F[i].append(var)

    def lp_solve(A, b):
        A_t = list(zip(*A))
        pseudo_inv = [[sum(a * b for a, b in zip(row, col)) / sum(a**2 for a in row) if any(b != 0 for b in col) else 0 for col in A_t] for row in A]
        return [sum(pseudo_inv[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]

    def max_discrepancy(chi):
        max_disc = 0
        for S in range(1 << n):
            disc = sum(chi[i] if (S >> i) & 1 else -chi[i] for i in range(n))
            if abs(disc) > max_disc:
                max_disc = abs(disc)
        return max_disc

    chi = [0] * m
    while True:
        A = []
        b = []
        for i, clause in enumerate(F):
            A.append([1 if var in clause else 0 for var in range(n)])
            b.append(0)
        slack = lp_solve(A, b)
        max_slack = max(slack)
        if max_slack <= 2:
            break
        for i, s in enumerate(slack):
            if abs(s) == max_slack:
                chi[i] = -1 if random.random() < 0.5 else 1
                break

    return max_discrepancy(chi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 14, 16, 18, 20]
    alpha_values = [4.0, 4.5, 5.0, 5.5]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = int(n * alpha)
        F = generate_3cnf(n, m)
        if not lex_dpll(F):
            continue
        delta_F = beck_fiala_slack(F)
        L_DPLL_F = 0
        while True:
            assignment = {}
            if lex_dpll(F, assignment):
                L_DPLL_F += 1
            else:
                break
        instances_tested += 1
        gap = math.log2(L_DPLL_F) - delta_F / 3 + 1
        if gap < -0.5:
            conjecture_holds = False
            counterexample = f"n={n}, alpha={alpha}, L_DPLL(F)={L_DPLL_F}, delta(F)={delta_F}"
            break

    return {
        "metric_name": "gap",
        "metric_value": gap,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["gap"] >= 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(r["gap"] < -0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["gap"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")