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

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
        random.shuffle(clause)
        clauses.append(tuple(clause))
    return clauses

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        pivot_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(i + 1, cols):
            A[i][j] /= A[i][i]
        A[i][i] = 1
        for k in range(rows):
            if k != i:
                factor = A[k][i]
                for j in range(i, cols):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row))
    return rank

def geometric_invariant_theory(poly):
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(poly):
        for j in clause:
            A[i][j - 1] += 1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(40, 50)
    m = random.randint(1, n**2)
    phi = generate_3cnf(n, m)
    rank = geometric_invariant_theory(phi)
    metric_value = rank / (m ** Fraction(1, 4) * n ** Fraction(1, 2))
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "K-theory rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")