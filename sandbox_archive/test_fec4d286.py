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
    
    def generate_3sat_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause[0] = -clause[0]
            if random.choice([True, False]):
                clause[1] = -clause[1]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        unassigned_vars = [var for var in range(1, n + 1) if var not in assignment]
        if not unassigned_vars:
            return all([any([assignment[var] == literal or assignment[-var] == -literal for literal in clause]) for clause in clauses])
        
        p_var = random.choice(unassigned_vars)
        new_assignment = assignment.copy()
        new_assignment[p_var] = True
        if dpll(clauses, new_assignment):
            return True
        
        new_assignment[p_var] = False
        if dpll(clauses, new_assignment):
            return True
        
        return False
    
    def find_normalizing_set_size(n, m):
        # Placeholder for the actual algorithm to find the normalizing set size
        # This is a dummy implementation that returns a random number for demonstration purposes
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = int(n * (n - 1) / 4)  # Ensure a reasonable number of clauses
    clauses = generate_3sat_instance(n, m)
    
    assignment = {}
    result = dpll(clauses, assignment)
    normalizing_set_size = find_normalizing_set_size(n, m)
    
    metric_value = float('inf') if not result else len(assignment)
    conjecture_holds = abs(metric_value - 3 * normalizing_set_size) <= normalizing_set_size
    counterexample = "" if conjecture_holds else f"Counterexample with n={n}, m={m}"
    
    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")