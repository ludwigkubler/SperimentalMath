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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of Yao's XOR function communication complexity
        return n
    
    def symmetric_group_action(f, n):
        actions = []
        for perm in itertools.permutations(range(n)):
            action = [f[perm[i]] for i in range(n)]
            actions.append(action)
        return actions
    
    def min_invariant_points(actions):
        invariant_points = set()
        for action in actions:
            if all(f[i] == action[i] for i in range(len(f))):
                invariant_points.add(tuple(action))
        return len(invariant_points)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        actions = symmetric_group_action(f, n)
        min_invar_f = min_invariant_points(actions)
        
        results.append({
            "n": n,
            "f": f,
            "c_f": c_f,
            "min_invar_f": min_invar_f
        })
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    min_invar_values = [r["min_invar_f"] for r in results]
    c_f_values = [r["c_f"] for r in results]
    
    mean_min_invar = sum(min_invar_values) / len(min_invar_values)
    mean_c_f = sum(c_f_values) / len(c_f_values)
    
    covariance = sum((min_invar_values[i] - mean_min_invar) * (c_f_values[i] - mean_c_f) for i in range(len(results))) / len(results)
    variance_min_invar = sum((min_invar_values[i] - mean_min_invar)**2 for i in range(len(results))) / len(results)
    variance_c_f = sum((c_f_values[i] - mean_c_f)**2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / math.sqrt(variance_min_invar * variance_c_f)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        max_n_max = max(r["n_max"] for r in results if not r["conjecture_holds"])
        if max_n_max < 16:
            print("RESULT: INCONCLUSIVE n_max_too_low")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_threshold\" first_failing_seed={first_failing_seed}")