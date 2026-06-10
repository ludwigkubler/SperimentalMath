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
    
    def communication_complexity_rank(f):
        n = len(f)
        max_depth = 0
        stack = [(f, 0)]
        while stack:
            current, depth = stack.pop()
            if isinstance(current, list):
                for item in current:
                    stack.append((item, depth + 1))
            else:
                max_depth = max(max_depth, depth)
        return max_depth
    
    def kahler_class_rank(f):
        # Placeholder function to simulate Kähler class rank calculation
        n = len(f)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        k_r = kahler_class_rank(f)
        results.append((n, r_f, k_r))
    
    if not results:
        return {
            "metric_name": "Kähler class rank vs Communication complexity rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    k_r_values = [r for _, r, _ in results]
    r_f_values = [k for _, k, _ in results]
    
    mean_k_r = sum(k_r_values) / len(k_r_values)
    mean_r_f = sum(r_f_values) / len(r_f_values)
    
    n_max = max(n for n, _, _ in results)
    
    correlation_coefficient = sum((k_r - mean_k_r) * (r_f - mean_r_f) for k_r, r_f in zip(k_r_values, r_f_values)) / \
                              math.sqrt(sum((k_r - mean_k_r)**2 for k_r in k_r_values) *
                                        sum((r_f - mean_r_f)**2 for r_f in r_f_values))
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(k_r >= r_f for _, r_f, k_r in results)
    
    return {
        "metric_name": "Kähler class rank vs Communication complexity rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")