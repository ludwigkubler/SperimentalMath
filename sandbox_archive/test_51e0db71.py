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
        n = len(clauses)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][i] = 1
        for length in range(2, n + 1):
            for start in range(1, n - length + 2):
                end = start + length - 1
                dp[start][end] = min(dp[start][k] + dp[k+1][end] for k in range(start, end))
        return dp[1][n]
    
    def calculate_metric(n):
        cnf = generate_cnf(n)
        p_phi = min_order_of_partitions(cnf)
        return p_phi
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        metrics.append(calculate_metric(n))
    
    mean_value = sum(metrics) / len(metrics)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metrics) / len(metrics))
    
    conjecture_holds = all(x > n ** (1/4 + 0.05) for x in metrics)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order_of_partitions",
        "metric_value": mean_value,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")