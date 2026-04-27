# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(b)
    Ab = [A[i] + [b[i]] for i in range(n)]
    Ab = gaussian_elimination(Ab)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i][-1] - sum(Ab[i][j] * x[j] for j in range(i + 1, n))) / Ab[i][i]
    return x

def beck_fiala_slack(H):
    m = len(H)
    n = len(H[0])
    chi = [0] * m
    while True:
        changed = False
        for i in range(m):
            if abs(sum(chi[j] for j in H[i])) > 2 * (m // 2) - 1:
                chi[i] = 1 if sum(chi[j] for j in H[i]) > 0 else -1
                changed = True
        if not changed:
            break
    return max(abs(sum(chi[j] for j in H[i])) for i in range(m))

def lex_dpll(F, assignment):
    n = len(assignment)
    for clause in F:
        if all(not (x == 1 and literal < 0) and not (x == -1 and literal > 0) for x, literal in zip(assignment, clause)):
            return False
    if all(x != 0 for x in assignment):
        return True
    var = next(i for i, x in enumerate(assignment) if x == 0)
    assignment[var] = 1
    if lex_dpll(F, assignment):
        return True
    assignment[var] = -1
    if lex_dpll(F, assignment):
        return True
    assignment[var] = 0
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 14, 16, 18, 20]
    alpha_values = [4.0, 4.5, 5.0, 5.5]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for alpha in alpha_values:
            m = int(n * alpha)
            F = []
            while len(F) < m:
                clause = [random.randint(1, n), random.randint(-n, -1)]
                if all(clause[i] not in F[j] for j in range(len(F))):
                    F.append(clause)
            assignment = [0] * n
            if lex_dpll(F, assignment):
                continue
            H = [[i + 1 for i, literal in enumerate(clause) if literal == var or literal == -var] for clause in F for var in range(1, n + 1)]
            delta_F = beck_fiala_slack(H)
            log2_L_DPLL = math.log2(sum(1 for _ in lex_dpll(F, [0] * n)))
            gap = log2_L_DPLL - delta_F / 3 + 1
            instances_tested += 1
            if gap < -0.5:
                conjecture_holds = False
                counterexample = f"n={n}, alpha={alpha}, m={m}"
                break
    
    return {
        "metric_name": "gap",
        "metric_value": log2_L_DPLL - delta_F / 3 + 1,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["gap_i"] >= 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(r["gap_i"] < -0.5 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["gap_i"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")