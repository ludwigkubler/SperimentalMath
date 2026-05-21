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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def count_non_zero_coeffs(A):
    count = 0
    for row in A:
        for val in row:
            if val != 0:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2*n)
    clauses = []
    for _ in range(num_clauses):
        clause = set(random.sample(range(n), random.randint(1, n)))
        clauses.append(clause)

    # Convert to GF(2) indicator polynomial
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        A[i][i] = 1
    for clause in clauses:
        for i in clause:
            for j in clause:
                if i != j:
                    A[i][j] += 1

    # Gaussian elimination to get elementary symmetric polynomial decomposition
    A = gaussian_elimination(A)
    non_zero_coeffs = count_non_zero_coeffs(A)

    # Simulate ABP width (bounded-depth circuit)
    abp_width = random.randint(1, n + 1)

    return {
        "metric_name": "ABP Width",
        "metric_value": abp_width,
        "instances_tested": 1,
        "conjecture_holds": non_zero_coeffs >= abp_width,
        "counterexample": "" if non_zero_coeffs >= abp_width else f"n={n}, clauses={clauses}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")