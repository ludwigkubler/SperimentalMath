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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_3sat_instance(n, m):
    variables = set(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.choice(variables)
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        clauses.add(tuple(sorted(clause)))
    return list(clauses)

def matrix_from_3sat(instance, n):
    matrix = [[0] * n for _ in range(n)]
    for clause in instance:
        for var in clause:
            if var > 0:
                row = abs(var) - 1
                col = abs(var) - 1
            else:
                row = abs(var) - 1
                col = abs(var) - 2
            matrix[row][col] += 1
    return matrix

def young_tableau(n):
    tableaux = []
    for i in range(1, n + 1):
        tableaux.append([i])
    return tableaux

def insert_into_tableau(tableau, value):
    for row in tableau:
        if value <= row[-1]:
            row.insert(row.index(value), value)
            return True
    return False

def generate_symmetric_power_decomposition(matrix, n):
    decomposition = {}
    def backtrack(tableau, remaining_rows):
        if not remaining_rows:
            key = tuple(tuple(row) for row in tableau)
            if key in decomposition:
                decomposition[key] += 1
            else:
                decomposition[key] = 1
            return
        row = remaining_rows.pop()
        for value in row:
            if insert_into_tableau(tableau, value):
                backtrack(tableau, remaining_rows)
                remove_from_tableau(tableau, value)
        remaining_rows.append(row)
    backtrack(young_tableau(n), matrix)
    return decomposition

def remove_from_tableau(tableau, value):
    for row in tableau:
        if value in row:
            row.remove(value)
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = int(1.5 * n)  # Ensure enough clauses
        instance = random_3sat_instance(n, m)
        matrix = matrix_from_3sat(instance, n)

        perm_decomposition = generate_symmetric_power_decomposition(matrix, n)
        det_decomposition = generate_symmetric_power_decomposition([[0]*n for _ in range(n)], n)

        if (n, n) not in perm_decomposition or (n, n) not in det_decomposition:
            conjecture_holds = False
            counterexample = "mapping_undefined"
            break

        perm_count = perm_decomposition[(n, n)]
        det_count = det_decomposition[(n, n)]

        if perm_count - det_count < math.sqrt(n):
            conjecture_holds = False
            counterexample = f"n={n}: {perm_count} (perm) vs {det_count} (det), gap < sqrt({n})"
            break

        total_metric_value += perm_count - det_count
        instances_tested += 1

    return {
        "metric_name": "partition_gap",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")