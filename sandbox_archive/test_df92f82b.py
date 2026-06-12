# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def p_adic_dilogarithm(x, p):
    if x <= 0:
        return 0
    result = 0
    for k in range(1, 50):  # Arbitrary precision limit
        term = (x ** k) / math.factorial(k)
        if abs(term) < 1e-10:
            break
        result += term * (-p_adic_log(p, k))
    return result

def p_adic_log(p, n):
    if n == 0:
        return 0
    result = 0
    for k in range(1, n + 1):
        result += (p ** -k) / k
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row[:] + [0] * m + [i] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot_row = None
        for row in range(col, m):
            if augmented_matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        augmented_matrix[pivot_row], augmented_matrix[col] = augmented_matrix[col], augmented_matrix[pivot_row]
        for row in range(m):
            if row == col:
                continue
            factor = augmented_matrix[row][col] / augmented_matrix[col][col]
            for j in range(n + m + 1):
                augmented_matrix[row][j] -= factor * augmented_matrix[col][j]
    rank = sum(1 for row in augmented_matrix if any(row[i] != 0 for i in range(n)))
    return rank

def generate_formula(n):
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals, random.randint(1, n))
        clauses.append(' or '.join(clause))
    formula = ' and '.join(clauses)
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            formula = generate_formula(n)
            MinRank_p = rank([[p_adic_dilogarithm(eval(lit), 2) for lit in formula.split(' or ')]])
            w_phi = len(formula.split(' and '))
            results.append((MinRank_p, w_phi))
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    MinRank_p_values = [r[0] for r in results]
    w_phi_values = [r[1] for r in results]
    n_max = max(n_values)
    mean_MarkRank_p = sum(MinRank_p_values) / len(MinRank_p_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    correlation_coefficient = (sum((MinRank_p - mean_MarkRank_p) * (w_phi - mean_w_phi) for MinRank_p, w_phi in results) /
                               math.sqrt(sum((MinRank_p - mean_MarkRank_p) ** 2 for MinRank_p in MinRank_p_values) *
                                         sum((w_phi - mean_w_phi) ** 2 for w_phi in w_phi_values)))
    p_value = 1  # Placeholder for actual p-value calculation
    conjecture_holds = abs(correlation_coefficient) >= 0.9 and p_value <= 0.05
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")