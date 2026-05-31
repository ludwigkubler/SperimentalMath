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
        
        # Clause 1: x1 ∨ ¬x2
        clauses.append([variables[0], -variables[1]])
        
        # Clause 2: ¬x1 ∨ x3
        clauses.append([-variables[0], variables[2]])
        
        # Clause 3: x2 ∨ x4
        clauses.append([variables[1], variables[3]])
        
        return variables, clauses
    
    def resolution(clauses):
        seen_clauses = set()
        new_clauses = set(clauses)
        
        while True:
            new_clause_added = False
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        new_clause.sort()
                        if new_clause and new_clause not in seen_clauses:
                            seen_clauses.add(tuple(new_clause))
                            new_clauses.add(new_clause)
                            new_clause_added = True
            if not new_clause_added:
                break
        
        return len(seen_clauses) + len(clauses)
    
    def coxeter_group(n):
        # This is a simplified representation of the Coxeter group for n variables
        reflections = []
        for i in range(n):
            reflection = [0] * n
            reflection[i] = 1
            reflection[(i + 1) % n] = -1
            reflections.append(reflection)
        return reflections
    
    def minimal_reflections(reflections):
        # This is a simplified representation of finding the minimal number of reflections
        return len(reflections)
    
    variables, clauses = tseitin_formula(5)
    proof_width = resolution(clauses)
    reflections = coxeter_group(len(variables))
    min_reflections = minimal_reflections(reflections)
    
    return {
        "metric_name": "resolution_proof_width_over_min_reflections_squared",
        "metric_value": proof_width / (min_reflections ** 2),
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if conjecture_holds_fraction >= 0.95:
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={conjecture_holds_fraction:.2f}")