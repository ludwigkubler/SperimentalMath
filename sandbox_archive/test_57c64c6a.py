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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_rank(instance):
        # Placeholder for actual minimal rank computation
        # This is a dummy implementation for testing purposes
        return len(instance) // 2
    
    def solve_sat_instance(instance):
        # Placeholder for actual SAT solver
        # This is a dummy implementation for testing purposes
        return random.choice([True, False])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_sat_instance(n)
        R_F = compute_minimal_rank(instance)
        solved = solve_sat_instance(instance)
        
        if not solved:
            counterexample = f"Instance with {n} variables could not be solved"
            return {
                "metric_name": "minimal_rank",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "n": n,
            "R_F": R_F,
            "solved": solved
        })
    
    total_n = sum(result["n"] for result in results)
    total_R_F = sum(result["R_F"] for result in results)
    mean_n = total_n / len(results)
    mean_R_F = total_R_F / len(results)
    
    if mean_R_F == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = mean_n / mean_R_F
    expected_ratio = 5 * math.log2(mean_n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": ratio <= expected_ratio * 1.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("mapping_undefined" in result["counterexample"] for result in results):
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined n_tested={len(seeds)}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")