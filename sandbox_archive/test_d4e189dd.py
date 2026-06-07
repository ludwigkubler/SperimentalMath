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
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause = [-c for c in clause]
            clauses.append(clause)
        return clauses
    
    def min_order_of_partitions(cnf):
        n = len(cnf)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][i] = 1
        for length in range(2, n + 1):
            for start in range(1, n - length + 2):
                end = start + length - 1
                dp[start][end] = min(dp[start][k] + dp[k + 1][end] for k in range(start, end))
        return dp[1][n]
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    p_values = []
    instances_tested = 0
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            p_value = min_order_of_partitions(cnf)
            p_values.append(p_value)
            instances_tested += 1
    
    if not p_values:
        return {
            "metric_name": "min_order_of_partitions",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_p = sum(p_values) / len(p_values)
    std_p = math.sqrt(sum((p - mean_p) ** 2 for p in p_values) / len(p_values))
    n_max = max(n_values)
    conjecture_holds = mean_p > (n_max ** (1/4 + 0.01)) and std_p >= 5
    counterexample = "" if conjecture_holds else "mean_p does not exceed n^(1/4 + ε)"
    
    return {
        "metric_name": "min_order_of_partitions",
        "metric_value": mean_p,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_p = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_p = math.sqrt(sum((r["metric_value"] - mean_p) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_p} std={std_p} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_p} std={std_p} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")