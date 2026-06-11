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

def generate_boolean_formula(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def evaluate_formula(formula, assignment):
    return all(sum(x * assignment[abs(x)-1] for x in clause) > 0 for clause in formula)

def characteristic_polynomial(formula, n):
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in formula:
        for literal in clause:
            i = abs(literal) - 1
            A[i][i] += literal
    return A

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    return A

def minimal_eichler_order(A, B):
    m = len(B)
    n = len(A) - 1
    M = [[A[i][j] for j in range(m)] + [B[j]] for i in range(n)]
    U = gaussian_elimination(M)
    det = 1
    for i in range(n):
        det *= U[i][i]
    return abs(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        m = random.randint(1, n)
        formula = generate_boolean_formula(n, m)
        assignments = [tuple(random.choice([0, 1]) for _ in range(n)) for _ in range(2**n)]
        satisfying_assignments = [assignment for assignment in assignments if evaluate_formula(formula, assignment)]
        num_satisfying = len(satisfying_assignments)

        A = characteristic_polynomial(formula, n)
        B = [sum(clause[i] for clause in formula) for i in range(n)]
        eichler_order = minimal_eichler_order(A, B)

        if num_satisfying > 0:
            correlation_sum += abs(eichler_order - (num_satisfying ** (1 / n)))
            instances_tested += 1
            n_max = max(n_max, n)

    mean_correlation = correlation_sum / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_correlation >= 0.7 and all(abs(mean_correlation - corr) <= 0.3 * abs(corr) for corr in [mean_correlation] * instances_tested)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")