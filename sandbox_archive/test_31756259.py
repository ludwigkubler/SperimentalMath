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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        S = list(range(2**n))
        M = [[f(S[i] ^ S[j]) for j in range(n)] for i in range(n)]
        return M
    
    def geometric_fluctuation(M):
        n = len(M)
        mean = sum(sum(row) for row in M) / (n * n)
        variance = sum((M[i][j] - mean)**2 for i in range(n) for j in range(n)) / (n * n)
        return math.sqrt(variance)
    
    def rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        pivot_row = 0
        for col in range(n):
            if all(A[row][col] == 0 for row in range(pivot_row, n)):
                continue
            max_row = pivot_row
            for i in range(pivot_row + 1, n):
                if abs(A[i][col]) > abs(A[max_row][col]):
                    max_row = i
            A[pivot_row], A[max_row] = A[max_row], A[pivot_row]
            for row in range(n):
                if row != pivot_row:
                    factor = -A[row][col] / A[pivot_row][col]
                    for j in range(col, n):
                        A[row][j] += factor * A[pivot_row][j]
            pivot_row += 1
        return pivot_row
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f, n)
        G_f = geometric_fluctuation(M)
        rank_f = rank(M)
        
        if G_f > 20 * (rank_f ** 2):
            return {
                "metric_name": "geometric_fluctuation",
                "metric_value": G_f,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Geometric fluctuation {G_f} exceeds 20 * (rank(f)^2) = {20 * (rank_f ** 2)}"
            }
        
        metric_values.append(G_f)
        instances_tested += n
        n_max = max(n_max, n)
    
    correlation_coefficient = correlation(metric_values, [rank(matrix_representation(generate_boolean_function(n), n)) for n in n_values])
    
    return {
        "metric_name": "geometric_fluctuation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
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
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result["metric_value"] < 0.5 or result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] < 0.5 or result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")