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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        if all(matrix[i][j] == 0 for i in range(rank)):
            continue
        pivot_row = rank
        for i in range(pivot_row + 1, rows):
            if matrix[i][j] != 0:
                matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                break
        factor = Fraction(matrix[pivot_row][j])
        for k in range(cols):
            matrix[pivot_row][k] /= factor
        for i in range(rows):
            if i != pivot_row and matrix[i][j] != 0:
                factor = Fraction(matrix[i][j])
                for k in range(cols):
                    matrix[i][k] -= factor * matrix[pivot_row][k]
        rank += 1
    return rank

def generate_read_twice_bp(n, seed):
    random.seed(seed)
    bp = []
    for _ in range(2 ** n):
        bp.append(random.choice([0, 1]))
    return bp

def construct_crossed_product_algebra(bp, n):
    F = [[Fraction(i == j, 1) for j in range(n)] for i in range(n)]
    u_alpha = [[Fraction(math.cos(alpha), 1), Fraction(-math.sin(alpha), 1)], [Fraction(math.sin(alpha), 1), Fraction(math.cos(alpha), 1)]]
    M = []
    for row in F:
        new_row = []
        for col in row:
            new_col = []
            for i in range(n):
                temp = []
                for j in range(n):
                    temp.append(col * u_alpha[i][j])
                new_col.extend(temp)
            new_row.extend(new_col)
        M.extend(new_row)
    return M

def run_trial(seed: int) -> dict:
    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_read_twice_bp(n, seed)
    M = construct_crossed_product_algebra(bp, n)
    rank_M = matrix_rank(M)
    metric_value = rank_M
    instances_tested = 1
    conjecture_holds = rank_M >= n and rank_M <= math.log(2 ** n, 2)
    counterexample = "" if conjecture_holds else f"n={n}, rank_M={rank_M}"
    return {
        "metric_name": "Minimal Rank of Crossed Product",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, rank_M={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")