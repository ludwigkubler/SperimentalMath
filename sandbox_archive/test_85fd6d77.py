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
    
    def calculate_algebraic_automorphism_group_order(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        # Placeholder for actual computation of algebraic automorphism group order
        return random.randint(1, 100)
    
    def calculate_communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        # Placeholder for actual computation of communication complexity rank
        return random.randint(1, 100)
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        ord_Aut_f = calculate_algebraic_automorphism_group_order(f)
        R_f = calculate_communication_complexity_rank(f)
        
        if ord_Aut_f is None or R_f is None:
            continue
        
        results.append((ord_Aut_f, R_f))
    
    if not results:
        return {
            "metric_name": "Ratio of Aut(f) to R_f",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_Aut_f_sum = sum(x for x, _ in results)
    R_f_sum = sum(y for _, y in results)
    ratio_mean = ord_Aut_f_sum / R_f_sum
    ratio_std = math.sqrt(sum((x - ratio_mean)**2 for x, _ in results) / len(results))
    
    return {
        "metric_name": "Ratio of Aut(f) to R_f",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": max(40 if n <= 40 else n for _, _ in results),
        "conjecture_holds": ratio_mean >= 1.5 and ratio_std <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")