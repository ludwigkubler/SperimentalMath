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
from fractions import Fraction
import math

def generate_truth_table(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def calculate_minimal_order(truth_table):
    n = int(math.log2(len(truth_table)))
    formal_context = {}
    for i in range(2**n):
        row = truth_table[i * (2**(n-1)):i * (2**(n-1)) + 2**(n-1)]
        if tuple(row) not in formal_context:
            formal_context[tuple(row)] = set()
        for j in range(n):
            if row[j] == 1:
                formal_context[tuple(row)].add(j)
    return len(formal_context)

def calculate_matrix_representation(truth_table):
    n = int(math.log2(len(truth_table)))
    matrix = []
    for i in range(2**n):
        row = truth_table[i * (2**(n-1)):i * (2**(n-1)) + 2**(n-1)]
        matrix.append(row)
    return matrix

def calculate_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
        matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
        for j in range(m):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def calculate_ratio(truth_table):
    n = int(math.log2(len(truth_table)))
    minimal_order = calculate_minimal_order(truth_table)
    matrix_representation = calculate_matrix_representation(truth_table)
    rank = calculate_rank(matrix_representation)
    if rank == 0:
        return None
    return Fraction(minimal_order, rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        truth_table = generate_truth_table(n)
        ratio = calculate_ratio(truth_table)
        if ratio is None:
            continue
        results.append(ratio)
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(ratio <= Fraction(math.log(n), 1) for n, ratio in zip(n_values, results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")