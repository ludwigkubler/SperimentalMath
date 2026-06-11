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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(A):
        U, _, V = gaussian_elimination(matrix_multiply(A, A))
        rank = sum(1 for row in U if any(val != 0 for val in row))
        return Fraction(rank) / len(A)

    def min_cat_complexity(A):
        m, n = len(A), len(A[0])
        max_nonzero_col = -1
        for j in range(n):
            if any(row[j] != 0 for row in A):
                max_nonzero_col = j
        return Fraction(max_nonzero_col + 1)

    def generate_communication_problem(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_metric_value = Fraction(0)
    instances_tested = 0
    n_max = -1
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = generate_communication_problem(n)
            R_phi = rank_variance(A)
            min_cat_phi_prime = min_cat_complexity(A)
            results.append((min_cat_phi_prime, R_phi))
            total_metric_value += abs(min_cat_phi_prime - R_phi)
            instances_tested += 1
            n_max = max(n_max, n)

    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    def pearson_correlation_coefficient(data):
        x, y = zip(*data)
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in data) / len(data)
        std_dev_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_dev_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_dev_x * std_dev_y)

    pearson_corr_coeff = pearson_correlation_coefficient(results)
    if pearson_corr_coeff < 0.5:
        conjecture_holds = False
        counterexample = f"Pearson correlation coefficient {pearson_corr_coeff} is below threshold"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient below threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")