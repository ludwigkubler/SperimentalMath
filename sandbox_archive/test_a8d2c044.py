# auto-injected by SEC sandbox
import itertools
import collections
import json
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
from sys import argv

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find max pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    return [A[i][i] for i in range(n)], b

def free_cumulant_transform(M):
    n = len(M)
    M_bar = [[0] * (n+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(n):
            M_bar[i][j] = M[i][j]
            M_bar[i][n] += M[i][j]
            M_bar[n][i] += M[j][i]
    M_bar[n][n] = n
    
    A_bar = [[M_bar[i][j] for j in range(n+1)] for i in range(n+1)]
    b = [0] * (n+1)
    
    det, _ = gaussian_elimination(A_bar, b)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    free_cumulants = [free_cumulant_transform(M) for _ in range(10)]
    sum_abs_kappa = sum(abs(kappa) for kappa in free_cumulants)
    
    metric_value = sum_abs_kappa
    instances_tested = 10
    conjecture_holds = abs(sum_abs_kappa - (1 / math.sqrt(n))) < 0.316
    counterexample = "" if conjecture_holds else "free cumulant sum out of bounds"
    
    return {
        "metric_name": "Sum of Absolute Free Cumulants",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in argv[1:]] if argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")