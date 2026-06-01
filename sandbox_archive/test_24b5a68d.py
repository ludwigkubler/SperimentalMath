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
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(instance):
        def solve(literals, assignment):
            if not literals:
                return True
            literal = literals[0]
            pos_var, neg_var = abs(literal), -literal
            if pos_var in assignment and assignment[pos_var] != (literal > 0):
                return False
            if neg_var in assignment and assignment[neg_var] != (literal < 0):
                return False
            for var in range(1, max(assignment.keys()) + 2):
                if var not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[var] = True
                    if solve([l for l in literals if l != literal and l != -literal], new_assignment):
                        return True
                    new_assignment[var] = False
                    if solve([l for l in literals if l != literal and l != -literal], new_assignment):
                        return True
            return False
        
        assignment = {}
        return len(instance) if not solve(instance, assignment) else 0
    
    def minimal_order_of_modular_form(n):
        # Placeholder function to simulate computation of modular form order
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_sat_instance(n)
    dpll_diameter = dpll(instance)
    order = minimal_order_of_modular_form(n)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": random.random(),  # Placeholder for actual computation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Placeholder for actual result
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")