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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
        if matrix[max_row][i] == 0:
            return None  # Matrix is singular
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def geometric_invariant_rank(phi_G):
    try:
        rank = 0
        n = len(phi_G)
        augmented_matrix = [row + [1] for row in phi_G]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        if reduced_matrix is None:
            return float('inf')  # Matrix is singular, rank is infinite
        for row in reduced_matrix:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    except Exception as e:
        print(f"Error: {e}")
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    gir_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        phi_G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        gir_value = geometric_invariant_rank(phi_G)
        gir_values.append(gir_value)
        instances_tested += n
        n_max = max(n_max, n)

    if len(gir_values) < 30:
        return {
            "metric_name": "geometric_invariant_rank",
            "metric_value": sum(gir_values) / len(gir_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation_coefficient = 0
    for i in range(1, len(n_values)):
        x_mean = sum(gir_values[:i]) / i
        y_mean = sum(n_values[:i]) / i
        numerator = sum((gir_values[j] - x_mean) * (n_values[j] - y_mean) for j in range(i))
        denominator = math.sqrt(sum((gir_values[j] - x_mean)**2 for j in range(i))) * math.sqrt(sum((n_values[j] - y_mean)**2 for j in range(i)))
        if denominator == 0:
            correlation_coefficient = float('nan')
            break
        correlation_coefficient += numerator / denominator

    conjecture_holds = not math.isnan(correlation_coefficient) and correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"

    return {
        "metric_name": "geometric_invariant_rank",
        "metric_value": sum(gir_values) / len(gir_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")