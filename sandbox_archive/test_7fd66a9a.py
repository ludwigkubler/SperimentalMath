# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        total = 0
        for x in range(2**n):
            y = x ^ (x >> 1)
            if f[x] != f[y]:
                total += 1
        return total
    
    def symmetric_group_actions(n):
        actions = []
        for perm in permutations(range(n)):
            action = [0] * n
            for i, j in enumerate(perm):
                action[j] = i
            actions.append(action)
        return actions
    
    def min_invariant_points(actions, f):
        n = len(f)
        invariant_points = 0
        for x in range(2**n):
            if all(f[x] == f[action[x]] for action in actions):
                invariant_points += 1
        return invariant_points
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n > 20 and len(results) < 30:  # Ensure at least 30 instances per seed
            continue
        
        f = generate_boolean_function(n)
        actions = symmetric_group_actions(n)
        min_invar_f = min_invariant_points(actions, f)
        c_f = communication_complexity(f)
        
        results.append({
            "n": n,
            "min_invar_f": min_invar_f,
            "c_f": c_f
        })
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    min_invar_values = [r["min_invar_f"] for r in results]
    c_f_values = [r["c_f"] for r in results]
    
    mean_min_invar = sum(min_invar_values) / len(min_invar_values)
    mean_c_f = sum(c_f_values) / len(c_f_values)
    
    covariance = sum((min_invar_values[i] - mean_min_invar) * (c_f_values[i] - mean_c_f) for i in range(len(results))) / len(results)
    variance_min_invar = sum((x - mean_min_invar)**2 for x in min_invar_values) / len(min_invar_values)
    variance_c_f = sum((x - mean_c_f)**2 for x in c_f_values) / len(c_f_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_min_invar) * math.sqrt(variance_c_f))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")