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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def permute(f, p):
        return [f[p[i]] for i in range(len(f))]
    
    def is_permutation(p):
        return len(p) == len(set(p)) and all(i in p for i in range(len(p)))
    
    def generate_group_elements(n):
        elements = []
        for i in range(2**n):
            perm = [i]
            while True:
                next_i = (perm[-1] * 3 + 1) % (2**n)
                if next_i == i:
                    break
                perm.append(next_i)
            elements.append(perm)
        return elements
    
    def is_group(elements):
        n = len(elements[0])
        for g in elements:
            if not is_permutation(g):
                return False
        for g1 in elements:
            for g2 in elements:
                if (g1 * [g2[i] for i in range(n)]) not in elements:
                    return False
        return True
    
    def group_order(elements):
        n = len(elements[0])
        return sum(len(g) for g in elements)
    
    def communication_complexity(f, n):
        # Simplified version of a communication complexity measure
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        group_elements = generate_group_elements(n)
        if not is_group(group_elements):
            return {
                "metric_name": "group_order",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        order = group_order(group_elements)
        cc = communication_complexity(f, n)
        results.append((order, cc))
    
    if len(results) < 30:
        return {
            "metric_name": "group_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    orders, ccs = zip(*results)
    mean_order = sum(orders) / len(orders)
    mean_cc = sum(ccs) / len(ccs)
    std_order = math.sqrt(sum((x - mean_order) ** 2 for x in orders) / len(orders))
    std_cc = math.sqrt(sum((x - mean_cc) ** 2 for x in ccs) / len(ccs))
    
    correlation_coefficient = sum((order - mean_order) * (cc - mean_cc) for order, cc in results)
    correlation_coefficient /= len(results) * std_order * std_cc
    
    return {
        "metric_name": "group_order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")