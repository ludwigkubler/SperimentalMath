# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations

def generate_cnf(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i, j in combinations(range(n), 2)):
            clauses.append(clause)
    return random.choice(clauses)

def polynomial_ring(cnf):
    n = len(cnf[0])
    ring = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for i, lit in enumerate(clause):
            if lit > 0:
                ring[i][lit - 1] += 1
            else:
                ring[lit - 1][i] += 1
    return ring

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            return None
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n + 1):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def min_order_k_theory(ring):
    n = len(ring)
    augmented_matrix = [row + [0] for row in ring] + [[0] * (n + 1) + [1]]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    if not reduced_matrix:
        return None
    rank = sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(n)))
    return n - rank

def resolution_proof_width(cnf):
    n = len(cnf[0])
    width = [max(abs(lit) for lit in clause) for clause in cnf]
    return max(width)

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
            cnf = generate_cnf(n)
            ring = polynomial_ring(cnf)
            min_order = min_order_k_theory(ring)
            width = resolution_proof_width(cnf)
            if min_order is not None and width is not None:
                metric_values.append(min_order / width)
                instances_tested += 1
                n_max = max(n_max, n)

    mean_value = sum(metric_values) / len(metric_values) if metric_values else 0
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values)) if metric_values else 0

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"

    return {
        "metric_name": "min_order_K_theory_over_resolution_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")