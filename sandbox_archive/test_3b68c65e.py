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
    
    def communication_complexity(phi):
        n = int(math.log2(len(phi)))
        count = 0
        for i in range(2**n):
            if phi[i] != phi[2*i]:
                count += 1
        return count
    
    def lefschetz_thimble_rank(phi):
        # Placeholder function to simulate Lefschetz thimble rank calculation
        n = int(math.log2(len(phi)))
        return random.randint(1, n)
    
    results = []
    for _ in range(30):
        phi = generate_boolean_function(random.randint(5, 40))
        c_phi = communication_complexity(phi)
        lr_phi = lefschetz_thimble_rank(phi)
        results.append((c_phi, lr_phi))
    
    if not results:
        return {
            "metric_name": "Lr(c)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c_values = [c for c, _ in results]
    lr_values = [lr for _, lr in results]
    
    n_max = max(len(phi) for phi, _ in results)
    
    # Pearson correlation coefficient
    mean_c = sum(c_values) / len(c_values)
    mean_lr = sum(lr_values) / len(lr_values)
    numerator = sum((c - mean_c) * (lr - mean_lr) for c, lr in results)
    denominator = math.sqrt(sum((c - mean_c)**2 for c in c_values)) * math.sqrt(sum((lr - mean_lr)**2 for lr in lr_values))
    
    if denominator == 0:
        return {
            "metric_name": "Lr(c)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Lr(c)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")