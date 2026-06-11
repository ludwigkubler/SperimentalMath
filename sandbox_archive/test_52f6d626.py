# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank_matrix = [[f[i ^ (a & (1 << j))] == f[i ^ (b & (1 << j))] for j in range(n)] for a, b in itertools.combinations(range(2**n), 2)]
        rank_sum = sum(sum(row) for row in rank_matrix)
        return rank_sum / (len(f) * len(rank_matrix))
    
    def quaternionic_automorphisms_count(f):
        n = int(math.log2(len(f)))
        count = 0
        for a in range(1, 2**n):
            if all((f[i ^ (a & (1 << j))] == f[(i + 1) % len(f) ^ (a & (1 << j))]) for j in range(n)):
                count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_complexity_rank_variance(f)
        q_automorphisms_count = quaternionic_automorphisms_count(f)
        results.append((n, C_f, q_automorphisms_count))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    C_values = [C_f for _, C_f, _ in results]
    q_automorphisms_counts = [q_automorphisms_count for _, _, q_automorphisms_count in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = (sum((x[i] - mean_x)**2 for i in range(n)) / n)**0.5
        std_dev_y = (sum((y[i] - mean_y)**2 for i in range(n)) / n)**0.5
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation = pearson_correlation(q_automorphisms_counts, [math.sqrt(C_f) for C_f in C_values])
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation > 0.7 and all(cor >= 0.5 for cor in [correlation] * 30),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")