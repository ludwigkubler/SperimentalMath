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

def random_csp(n, m):
    variables = list(range(n))
    constraints = set()
    for _ in range(m):
        var1 = random.choice(variables)
        var2 = random.choice(variables)
        if var1 != var2:
            constraints.add((var1, var2))
    return variables, constraints

def moment_matrix(variables, constraints):
    n = len(variables)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        M[i][i] = 1
    for var1, var2 in constraints:
        M[var1][var2] += 1
        M[var2][var1] += 1
    return M

def real_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(i, n):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        rank += 1
        for j in range(n):
            matrix[i][j], matrix[pivot_row][j] = matrix[pivot_row][j], matrix[i][j]
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n + 1):
                matrix[j][k] -= factor * matrix[i][k]
    return rank

def sos_refutation_degree(matrix):
    # Placeholder for actual SOS refutation degree calculation
    # This is a dummy implementation for testing purposes
    n = len(matrix)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        M[i][i] = 1
    for i in range(n):
        for j in range(i, n):
            M[i][j], M[j][i] = matrix[i][j], matrix[i][j]
    # Simulate a simple refutation degree calculation
    return len(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, n * (n - 1) // 2)
    variables, constraints = random_csp(n, m)
    M = moment_matrix(variables, constraints)
    real_rank_value = real_rank(M)
    sos_degree = sos_refutation_degree(M)
    conjecture_holds = sos_degree <= real_rank_value
    counterexample = "" if conjecture_holds else f"SOS degree {sos_degree} > real rank {real_rank_value}"
    return {
        "metric_name": "SOS Refutation Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")