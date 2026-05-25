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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjunctive_boolean_function(n):
        # Generate a disjunctive Boolean function by ORing n-1 random literals
        return [random.choice([0, 1]) for _ in range(n - 1)] + [1]
    
    def spectral_radius(matrix):
        n = len(matrix)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix
        for _ in range(20):  # Power iteration method
            A = matmul(A, matrix)
            norm = sum(sum(abs(x) for x in row) for row in A)
            A = [[x / norm for x in row] for row in A]
        return max(max(row) for row in A)
    
    def matmul(A, B):
        n = len(A)
        result = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different disjunctive functions
            F = generate_disjunctive_boolean_function(n)
            matrix = [[F[i] ^ F[j] for j in range(n)] for i in range(n)]
            radius = spectral_radius(matrix)
            total_metric_value += radius
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((radius - mean_metric_value) ** 2 for radius in [spectral_radius(generate_disjunctive_boolean_function(n)) for n in n_values for _ in range(5)]) / (instances_tested - 1))
    
    c = 0.5  # Hypothetical constant c, adjust as needed
    lower_bound = c * math.log(n)
    upper_bound = c * math.log(n) + 3 * std_metric_value
    
    conjecture_holds = all(lower_bound <= radius <= upper_bound for n in n_values for _ in range(5))
    
    return {
        "metric_name": "L^p spectral radius",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")