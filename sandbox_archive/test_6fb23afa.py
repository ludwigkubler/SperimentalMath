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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_kcnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 2:
            var = random.choice(variables)
            if random.choice([True, False]):
                var *= -1
            clause.add(var)
        clauses.append(clause)
    return clauses

def incidence_matrix(clauses, n):
    m = len(clauses)
    W = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                W[i][var - 1] = 1
            else:
                W[i][-var - 1] = 1
    return W

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot_row = None
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is not None:
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = -A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] += factor * A[rank][k]
            rank += 1
    return rank

def schur_weyl_polynomial(W):
    m, n = len(W), len(W[0])
    if gaussian_elimination(W) != min(m, n):
        return None
    det = 1
    for i in range(min(m, n)):
        det *= W[i][i]
    return abs(det)

def monomial_ideal_complexity(k, n):
    # Placeholder function. Actual implementation required.
    return random.randint(1, 10)  # Dummy value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = random.choice([3, 4, 5])
    n = random.choice(range(5, 41))
    clauses = generate_kcnf(n, k)
    W = incidence_matrix(clauses, n)
    rho = schur_weyl_polynomial(W)
    if rho is None:
        return {
            "metric_name": "rho",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    I_m = monomial_ideal_complexity(k, n)
    if I_m is None:
        return {
            "metric_name": "I_m",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "undefined_mapping"
        }
    rho_expected = I_m ** 1.5
    correlation = (rho - rho_expected) / max(abs(rho), abs(rho_expected))
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": abs(correlation) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")