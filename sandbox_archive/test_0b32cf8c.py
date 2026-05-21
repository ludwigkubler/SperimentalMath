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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return None
        for j in range(i + 1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i + 1, n))) / augmented_matrix[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(n)]
        quiver_representation = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    quiver_representation[i][j] = 1
                    quiver_representation[j][i] = 1

        # Calculate minimal root separation
        A = [row[:] for row in quiver_representation]
        b = [0] * n
        x = gaussian_elimination(A, b)
        if x is None:
            conjecture_holds = False
            counterexample = "singular_matrix"
            break

        min_root_separation = min(abs(x[i]) for i in range(n))
        total_metric_value += min_root_separation

        # Calculate communication complexity (simplified example)
        comm_complexity = math.sqrt(n)

        if min_root_separation < comm_complexity / 2:
            conjecture_holds = False
            counterexample = "communication_complexity_violation"

    return {
        "metric_name": "minimal_root_separation",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")