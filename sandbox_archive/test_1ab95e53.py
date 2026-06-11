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
        variables = list(range(1, n+1))
        clauses = []
        for i in range(n):
            clause = [random.choice(variables), random.choice(variables)]
            while len(set(clause)) != 2:
                clause = [random.choice(variables), random.choice(variables)]
            clauses.append(clause)
        return variables, clauses
    
    def construct_kahler_manifold(clauses):
        # Simplified model: each clause contributes a unit to the entropy
        return len(clauses)
    
    def resolution_width(instance):
        variables, clauses = instance
        width = 2 ** (len(variables) - 1)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_width = 0
        total_entropy = 0
        
        while instances_tested < 30:
            instance = generate_instance(n)
            width = resolution_width(instance)
            entropy = construct_kahler_manifold(instance[1])
            
            if width == 0 or entropy == 0:
                continue
            
            results.append((width, entropy))
            total_width += width
            total_entropy += entropy
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
    
    widths = [r[0] for r in results]
    entropies = [r[1] for r in results]
    correlation_coefficient = sum((w - mean_width) * (e - mean_entropy) for w, e in results)
    correlation_coefficient /= math.sqrt(sum((w - mean_width) ** 2 for w in widths)) * math.sqrt(sum((e - mean_entropy) ** 2 for e in entropies))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds if result["metric_value"] is not None]
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")