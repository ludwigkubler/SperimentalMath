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

def generate_truth_table(n):
    return [[(i >> j) & 1 for j in range(n)] for i in range(2**n)]

def walsh_hadamard_transform(table):
    n = len(table)
    transform = table[:]
    s = 1
    while s < n:
        for k in range(s):
            for i in range(k, n, 2 * s):
                j = i + s
                a, b = transform[i], transform[j]
                transform[i] = a + b
                transform[j] = (a - b) * math.sqrt(2)
        s *= 2
    return [[x / math.sqrt(n) for x in row] for row in transform]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            return None
        for j in range(i, n * 2):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n * 2):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[n:] for row in augmented_matrix]

def rank_stable(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    if reduced_matrix is None:
        return 0
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        truth_table = generate_truth_table(n)
        M_C = walsh_hadamard_transform(truth_table)
        rank_stable_M_C = rank_stable(M_C)
        if rank_stable_M_C < 0.6 * math.log2(n):
            conjecture_holds = False
            counterexample = f"rank_stable(M_C) = {rank_stable_M_C} < 0.6 * log₂({n})"

    return {
        "metric_name": "rank_stable",
        "metric_value": rank_stable_M_C,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")