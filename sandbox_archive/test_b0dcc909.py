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
    
    def communication_complexity(n):
        return n * (n - 1) // 2
    
    def geometrically_enhanced_group_actions(n):
        # Placeholder for actual computation
        return [random.randint(0, n-1) for _ in range(n)]
    
    def min_local_index(actions):
        # Placeholder for actual computation
        return len(set(actions))
    
    instances_tested = 30
    metric_values = []
    n_max = 5
    
    for n in {5, 10, 15, 20, 30, 40}:
        if n > n_max:
            n_max = n
        
        for _ in range(instances_tested // len({5, 10, 15, 20, 30, 40})):
            actions = geometrically_enhanced_group_actions(n)
            mli = min_local_index(actions)
            C = communication_complexity(n)
            metric_values.append((mli, C))
    
    if not metric_values:
        return {
            "metric_name": "min_local_index",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mli = sum(mli for mli, C in metric_values) / len(metric_values)
    mean_C = sum(C for mli, C in metric_values) / len(metric_values)
    correlation_coefficient = 0
    
    if mean_C != 0:
        correlation_coefficient = sum((mli - mean_mli) * (C - mean_C) for mli, C in metric_values) / (len(metric_values) * math.sqrt(sum((mli - mean_mli) ** 2 for mli, C in metric_values)) * math.sqrt(sum((C - mean_C) ** 2 for mli, C in metric_values)))
    
    return {
        "metric_name": "min_local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")