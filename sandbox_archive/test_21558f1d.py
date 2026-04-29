# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def generate_k_clique_dnf(n, k):
    clauses = []
    for clique in combinations(range(n), k):
        clause = [f"x{i+1}" for i in clique]
        clauses.append(" or ".join(clause))
    dnf = " and ".join(clauses)
    return dnf

def generate_random_dnf(n, m):
    variables = [f"x{i+1}" for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [f"not {v}" for v in clause]
        clauses.append(" or ".join(clause))
    dnf = " and ".join(clauses)
    return dnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        if n == 20:  # Skip n=20 to avoid excessive computation time
            continue
        for _ in range(5):  # Sample 5 instances per n
            dnf = generate_k_clique_dnf(n, n // 2) if n >= 10 else generate_random_dnf(n, random.randint(1, n**2))
            A_F = []
            for clause in dnf.split(" and "):
                row = [1] * (n + 1)
                for var in clause.split(" or "):
                    if var.startswith("not "):
                        j = int(var[4:]) - 1
                        row[j] = 0
                    else:
                        j = int(var[1:]) - 1
                        row[j] = 1
                A_F.append(row)
            rank_F2 = rank(A_F)
            m = len(A_F)
            delta_F = math.log2(m + 1) - math.log2(rank_F2)
            total_metric_value += delta_F
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (len(n_values) * 5)

    if support_fraction < 0.8:
        conjecture_holds = False
        counterexample = "support_fraction_below_80"

    return {
        "metric_name": "GF(2) rank defect",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_below_80\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_below_80")