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
from itertools import combinations, product

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def geometric_representation(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for j in clause:
            A[i][abs(j) - 1] += 1 if j > 0 else -1
        A[i][-1] = -sum(A[i][:n])
    return gaussian_elimination(A)

def dpll(clauses, assignment=[]):
    if not clauses:
        return True
    var = next((v for v in range(1, len(clauses) + 1) if v not in assignment and -v not in assignment), None)
    if var is None:
        return False
    for value in [True, False]:
        new_assignment = assignment[:]
        new_assignment.append(var if value else -var)
        if dpll([c for c in clauses if not any(v in c or -v in c for v in new_assignment)], new_assignment):
            return True
    return False

def max_complexity(A):
    n = len(A)
    rank = 0
    for row in A:
        if all(x == 0 for x in row[:-1]):
            continue
        pivot_row = max(range(rank, n), key=lambda r: abs(row[r]))
        row[:], A[pivot_row][:] = A[pivot_row][:], row[:]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    metric_value = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = []
            for _ in range(n):
                variables = random.sample(range(1, n + 1), random.randint(1, n))
                clause = [random.choice([v, -v]) for v in variables]
                clauses.append(clause)
            instances_tested += 1
            n_max = max(n_max, len(clauses))

            try:
                geometric_rep = geometric_representation(clauses)
                complexity = max_complexity(geometric_rep)
                height = dpll(clauses)
                metric_value += complexity / height if height > 0 else float('inf')
            except Exception as e:
                conjecture_holds = False
                counterexample = f"Error during computation for n={n}: {e}"
                break

    if instances_tested < 30:
        return {
            "metric_name": "complexity_to_height_ratio",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean = metric_value / instances_tested
    std_dev = (sum((x - mean) ** 2 for x in [complexity / height if height > 0 else float('inf') for _ in range(instances_tested)]) / instances_tested) ** 0.5

    return {
        "metric_name": "complexity_to_height_ratio",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={std_dev} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")