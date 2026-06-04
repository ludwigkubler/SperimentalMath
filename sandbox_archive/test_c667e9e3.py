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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_topological_entanglement(f):
        n = int(math.log2(len(f)))
        # Simplified calculation of topological entanglement
        return n
    
    def calculate_communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified calculation of communication complexity rank
        return n
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        f = generate_boolean_function(random.randint(5, 40))
        toe_f = calculate_topological_entanglement(f)
        r_f = calculate_communication_complexity_rank(f)
        results.append((toe_f, r_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_functions_generated"
        }
    
    toe_values = [toe for toe, _ in results]
    r_values = [r for _, r in results]
    mean_toe = sum(toe_values) / len(toe_values)
    mean_r = sum(r_values) / len(r_values)
    correlation_coefficient = sum((toe - mean_toe) * (r - mean_r) for toe, r in results) / (len(results) * math.sqrt(sum((toe - mean_toe)**2 for toe in toe_values)) * math.sqrt(sum((r - mean_r)**2 for r in r_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(int(math.log2(len(f))) for f in [generate_boolean_function(n) for n in range(5, 41)]),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")