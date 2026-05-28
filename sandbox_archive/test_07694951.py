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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[n:] for row in augmented_matrix]

def rank(matrix):
    return len(gaussian_elimination(matrix))

def construct_quaternionic_form(n):
    truth_table = [[random.choice([0, 1]) for _ in range(3)] for _ in range(2**n)]
    form = []
    for i in range(2**n):
        row = [truth_table[i][j] * (-1)**sum(truth_table[i][k] & truth_table[j][k] for k in range(3)) for j in range(2**n)]
        form.append(row)
    return form

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):
            form = construct_quaternionic_form(n)
            rank_value = rank(form)
            if rank_value == 0:
                continue
            total_rank += rank_value
            instances_tested += 1
        if instances_tested == 0:
            continue
        average_rank = total_rank / instances_tested
        results.append({
            "n": n,
            "average_rank": average_rank,
            "log_n": math.log(n)
        })
    if not results:
        return {
            "metric_name": "Average Rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    average_rank = sum(result["average_rank"] for result in results) / len(results)
    log_n_mean = sum(result["log_n"] for result in results) / len(results)
    epsilon = 0.1
    conjecture_holds = all(result["average_rank"] >= 0.5 * result["log_n"] + epsilon for result in results)
    counterexample = "" if conjecture_holds else "Average rank does not meet the threshold"
    return {
        "metric_name": "Average Rank",
        "metric_value": average_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank does not meet the threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")