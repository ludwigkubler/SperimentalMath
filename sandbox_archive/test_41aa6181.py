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

def generate_disjunctive_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def matmul(A, B):
    n = len(A)
    result = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return result

def spectral_radius(matrix):
    n = len(matrix)
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    A = matrix
    for _ in range(100):  # Power iteration method
        A = matmul(A, matrix)
        norm = sum(sum(abs(x) for x in row) for row in A)
        A = [[x / norm for x in row] for row in A]
    return max(max(row) for row in A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 30
    total_radius = 0.0

    for _ in range(instances_tested):
        F = generate_disjunctive_boolean_function(random.randint(5, 40))
        radius = spectral_radius([[Fraction(F[i]) for i in range(len(F))]])
        total_radius += radius

    mean_metric_value = total_radius / instances_tested
    std_metric_value = math.sqrt(sum((radius - mean_metric_value) ** 2 for radius in [spectral_radius(generate_disjunctive_boolean_function(random.randint(5, 40))) for _ in range(instances_tested)]) / (instances_tested - 1))
    
    c = 1.0  # Hypothetical constant c
    lower_bound = c * math.log(max(n_values))
    upper_bound = c * math.log(min(n_values))

    conjecture_holds = all(lower_bound <= radius <= upper_bound for radius in [spectral_radius(generate_disjunctive_boolean_function(random.randint(5, 40))) for _ in range(instances_tested)])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "L^p spectral radius",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")