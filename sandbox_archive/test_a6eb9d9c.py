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
        if 2**n != len(f):
            return float('inf')  # Invalid function size
        toe = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    toe += 1
        return toe
    
    def calculate_communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        toe = calculate_topological_entanglement(f)
        r = calculate_communication_complexity_rank(f)
        results.append((toe, r))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    toe_values, r_values = zip(*results)
    mean_toe = sum(toe_values) / len(toe_values)
    mean_r = sum(r_values) / len(r_values)
    correlation_coefficient = (sum((toe - mean_toe) * (r - mean_r) for toe, r in results) /
                                math.sqrt(sum((toe - mean_toe)**2 for toe in toe_values) *
                                          sum((r - mean_r)**2 for r in r_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit()
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")