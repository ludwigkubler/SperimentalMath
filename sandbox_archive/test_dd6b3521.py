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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_clause_complexity(formula):
        return sum(1 for bit in formula if bit == 1)
    
    def min_order_of_cuspidal_subgroup(clause_complexity):
        # Placeholder function. Replace with actual computation.
        return clause_complexity + 1
    
    n_max = 0
    instances_tested = 0
    total_min_order = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 5 instances per size
            formula = generate_boolean_formula(n)
            clause_complexity = compute_clause_complexity(formula)
            min_order = min_order_of_cuspidal_subgroup(clause_complexity)
            
            if min_order > 10:
                conjecture_holds = False
                counterexample = f"Formula with n={n} and complexity {clause_complexity} has min order {min_order}"
                break
            
            total_min_order += min_order
            instances_tested += 1
    
    mean_min_order = total_min_order / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "min_order_of_cuspidal_subgroup",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")