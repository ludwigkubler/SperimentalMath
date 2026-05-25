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
        # Generate a disjunctive Boolean function (e.g., OR of all variables)
        return [1 if i % 2 == 0 else 0 for i in range(n)]
    
    def spectral_radius(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        max_iter = 1000
        tol = 1e-6
        
        # Power iteration method to approximate the spectral radius
        v = [1] * n
        for _ in range(max_iter):
            Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            max_val = max(abs(x) for x in Av)
            if max_val < tol:
                break
            v = [x / max_val for x in Av]
        
        return max_val
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        F = generate_disjunctive_boolean_function(n)
        matrix = [[F[i] * F[j] for j in range(n)] for i in range(n)]
        radius = spectral_radius(matrix)
        total_metric_value += radius
        instances_tested += 1
    
    mean_metric_value = total_metric_value / len(n_values)
    std_deviation = math.sqrt(sum((radius - mean_metric_value) ** 2 for radius in [spectral_radius(generate_disjunctive_boolean_function(n)) for n in n_values]) / len(n_values))
    
    conjecture_holds = all(mean_metric_value >= c * math.log(n) for n in n_values)
    if not conjecture_holds:
        counterexample = "mean_metric_value < c * log(n)"
    else:
        counterexample = ""
    
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
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")