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
    
    def communication_rank_variance(f):
        n = len(f)
        count_0 = sum(1 for x in f if x == 0)
        count_1 = n - count_0
        return max(count_0, count_1) / min(count_0, count_1)

    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def quasi_plurality_group(f):
        count_0 = sum(1 for x in f if x == 0)
        count_1 = len(f) - count_0
        if count_0 > count_1:
            return [0] * count_0 + [1] * count_1
        else:
            return [1] * count_1 + [0] * count_0

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        delta_f = communication_rank_variance(f)
        Q_f = quasi_plurality_group(f)
        order_Q_f = len(Q_f)
        
        if delta_f == 0:
            continue
        
        results.append({
            "n": n,
            "delta_f": delta_f,
            "order_Q_f": order_Q_f
        })
    
    if not results:
        return {
            "metric_name": "order_Q_f / delta_f^2",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    order_over_delta_squared = [r["order_Q_f"] / r["delta_f"]**2 for r in results]
    mean_value = sum(order_over_delta_squared) / len(order_over_delta_squared)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in order_over_delta_squared) / len(order_over_delta_squared))
    
    return {
        "metric_name": "order_Q_f / delta_f^2",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(x <= 10 for x in order_over_delta_squared),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] <= 10 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")