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
    
    def generate_instance(n):
        return [random.choice([True, False]) for _ in range(2**n)]
    
    def dpll(clauses):
        assignment = {}
        
        def backtrack(clauses, assignment):
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                value = literal > 0
                assignment[literal] = value
                return backtrack(clauses, assignment)
            
            if not clauses:
                return True
            
            literal = next((c for c in clauses if c and c[0] > 0), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            if backtrack(clauses, assignment):
                return True
            del assignment[literal]
            
            assignment[-literal] = True
            if backtrack(clauses, assignment):
                return True
            del assignment[-literal]
        
        clauses = [c for c in instance if any(lit in assignment or -lit in assignment for lit in c)]
        return backtrack(clauses, assignment)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            instance = generate_instance(n)
            if dpll(instance):
                instances_tested += 1
                msl = len(instance)  # Minimal symplectic form is the number of clauses
                metric_values.append(math.log(msl))
    
    mean_msl = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_msl) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = sum((x - mean_msl) * (math.log(n**2) - math.log(5**2)) for n, x in zip(range(5, n_max + 1), metric_values)) / len(metric_values)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "log(minimal_symplectic_form)",
        "metric_value": mean_msl,
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
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_msl = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msl) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "correlation_coefficient < 0.8" for r in results) and sum(1 for r in results if r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")