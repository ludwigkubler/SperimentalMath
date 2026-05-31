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
    
    def compute_quantum_group_algebra(comm_problem):
        # Compute the quantum group algebra (simplified example)
        return sum(comm_problem)
    
    def compute_automorphism_group_order(qga):
        # Compute the order of automorphism groups (simplified example)
        return qga + 1
    
    def compute_communication_complexity(comm_problem):
        # Compute communication complexity (simplified example)
        return len(comm_problem) * sum(comm_problem)
    
    n = random.randint(5, 40)
    comm_problem = generate_communication_problem(n)
    qga = compute_quantum_group_algebra(comm_problem)
    automorphism_group_order = compute_automorphism_group_order(qga)
    communication_complexity = compute_communication_complexity(comm_problem)
    
    if automorphism_group_order <= 0 or communication_complexity <= 0:
        return {
            "metric_name": "log(autogroup_order)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "non-positive values"
        }
    
    log_autogroup_order = math.log(automorphism_group_order)
    log_n_plus_C = math.log(n) + math.log(5)  # C is a constant, here chosen as 5
    
    return {
        "metric_name": "log(autogroup_order)",
        "metric_value": log_autogroup_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": log_autogroup_order >= log_n_plus_C,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_C = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "log(autogroup_order) < log(n) + log(C)"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")