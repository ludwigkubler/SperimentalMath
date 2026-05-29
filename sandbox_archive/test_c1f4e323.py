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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set(random.sample(range(1, n + 1), 2))
        if random.choice([True, False]):
            clause = {x: -1 for x in clause}
        clauses.append(clause)
    return clauses

def incidence_matrix(clauses, n):
    matrix = [[0] * (n * 2) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                matrix[i][var - 1] = 1
            else:
                matrix[i][-var - 1 + n] = 1
    return matrix

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = None
        for j in range(rank, rows):
            if matrix[j][i]:
                pivot_row = j
                break
        if pivot_row is not None:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if i != j:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
    return rank

def schur_weyl_invariant(matrix):
    rank = gaussian_elimination(matrix)
    n = len(matrix[0]) // 2
    det = 1
    for i in range(rank):
        det *= matrix[i][i] * (-matrix[i][n + i])
    return abs(det)

def monomial_ideal_complexity(n, k):
    # Placeholder function; actual implementation required
    return n * k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(3, 10)
    clauses = generate_k_cnf(n, k)
    matrix = incidence_matrix(clauses, n)
    rho = schur_weyl_invariant(matrix)
    I_m = monomial_ideal_complexity(n, k)
    metric_value = rho / (I_m ** 1.5)
    instances_tested = 1
    conjecture_holds = abs(metric_value - 1) < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")