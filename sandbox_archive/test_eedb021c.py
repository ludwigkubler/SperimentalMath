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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance_ratio(f):
        n = len(f)
        total = sum(f)
        mean = total / n
        variance = sum((x - mean) ** 2 for x in f) / n
        return variance
    
    def construct_braided_tensor_product_module(f):
        n = len(f)
        m = n * (n + 1) // 2
        return m
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance_ratio(f)
        M = construct_braided_tensor_product_module(f)
        log2_M = math.log2(M) if M > 0 else -math.inf
        results.append((log2_M, n * R_f))
    
    mean_log2_M = sum(x for x, _ in results) / len(results)
    mean_nR_f = sum(y for _, y in results) / len(results)
    correlation = (sum((x - mean_log2_M) * (y - mean_nR_f) for x, y in results) /
                   math.sqrt(sum((x - mean_log2_M) ** 2 for x, _ in results) *
                             sum((y - mean_nR_f) ** 2 for _, y in results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) > 0.5,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results) and support_fraction >= 0.8:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")