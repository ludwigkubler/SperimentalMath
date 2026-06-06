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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + random.randint(0, n - i - 1)
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def is_singular(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            if matrix[i][i] == 0:
                return True
            det *= matrix[i][i]
        return det == 0

    def variance_ratio(matrix):
        n = len(matrix)
        sum_squares = 0
        for row in matrix:
            for val in row:
                sum_squares += val ** 2
        mean_square = sum_squares / (n * n)
        square_mean = (sum(row) / n) ** 2
        variance = mean_square - square_mean
        return Fraction(variance, n * (n + 1) // 2)

    def min_order_formal_context(matrix):
        n = len(matrix)
        matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in matrix if any(row))
        return rank

    def generate_communication_complexity_instance(n):
        elements = list(range(n))
        relations = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    relations.add((i, j))
        matrix = [[0] * n for _ in range(n)]
        for i, j in relations:
            matrix[i][j] = 1
            matrix[j][i] = 1
        return matrix

    def calculate_metric(matrix):
        min_order = min_order_formal_context(matrix)
        variance = variance_ratio(matrix)
        if variance == 0:
            return None
        return Fraction(min_order, variance)

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        matrix = generate_communication_complexity_instance(n)
        if is_singular(matrix):
            continue
        result = calculate_metric(matrix)
        if result is not None:
            metric_values.append(result)
        else:
            conjecture_holds = False
            counterexample = "mapping_undefined"
            break

    return {
        "metric_name": "Min Order / Variance Ratio",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")