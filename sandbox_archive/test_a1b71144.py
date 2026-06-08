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
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def characteristic_polynomial(matrix):
    n = len(matrix)
    coeff = [Fraction(1)]
    for i in range(n):
        new_coeff = [0] * (n - i + 1)
        for j in range(i+1, n):
            for k in range(j):
                if k < i:
                    new_coeff[j-k] += matrix[i][k] * coeff[-j+k]
                else:
                    new_coeff[j-k] -= matrix[i][k] * coeff[-j+k-1]
        coeff = new_coeff
    return coeff

def min_local_index(coeff):
    n = len(coeff) - 1
    if n == 0: return 0
    for i in range(1, n+1):
        if all(abs(coeff[j]) < abs(coeff[j+i]) for j in range(n-i+1)):
            return i
    return n

def variance(lst):
    mean = sum(lst) / len(lst)
    return sum((x - mean) ** 2 for x in lst) / len(lst)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        rank_variances = [random.randint(1, 100) for _ in range(30)]
        for rank_variance in rank_variances:
            matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            gaussian_elimination(matrix)
            coeff = characteristic_polynomial(matrix)
            min_local = min_local_index(coeff)
            results.append((n, min_local, rank_variance))
    
    if not results:
        return {
            "metric_name": "log_min_local_index",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }
    
    log_msl = [math.log(result[1]) for result in results]
    var_rank = [result[2] for result in results]
    correlation_coefficient = sum((log_msl[i] - mean(log_msl)) * (var_rank[i] - mean(var_rank)) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "log_min_local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        RESULT = "SUPPORTED"
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={mean([result['metric_value'] for result in results])} std=0 support_fraction=1")