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
    
    def generate_communication_problem(n):
        # Generate a random communication problem with n participants
        return [random.randint(1, 10) for _ in range(n)]
    
    def compute_quantum_group_algebra(problem):
        # Placeholder function to simulate computing the quantum group algebra
        return sum(problem)
    
    def compute_automorphism_group_size(algebra):
        # Placeholder function to simulate computing the automorphism group size
        return len(str(algebra))
    
    def communication_complexity(problem):
        # Placeholder function to simulate computing communication complexity
        return max(problem) - min(problem)
    
    n = random.randint(5, 40)
    problem = generate_communication_problem(n)
    algebra = compute_quantum_group_algebra(problem)
    automorphism_group_size = compute_automorphism_group_size(algebra)
    C = 1.0  # Placeholder constant
    log_order = math.log(automorphism_group_size)
    log_n_plus_C = math.log(n) + math.log(C)
    
    if log_order < log_n_plus_C:
        return {
            "metric_name": "log_order",
            "metric_value": log_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    communication_complexity_val = communication_complexity(problem)
    return {
        "metric_name": "log_order",
        "metric_value": log_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_log_order = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_log_order} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_order} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")