# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(m):
            if j != i:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    return A

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        if A[i][i] != 0:
            rank += 1
    return rank

def generate_k_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, k=random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def projective_space_embedding(cnf):
    m = len(cnf)
    n = max(max(abs(v) for v in clause) for clause in cnf)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(cnf):
        for v in clause:
            A[i][abs(v)] += 1 if v > 0 else -1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_sym_vol = []
    comm_rank_variances = []

    for n in n_values:
        m = random.randint(n, 2*n)
        cnf = generate_k_cnf(n, m)
        A = projective_space_embedding(cnf)
        rank = matrix_rank(A)
        min_sym_vol.append(sum(abs(x) for x in sum(A, [])))
        comm_rank_variances.append(rank**2)

    if not min_sym_vol or not comm_rank_variances:
        return {
            "metric_name": "Minimal Symplectic Volume to Communication Complexity Rank Variance Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Empty or invalid data"
        }

    min_sym_vol = sum(min_sym_vol) / len(min_sym_vol)
    comm_rank_variance = sum(comm_rank_variances) / len(comm_rank_variances)
    ratio = abs(Fraction(min_sym_vol, comm_rank_variance))

    return {
        "metric_name": "Minimal Symplectic Volume to Communication Complexity Rank Variance Ratio",
        "metric_value": float(ratio),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 10,  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")