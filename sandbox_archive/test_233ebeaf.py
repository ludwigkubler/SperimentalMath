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
    
    def communication_complexity(n):
        # Placeholder for actual communication complexity calculation
        return n * (n - 1) // 2
    
    def min_aut(n):
        # Placeholder for actual automorphism class counting
        if n <= 1:
            return 0
        return int(math.log(n, 2))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        c_phi = communication_complexity(n)
        min_aut_phi = min_aut(n)
        
        if min_aut_phi < math.log(n, 2) or min_aut_phi > n**2:
            return {
                "metric_name": "min_aut",
                "metric_value": None,
                "instances_tested": len(results),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((c_phi, min_aut_phi))
    
    if not results:
        return {
            "metric_name": "min_aut",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(n for _, _ in results)
    instances_tested = len(results)
    conjecture_holds = all(min_aut_phi >= math.log(c_phi, 2) and min_aut_phi <= c_phi**2 for c_phi, min_aut_phi in results)
    counterexample = "" if conjecture_holds else "min_aut out of bounds"
    
    return {
        "metric_name": "min_aut",
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result["conjecture_holds"]:
            break
        results.append(trial_result["metric_value"])
    
    if len(results) == len(seeds):
        mean_C = sum(results) / len(results)
        std_C = math.sqrt(sum((x - mean_C)**2 for x in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif trial_result["counterexample"]:
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")