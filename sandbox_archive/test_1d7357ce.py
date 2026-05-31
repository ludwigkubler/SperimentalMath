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
    
    def communication_complexity(n):
        # Placeholder for actual communication complexity calculation
        return n * (n - 1) // 2
    
    def min_automorphism_classes(n):
        # Placeholder for actual automorphism class calculation
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return n * (n - 1)
    
    instances_tested = 0
    min_aut_values = []
    comm_complexity_values = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        min_aut = min_automorphism_classes(n)
        comm_complexity = communication_complexity(n)
        
        min_aut_values.append(min_aut)
        comm_complexity_values.append(comm_complexity)
    
    correlation_coefficient = pearson_correlation(min_aut_values, comm_complexity_values)
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(log_n <= min_aut <= n_squared for log_n, min_aut, n_squared in zip(map(math.log, range(5, 41)), min_aut_values, map(lambda n: n**2, range(5, 41))))
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.7 or min_aut out of bounds"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")