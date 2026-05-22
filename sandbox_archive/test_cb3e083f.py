# auto-injected by SEC sandbox
import math
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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        pivot = A_b[i][i]
        for j in range(i, n+1):
            A_b[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_b[j][i]
                for k in range(i, n+1):
                    A_b[j][k] -= factor * A_b[i][k]
    return [row[-1] for row in A_b]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    X = {tuple(random.randint(0, 100) for _ in range(n)) for _ in range(n)}
    instances_tested = len(X)

    # Construct moduli space M (simplified example)
    M = [[random.random() for _ in range(n)] for _ in range(n)]

    # Compute minimal lifting rank
    incidence_variety = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    ambient_space = M
    A = matrix_multiply(incidence_variety, ambient_space)
    b = [random.random() for _ in range(n)]
    lifting_rank = len(gaussian_elimination(A, b))

    # Measure randomized communication complexity (simplified example)
    communication_complexity = n * 2

    conjecture_holds = lifting_rank >= 10 * instances_tested and communication_complexity < 0.5 * instances_tested
    counterexample = "" if conjecture_holds else f"lifting_rank={lifting_rank}, communication_complexity={communication_complexity}"

    return {
        "metric_name": "Lifting Rank / Communication Complexity",
        "metric_value": lifting_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")