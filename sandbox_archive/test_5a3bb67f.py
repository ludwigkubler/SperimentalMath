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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance_ratio(f):
        n = len(f)
        m = 2**n
        rank = 0
        for i in range(m):
            if f[i] == 1:
                rank += 1
        return rank / m
    
    def construct_braided_tensor_product_module(n, f):
        # Construct a simple module based on the function
        M = [f]
        return M
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        R_f = communication_complexity_rank_variance_ratio(f)
        M = construct_braided_tensor_product_module(n, f)
        log_M = math.log2(len(M))
        log_nR_f = math.log2(n) * R_f
        metric_values.append((log_M, log_nR_f))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "log|M| vs. log(n) * R(f)",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_log_M = sum(x[0] for x in metric_values) / len(metric_values)
    mean_log_nR_f = sum(x[1] for x in metric_values) / len(metric_values)
    correlation = 0
    for log_M, log_nR_f in metric_values:
        correlation += (log_M - mean_log_M) * (log_nR_f - mean_log_nR_f)
    correlation /= len(metric_values) * math.sqrt(sum((x[0] - mean_log_M)**2 for x in metric_values)) * math.sqrt(sum((x[1] - mean_log_nR_f)**2 for x in metric_values))
    
    return {
        "metric_name": "log|M| vs. log(n) * R(f)",
        "metric_value": correlation,
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.5,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(30)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_data")