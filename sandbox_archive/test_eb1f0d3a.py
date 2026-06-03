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
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Singular check
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        
        # Eliminate above and below
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(M):
    n = len(M)
    matrix = [row[:] for row in M]
    try:
        gaussian_elimination(matrix)
        rank = sum(1 for row in matrix if any(row))
        return rank
    except ValueError:
        return 0

def min_local_indeterminacy(M):
    n = len(M)
    matrix = [row[:] for row in M]
    try:
        gaussian_elimination(matrix)
        indeterminacy = sum(1 for row in matrix if not all(row))
        return indeterminacy
    except ValueError:
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    alpha_values = []
    r_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            alpha = min_local_indeterminacy(M)
            r = rank(M)
            if alpha is not None and r is not None:
                alpha_values.append(alpha)
                r_values.append(r)
                instances_tested += 1

    if not alpha_values or not r_values:
        return {
            "metric_name": "min_local_indeterminacy vs communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    alpha_mean = sum(alpha_values) / len(alpha_values)
    r_mean = sum(r_values) / len(r_values)
    mean_abs_diff = sum(abs(a - r) for a, r in zip(alpha_values, r_values)) / len(alpha_values)

    correlation_coefficient = 0
    if len(alpha_values) > 1:
        numerator = sum((alpha_values[i] - alpha_mean) * (r_values[i] - r_mean) for i in range(len(alpha_values)))
        denominator = math.sqrt(sum((alpha_values[i] - alpha_mean)**2 for i in range(len(alpha_values))) *
                                sum((r_values[i] - r_mean)**2 for i in range(len(r_values))))
        correlation_coefficient = numerator / denominator

    return {
        "metric_name": "min_local_indeterminacy vs communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff / n_max <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")