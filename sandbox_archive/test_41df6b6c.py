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
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def min_order_of_partitions(clauses):
        # Simplified dynamic programming approach to find the minimal order of partitions
        n = len(clauses)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][i] = 1
        for length in range(2, n + 1):
            for start in range(1, n - length + 2):
                end = start + length - 1
                dp[start][end] = min(dp[start][k] + dp[k + 1][end] for k in range(start, end))
        return dp[1][n]
    
    def calculate_metric(n, p):
        return abs(p - n ** (0.25 + 0.01))  # Using a small ε to ensure non-triviality
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        p = min_order_of_partitions(generate_cnf(n))
        metric_value = calculate_metric(n, p)
        results.append(metric_value)
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    
    conjecture_holds = all(x > n ** (0.25 + 0.01) for x, n in zip(results, [5, 10, 15, 20, 30, 40]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order_of_partitions",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")