# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations, chain

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def configuration_space(graph):
    n = len(graph)
    subsets = powerset(range(n))
    config_space = set()
    for subset in subsets:
        config = 0
        for node in subset:
            config |= (1 << node)
        config_space.add(config)
    return len(config_space)

def circuit_depth(graph):
    # Placeholder function to compute the depth of a circuit computing a function on the graph
    # This is a dummy implementation and should be replaced with actual circuit computation logic
    n = len(graph)
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        r = configuration_space(graph)
        d_C = circuit_depth(graph)
        results.append((r, d_C))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    r_values = [r for r, _ in results]
    d_C_values = [d_C for _, d_C in results]
    n_tested = len(results)
    n_max = max(n_values)
    
    # Calculate correlation coefficient
    mean_r = sum(r_values) / n_tested
    mean_d_C = sum(d_C_values) / n_tested
    numerator = sum((r - mean_r) * (d_C - mean_d_C) for r, d_C in results)
    denominator = (sum((r - mean_r)**2 for r in r_values) * sum((d_C - mean_d_C)**2 for d_C in d_C_values))**0.5
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tested,
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
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")