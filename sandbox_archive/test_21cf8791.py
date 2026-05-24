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

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            continue
        for j in range(n + 1):
            augmented_matrix[i][j] /= pivot
        for k in range(m):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(n)))

def commutator(A, B):
    return matrix_multiply(matrix_multiply(A, B), -matrix_multiply(B, A))

def minimal_index_of_noncommutativity(channel):
    identity = [[1 if i == j else 0 for j in range(len(channel))] for i in range(len(channel))]
    rho = rank(commutator(identity, channel))
    return rho

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    channel = [[random.random() for _ in range(n)] for _ in range(n)]
    rho = minimal_index_of_noncommutativity(channel)
    log_size_BP = math.log(n)  # Simplified size measure for BP
    metric_value = rho / log_size_BP
    instances_tested = 1
    conjecture_holds = n / (log_size_BP * log(log_size_BP)) <= rho <= n * log_size_BP
    counterexample = "" if conjecture_holds else f"rho={rho}, expected bounds: [{n / (log_size_BP * log(log_size_BP)), n * log_size_BP}]"
    return {
        "metric_name": "minimal_index_of_noncommutativity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")