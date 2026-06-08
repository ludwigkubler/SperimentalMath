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
    
    def generate_instance(n):
        if n == 1:
            return [0]
        else:
            instance = [random.randint(0, 1) for _ in range(n)]
            while sum(instance) == 0 or sum(instance) == n:
                instance = [random.randint(0, 1) for _ in range(n)]
            return instance
    
    def rank_variance(instance):
        n = len(instance)
        avg_rank = sum(instance) / n
        variance = sum((x - avg_rank) ** 2 for x in instance) / n
        return variance
    
    def median_rank(instance):
        sorted_instance = sorted(instance)
        n = len(sorted_instance)
        if n % 2 == 1:
            return sorted_instance[n // 2]
        else:
            return (sorted_instance[n // 2 - 1] + sorted_instance[n // 2]) / 2
    
    def local_coherence_index(configuration_space):
        n = len(configuration_space)
        sum_i = sum(configuration_space[i][i] for i in range(n))
        sum_ij = sum(configuration_space[i][j] for i in range(n) for j in range(i+1, n))
        return sum_i / (2 * sum_ij)
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]
        return [M[i][-1] for i in range(n)]
    
    def linear_regression(X, Y):
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x * y for x, y in zip(X, Y))
        sum_xx = sum(x ** 2 for x in X)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def p_value(slope, intercept, X, Y):
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x * y for x, y in zip(X, Y))
        sum_xx = sum(x ** 2 for x in X)
        sum_yy = sum(y ** 2 for y in Y)
        numerator = (n * sum_xy - sum_x * sum_y) ** 2
        denominator = (n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2)
        r_squared = numerator / denominator
        t_statistic = slope / math.sqrt(r_squared * (1 - r_squared) / (n - 2))
        p_value = 2 * (1 - abs(t_statistic) / math.sqrt(n - 2))
        return p_value
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_instance(n)
        rank_var = rank_variance(instance)
        median_rank_val = median_rank(instance)
        R = median_rank_val
        I = local_coherence_index(generate_instance(n))
        
        if R == 0 or rank_var == 0:
            continue
        
        results.append((I, rank_var / R))
    
    if not results:
        return {
            "metric_name": "p_value",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    X, Y = zip(*results)
    slope, intercept = linear_regression(X, Y)
    p_val = p_value(slope, intercept, X, Y)
    
    return {
        "metric_name": "p_value",
        "metric_value": p_val,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": p_val < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_p_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_p_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "p-value >= 0.05"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")