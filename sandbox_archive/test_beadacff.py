# auto-injected by SEC sandbox
import math
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
from itertools import combinations

def generate_3cnf(n: int, num_clauses: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(num_clauses):
        clause = set(random.sample(variables, 3))
        while len(clause) < 3:
            clause.add(random.choice(variables))
        clauses.append(tuple(sorted(clause)))
    return clauses

def rank_matrix(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            return -1
        for j in range(i + 1, m):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def hook_length_formula(shape: list[int]) -> int:
    m, n = len(shape), max(shape)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if i < shape[j]:
                table[i][j] = (i + 1) * (n - j) // (i + j + 2)
    return int(math.prod(table))

def generate_partition(clauses: list[tuple[int, ...]]) -> list[int]:
    incidence_matrix = [[0] * len(clauses) for _ in range(2)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                incidence_matrix[0][i] += 1
            else:
                incidence_matrix[1][i] += 1
    rank = min(rank_matrix(incidence_matrix), len(clauses))
    return [rank]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    num_clauses = 3 * n
    clauses = generate_3cnf(n, num_clauses)
    partition = generate_partition(clauses)
    tableau_count = hook_length_formula(partition)
    circuit_size = len(clauses)  # Simplified for testing purposes
    product = tableau_count * circuit_size
    conjecture_holds = product <= 100  # Placeholder value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "product",
        "metric_value": product,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")