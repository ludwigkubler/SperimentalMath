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
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def frobenius_norm(M):
    n = len(M)
    norm = 0
    for i in range(n):
        for j in range(n):
            norm += M[i][j] ** 2
    return math.sqrt(norm)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_norm = 0

    for _ in range(instances_tested):
        # Generate a balanced bipartite graph with uniform edge weights
        A = [[0] * n for _ in range(n)]
        for i in range(n // 2):
            for j in range(n // 2, n):
                if random.choice([True, False]):
                    A[i][j] = 1
                    A[j][i] = 1

        # Compute the Frobenius norm of the adjacency matrix
        norm = frobenius_norm(A)
        total_norm += norm

    average_norm = total_norm / instances_tested
    conjecture_holds = average_norm >= 0.95 * math.sqrt(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Frobenius Norm",
        "metric_value": average_norm,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    # Compute mean and standard deviation of metric_value
    values = [r["metric_value"] for r in results]
    mean = sum(values) / len(values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))

    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")