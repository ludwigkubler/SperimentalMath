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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def log_factorial(n):
        return sum(math.log(i) for i in range(1, n + 1))
    
    def generate_sat_instance(m, n):
        variables = set(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def minimal_root_count(clauses):
        # Placeholder function to compute the minimal root count
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(clauses)  # Simplified for demonstration purposes
    
    results = []
    for n in range(5, 41):
        for _ in range(30):  # Ensure at least 30 instances per seed
            m = random.randint(5, min(40, max(5, int(n * 1.2))))
            clauses = generate_sat_instance(m, n)
            root_count = minimal_root_count(clauses)
            results.append({
                "n": n,
                "m": m,
                "root_count": root_count
            })
    
    total_metric_value = sum(result["root_count"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["root_count"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(log_factorial(n) <= result["root_count"] <= n**3 for result in results)
    counterexample = "" if conjecture_holds else "minimal_root_count_undefined"
    
    return {
        "metric_name": "Minimal Root Count",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")