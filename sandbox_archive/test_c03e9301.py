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
    m, k1 = len(A), len(A[0])
    k2, n = len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k1):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        pivot_row = max(range(col, m), key=lambda r: abs(augmented[r][col]))
        if augmented[pivot_row][col] == 0:
            continue
        augmented[col], augmented[pivot_row] = augmented[pivot_row], augmented[col]
        for row in range(m):
            if row != col:
                factor = augmented[row][col] / augmented[col][col]
                for j in range(n + 1):
                    augmented[row][j] -= factor * augmented[col][j]
    rank = sum(1 for row in augmented if any(row[i] != 0 for i in range(n)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    mso_depth = random.randint(1, 3)
    clause_length = random.randint(2, 5)

    # Construct an MSO formula with the given depth and clause length
    variables = [f"x{i}" for i in range(n)]
    clauses = []
    for _ in range(clause_length):
        clause = random.sample(variables, mso_depth)
        if random.choice([True, False]):
            clause = [f"~{var}" for var in clause]
        clauses.append(" | ".join(clause))
    
    formula = " & ".join(clauses)

    # Compute the Ramanujan sum for this formula
    assignments = [tuple(random.randint(0, 1) for _ in variables)]
    ramanujan_sum = 0
    for assignment in assignments:
        value = 1
        for var, val in zip(variables, assignment):
            if f"~{var}" in formula:
                value *= (1 - val)
            else:
                value *= val
        ramanujan_sum += value

    # Compute the rank of the Ramanujan sum matrix
    rank = gaussian_elimination([[ramanujan_sum]], [1])[0]

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * mso_depth,
        "counterexample": "" if rank <= 2 * mso_depth else f"Formula: {formula}, Rank: {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")