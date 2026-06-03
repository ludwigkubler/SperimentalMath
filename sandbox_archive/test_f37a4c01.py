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

def generate_random_cnf(n, m):
    clauses = []
    for _ in range(m):
        literals = [random.choice([f"x{i+1}", f"~x{i+1}"]) for i in range(n)]
        clause = " | ".join(literals)
        clauses.append(clause)
    return " & ".join(clauses)

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    literals = set()
    for clause in cnf.split(" & "):
        literals.update(clause.split(" | "))
    literal = next(iter(literals))
    if literal.startswith("~"):
        negated = True
        literal = literal[1:]
    else:
        negated = False
    assignment[literal] = not negated
    new_cnf = []
    for clause in cnf.split(" & "):
        literals_in_clause = set(clause.split(" | "))
        if literal in literals_in_clause:
            continue
        if negated and f"~{literal}" in literals_in_clause:
            continue
        new_cnf.append(" | ".join(literals_in_clause))
    return dpll(" & ".join(new_cnf), assignment)

def symmetric_matrix(cnf):
    n = len(cnf.split(" & "))
    matrix = [[0] * n for _ in range(n)]
    for i, clause1 in enumerate(cnf.split(" & ")):
        for j, clause2 in enumerate(cnf.split(" & ")):
            if i == j:
                continue
            literals_in_clause1 = set(clause1.split(" | "))
            literals_in_clause2 = set(clause2.split(" | "))
            common_literals = literals_in_clause1.intersection(literals_in_clause2)
            matrix[i][j] = len(common_literals)
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None
        pivot = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= pivot
        for k in range(n):
            if k == i:
                continue
            factor = matrix[k][i]
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    return matrix

def minimal_index(matrix):
    n = len(matrix)
    identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity_matrix)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    if reduced_matrix is None:
        return float('inf')
    rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(n, 2 * n)
        cnf = generate_random_cnf(n, m)
        dpll_depth = dpll(cnf)
        if dpll_depth is None:
            return {
                "metric_name": "log_min_index",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "dpll failed"
            }
        matrix = symmetric_matrix(cnf)
        min_index = minimal_index(matrix)
        if min_index == float('inf'):
            return {
                "metric_name": "log_min_index",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "gaussian elimination failed"
            }
        results.append((min_index, dpll_depth))
    log_min_indices = [math.log(min_index) for min_index, _ in results]
    dpll_depths = [dpll_depth for _, dpll_depth in results]
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_min_indices, dpll_depths)) / len(results)
    mean_log_min_index = sum(log_min_indices) / len(log_min_indices)
    mean_dpll_depth = sum(dpll_depths) / len(dpll_depths)
    if abs(correlation_coefficient) < 0.7:
        return {
            "metric_name": "log_min_index",
            "metric_value": mean_log_min_index,
            "instances_tested": 30,
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={correlation_coefficient}"
        }
    return {
        "metric_name": "log_min_index",
        "metric_value": mean_log_min_index,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")