# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n + 1):
                if k < i:
                    matrix[j][k] -= factor * matrix[i][k]
                elif k == i:
                    matrix[j][k] = Fraction(0)
                else:
                    matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n = len(matrix)
    augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    return sum(1 for row in augmented_matrix if any(row[j] != Fraction(0) for j in range(n)) and all(row[j] == Fraction(0) for j in range(n, 2*n)))

def min_local_indeterminacy(matroid):
    n = len(matroid)
    matrix = [[Fraction(0)] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if matroid[i][j] == 1:
                matrix[i][j] = Fraction(1)
                matrix[j][i] = Fraction(1)
    
    gaussian_elimination(matrix)
    rank_matrix = rank(matrix)
    return rank_matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    alpha_values = []
    r_values = []

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed (6 instances per size)
            matroid = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            alpha = min_local_indeterminacy(matroid)
            r = rank(matroid)
            alpha_values.append(alpha)
            r_values.append(r)
            instances_tested += 1

    correlation_coefficient = sum((alpha - mean_alpha) * (r - mean_r) for alpha, r in zip(alpha_values, r_values)) / len(alpha_values)
    mean_alpha = sum(alpha_values) / len(alpha_values)
    mean_r = sum(r_values) / len(r_values)
    max_diff_over_n = max(abs(alpha - r) / n for alpha, r in zip(alpha_values, r_values))

    conjecture_holds = correlation_coefficient >= 0.8 and max_diff_over_n <= 3
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, Max diff/n: {max_diff_over_n}"

    return {
        "metric_name": "Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")