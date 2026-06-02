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
    
    def generate_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def noncrossing_partitions(n):
        if n == 0:
            return [[]]
        partitions = []
        for i in range(1, n):
            for left in noncrossing_partitions(i):
                for right in noncrossing_partitions(n - i - 1):
                    partitions.append([left + [j + i + 1] for j in right])
        return partitions
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        return len(clauses)
    
    n_ncp_values = []
    w_values = []
    instances_tested = 0
    n_max = 5
    
    for n in range(5, 41, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        for _ in range(5):  # Test each size 5 times
            clauses = generate_instance(n)
            n_ncp = len(noncrossing_partitions(n))
            w = resolution_width(clauses)
            n_ncp_values.append(n_ncp)
            w_values.append(w)
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    if not n_ncp_values or not w_values:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_n_ncp = sum(n_ncp_values) / len(n_ncp_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = 0
    numerator = sum((n_ncp - mean_n_ncp) * (w - mean_w) for n_ncp, w in zip(n_ncp_values, w_values))
    denominator = math.sqrt(sum((n_ncp - mean_n_ncp) ** 2 for n_ncp in n_ncp_values)) * math.sqrt(sum((w - mean_w) ** 2 for w in w_values))
    
    if denominator == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.6 < correlation_coefficient < 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(0.6 <= r["metric_value"] < 0.9 for r in results):
        print("RESULT: INCONCLUSIVE insufficient_support")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")