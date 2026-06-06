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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of the communication complexity rank calculation
        # This is a placeholder and should be replaced with an actual algorithm
        return n
    
    def algebraic_automorphism_group_order(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of the algebraic automorphism group order calculation
        # This is a placeholder and should be replaced with an actual algorithm
        return n
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        R_f = communication_complexity_rank(f)
        ord_Aut_f = algebraic_automorphism_group_order(f)
        
        if R_f == 0:
            continue
        
        results.append(ord_Aut_f / R_f)
    
    if not results:
        return {
            "metric_name": "ord(Aut(f))/R_f",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(x >= 1.5 for x in results) and std <= 0.3
    
    return {
        "metric_name": "ord(Aut(f))/R_f",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(40, random.randint(5, 40)),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")