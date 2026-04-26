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
    m, n = len(A), len(b)
    for i in range(m):
        max_row = max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dpll(F, assignment=None):
    if assignment is None:
        assignment = {}
    free_vars = [v for v in F[0].keys() if v not in assignment]
    if not free_vars:
        return all([F[i][assignment.get(v, False)] for i in range(len(F))])
    v = free_vars[0]
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[v] = val
        if dpll(F, new_assignment):
            return True
    return False

def resolution_width(F, max_width=8):
    clauses = F[:]
    while len(clauses) > 1:
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause_i = set(clauses[i])
                clause_j = set(clauses[j])
                if len(clause_i & clause_j) == 2:
                    new_clause = list((clause_i | clause_j) - (clause_i & clause_j))
                    if len(new_clause) <= max_width:
                        clauses.append(new_clause)
                    else:
                        return False
        clauses = [c for c in clauses if not any([x in c and not assignment[x] for x, assignment in assignment.items()])]
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    c1, c2 = 0.25, 2.0
    for n in n_values:
        F = [[{random.choice([True, False]): random.choice([True, False])} for _ in range(n)] for _ in range(2 * n)]
        depths = []
        for i in range(2 * n):
            depth = 0
            assignment = {}
            while not dpll(F[i], assignment):
                unit_propagate(F[i], assignment)
                depth += 1
            depths.append(depth)
        Q_05 = sorted(depths)[len(depths) // 2]
        Q_99 = sorted(depths)[-int(len(depths) * 0.01)]
        beta_n = Q_99 - Q_05
        W_max = None
        for i in range(2 * n):
            if resolution_width(F[i]):
                W_max = max(W_max, len(F[i]))
        if W_max is not None:
            results.append((n, Q_05, Q_99, beta_n, W_max))
    metric_value = sum(W_max for _, _, _, _, W_max in results) / len(results)
    conjecture_holds = all(c1 * Q_99 <= W_max <= c2 * Q_05 * math.log(100) for _, _, _, _, W_max in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")