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
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            if not is_d_regular(G):
                continue

            φ_G = construct_tseitin_formula(G)
            G1_phi_G = compute_G1_phi_G(φ_G)
            w_phi_G = compute_resolution_width(φ_G)

            metric_values.append(abs(G1_phi_G))
            instances_tested += 1
            n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "G^1(φ_G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    R2 = calculate_R2(metric_values, [w_phi_G for _ in range(len(metric_values))])
    if R2 < 0.95:
        conjecture_holds = False
        counterexample = f"R²={R2} < 0.95"

    return {
        "metric_name": "G^1(φ_G)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def is_d_regular(G):
    d = sum(sum(row) for row in G)
    return all(sum(row) == d for row in G)

def construct_tseitin_formula(G):
    n = len(G)
    variables = [f"x{i}" for i in range(n)]
    clauses = []

    # Clause for each row
    for i in range(n):
        clause = []
        for j in range(n):
            if G[i][j] == 1:
                clause.append(variables[j])
        clauses.append(clause)

    return variables, clauses

def compute_G1_phi_G(φ_G):
    # Placeholder for actual computation
    return random.randint(0, 100)

def compute_resolution_width(φ_G):
    # Placeholder for actual computation
    return random.randint(50, 200)

def calculate_R2(y_true, y_pred):
    n = len(y_true)
    mean_y_true = sum(y_true) / n
    ss_tot = sum((y - mean_y_true) ** 2 for y in y_true)
    ss_res = sum((y_true[i] - y_pred[i]) ** 2 for i in range(n))
    return 1 - (ss_res / ss_tot)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R² too low\" first_failing_seed={first_failing_seed}")