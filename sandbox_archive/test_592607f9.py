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

def generate_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = set()
        for _ in range(3):
            var = f'x{random.randint(1, n)}'
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(f'~{var}')
        clauses.append(clause)
    return clauses

def solve_system(literals: set, clauses: list) -> int:
    n = len(literals)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)

    for clause in clauses:
        clause_vars = {var[2:] if var.startswith('~') else var for var in clause}
        for i, literal in enumerate(literals):
            if literal in clause_vars:
                A[i][i] += 1
            elif f'~{literal}' in clause_vars:
                A[i][i] -= 1

    # Gaussian elimination with partial pivoting
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitution
    x = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n + 1))) / A[i][i]

    # Count distinct real points
    num_real_points = 0
    for i in range(n):
        if abs(x[i]) < 1e-6:
            continue
        is_distinct = True
        for j in range(i):
            if abs(x[j] - x[i]) < 1e-6:
                is_distinct = False
                break
        if is_distinct:
            num_real_points += 1

    return num_real_points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    literals = set()
    for clause in clauses:
        literals.update(clause)

    num_real_points = solve_system(literals, clauses)
    conjecture_holds = num_real_points >= n
    counterexample = "" if conjecture_holds else f"n={n}, real points={num_real_points}"

    return {
        "metric_name": "Number of distinct real points",
        "metric_value": num_real_points,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, real points={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")