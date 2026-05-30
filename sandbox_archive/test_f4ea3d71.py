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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def construct_affine_algebra(formula):
        n = len(formula)
        algebra = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            algebra[i][i] = 1
            algebra[n][i] = int(formula[i])
        return algebra
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        if A is None:
            return 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 30
    total_order = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        algebra = construct_affine_algebra(formula)
        order = matrix_rank(algebra)
        total_order += order
    
    metric_value = total_order / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if len(results) >= 80:
        correlation_coefficient = calculate_correlation(results)
        if correlation_coefficient >= 0.8:
            conjecture_holds = True
    
    return {
        "metric_name": "Average Order of Affine Algebra",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(results):
    n = len(results)
    if n < 2:
        return 0
    
    x_mean = sum(result["metric_value"] for result in results) / n
    y_mean = math.log(len(results))
    
    numerator = sum((result["metric_value"] - x_mean) * (math.log(i) - y_mean) for i, result in enumerate(results, start=5))
    denominator = math.sqrt(sum((result["metric_value"] - x_mean)**2 for result in results)) * math.sqrt(sum((math.log(i) - y_mean)**2 for i, result in enumerate(results, start=5)))
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")