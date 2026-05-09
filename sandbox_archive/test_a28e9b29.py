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

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def hook_length_formula(matrix, shape):
    n = len(shape)
    numerator = factorial(factorial(n))
    denominator = 1
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == shape[i]:
                denominator *= (i + j + 1 - shape[i])
    return numerator / denominator

def generate_random_matrix(n):
    return [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    matrix = generate_random_matrix(n)
    
    # Rectangular shape (n,n,...,n)
    rectangular_shape = [n] * n
    rect_count = hook_length_formula(matrix, rectangular_shape)
    
    # Staircase shape (n,n-1,...,1)
    staircase_shape = list(range(n, 0, -1))
    stair_count = hook_length_formula(matrix, staircase_shape)
    
    ratio = rect_count / stair_count
    
    metric_value = math.log2(ratio) if ratio > 0 else float('-inf')
    conjecture_holds = metric_value >= n
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 2^{n}"
    
    return {
        "metric_name": "log2_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")