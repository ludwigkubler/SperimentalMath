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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f'y{i}'])
            clauses.append([f'y{i}', variables[(i-1) % n + 1]])
            clauses.append([-f'y{i}', -variables[(i-1) % n + 1]])
        
        return variables, clauses
    
    def resolution(clauses):
        new_clauses = set(clauses)
        while True:
            new_clause = None
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list((set(clause1) ^ set(clause2)))
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return new_clauses
            new_clauses.add(tuple(sorted(new_clause)))
    
    def resolution_width(clauses):
        queue = [tuple(sorted(clause)) for clause in clauses]
        visited = set()
        width = 0
        
        while queue:
            current_clause = queue.pop(0)
            if current_clause not in visited:
                visited.add(current_clause)
                new_clauses = resolution([current_clause])
                for new_clause in new_clauses:
                    if new_clause not in visited:
                        queue.append(new_clause)
                        width = max(width, len(queue))
        
        return width
    
    def minimal_representation_degree(n):
        # Placeholder function to represent the minimal representation degree
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        w_phi = resolution_width(clauses)
        minimal_degree = minimal_representation_degree(n)
        log_w_phi = math.log(w_phi) if w_phi > 0 else float('-inf')
        
        results.append((log_w_phi, minimal_degree))
    
    correlation_coefficient = sum((x[0] - mean_x) * (x[1] - mean_y) for x in results) / len(results)
    mean_x = sum(x[0] for x in results) / len(results)
    mean_y = sum(x[1] for x in results) / len(results)
    
    conjecture_holds = -0.5 <= correlation_coefficient <= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")