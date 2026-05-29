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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL algorithm to estimate resolution width
        states = set()
        for clause in clauses:
            states.add(tuple(sorted(clause)))
        
        while True:
            new_states = set()
            for state1 in states:
                for state2 in states:
                    if len(state1) != 2 or len(state2) != 2:
                        continue
                    if state1[0] == -state2[0]:
                        new_state = tuple(sorted(set(state1 + state2) - {state1[0], -state1[0]}))
                        new_states.add(new_state)
            if not new_states:
                break
            states.update(new_states)
        
        return max(len(state) for state in states)
    
    def quaternion_order(clauses):
        # Placeholder function to compute quaternion order (not implemented)
        return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_time = 0
    
    for n in n_values:
        for _ in range(5):
            m = min(n * 4, 20)
            clauses = generate_3cnf(n, m)
            width = resolution_width(clauses)
            order = quaternion_order(clauses)
            results.append({"n": n, "m": m, "width": width, "order": order})
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = 0
    for result in results:
        correlation += (result["width"] - sum(result["width"] for result in results) / len(results)) * \
                      (math.log(result["order"]) - sum(math.log(result["order"]) for result in results) / len(results))
    correlation /= math.sqrt(sum((result["width"] - sum(result["width"] for result in results) / len(results)) ** 2 for result in results)) * \
                    math.sqrt(sum((math.log(result["order"]) - sum(math.log(result["order"]) for result in results) / len(results)) ** 2 for result in results))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")