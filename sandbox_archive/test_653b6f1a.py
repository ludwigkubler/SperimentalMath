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
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda x: abs(A_augmented[x][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        for j in range(i + 1, n):
            factor = -A_augmented[j][i] / A_augmented[i][i]
            A_augmented[j] = [A_augmented[j][k] + factor * A_augmented[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i + 1, n))) / A_augmented[i][i]
    return x

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_sub(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def hodge_order(CNF, n):
    m = len(CNF)
    A = [[0] * (n + 1) for _ in range(m)]
    b = [0] * m
    for i in range(m):
        for j in range(n):
            if CNF[i][j] == -1:
                A[i][j] = 1
            elif CNF[i][j] == 1:
                A[i][j + n] = 1
        b[i] = 1
    x = gaussian_elimination(A, b)
    return sum(abs(x[i]) for i in range(n))

def dpll_width(CNF):
    def dpll(clauses, assignment, literals):
        if not clauses:
            return len(assignment)
        p = next(lit for lit in literals if all(lit not in clause and -lit not in clause for clause in clauses))
        pos_clauses = [clause for clause in clauses if p in clause]
        neg_clauses = [clause for clause in clauses if -p in clause]
        return max(dpll(pos_clauses, assignment + [p], literals), dpll(neg_clauses, assignment + [-p], literals))
    return dpll(CNF, [], list(range(1, n + 1)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    CNF = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(10, 30))]
    hord_values = [hodge_order(CNF, n) for _ in range(30)]
    w_DPLL_values = [dpll_width(CNF) for _ in range(30)]
    mean_hord = sum(hord_values) / len(hord_values)
    mean_w_DPLL = sum(w_DPLL_values) / len(w_DPLL_values)
    corr_coeff = sum((hord_values[i] - mean_hord) * (w_DPLL_values[i] - mean_w_DPLL) for i in range(len(hord_values))) / len(hord_values)
    abs_diff_mean = abs(mean_hord - mean_w_DPLL)
    conjecture_holds = corr_coeff >= 0.8 and abs_diff_mean <= 3
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(hord_values),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"corr_coeff={corr_coeff}, abs_diff_mean={abs_diff_mean}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")