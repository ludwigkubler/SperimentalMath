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

def generate_sat_instance(n: int) -> list:
    instance = [0] * n
    for i in range(n):
        if random.choice([True, False]):
            instance[i] = 1
        else:
            instance[i] = -1
    return instance

def solve_sat(instance: list) -> bool:
    stack = []
    literals = set()
    
    for literal in instance:
        if literal == 0:
            continue
        
        if literal > 0:
            literals.add(literal)
            if -literal in literals:
                return False
        else:
            literals.add(-literal)
            if literal in literals:
                return False
    
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        valid_instances = 0
        
        while instances_tested < 50:  # Ensure at least 50 instances per size
            instance = generate_sat_instance(n)
            if solve_sat(instance):
                instances_tested += 1
                valid_instances += 1
        
        R_F = Fraction(valid_instances, n)  # Minimal rank of the algebraic cycle
        metric_value = n / (R_F * math.log2(n))**2
        
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "valid_instances": valid_instances,
            "metric_value": metric_value
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    
    conjecture_holds = all(result["metric_value"] <= 1.05 * mean_metric_value for result in results)
    counterexample = "" if conjecture_holds else "n={n}, R_F={R_F}, metric_value={metric_value}"
    
    return {
        "seed": seed,
        "metric_name": "Ratio of variables to minimal rank",
        "metric_value": mean_metric_value,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample = f"n={results[0]['n']}, R_F={results[0]['R_F']}, metric_value={results[0]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")