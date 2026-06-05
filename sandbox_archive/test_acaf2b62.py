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
    
    def dpll(instance, assignment, free_vars, clause_set):
        if not clause_set:
            return True
        if not free_vars:
            return False
        
        p = free_vars[0]
        new_assignment = assignment[:]
        new_assignment[p] = 0
        if dpll(instance, new_assignment, free_vars[1:], clause_set):
            return True
        
        new_assignment[p] = 1
        if dpll(instance, new_assignment, free_vars[1:], clause_set):
            return True
        
        return False
    
    def compute_dpll_width(instance):
        n = int(math.log2(len(instance)))
        assignment = [None] * (n + 1)
        free_vars = list(range(1, n + 1))
        return dpll(instance, assignment, free_vars, clause_set)
    
    def compute_minimal_order(instance):
        # Placeholder for the actual computation of minimal order
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(instance) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_sat_instance(n)
            min_order = compute_minimal_order(instance)
            dpll_width = compute_dpll_width(instance)
            
            total_metric_value += abs(min_order - dpll_width)
            instances_tested += 1
            n_max = max(n_max, n)
            
            if abs(min_order - dpll_width) > 0.5:
                conjecture_holds = False
                counterexample = f"Instance of size {n} with min_order={min_order} and dpll_width={dpll_width}"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")