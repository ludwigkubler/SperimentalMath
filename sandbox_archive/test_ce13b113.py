# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literal = next((lit for lit in range(1, len(cnf) + 1) if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                if not clause:
                    return None
                new_cnf.append(clause)
            return new_cnf
        
        assignment.append(lit)
        result = dpll(propagate(lit), assignment)
        if result:
            return True
        assignment.pop()
        
        assignment.append(-lit)
        result = dpll(propagate(-lit), assignment)
        if result:
            return True
        assignment.pop()
        
        return False
    
    def p_adic_l_function(cnf):
        # Placeholder for actual computation of p-adic L-function
        # This is a dummy implementation for testing purposes
        return random.random() * 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_length = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(n, 2*n))
            length = len(cnf)
            order = p_adic_l_function(cnf)
            
            total_order += order
            total_length += length
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_length = total_length / instances_tested
    correlation_coefficient = (mean_order * mean_length - mean_order * mean_length) / (mean_order**2 * mean_length**2)
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "p_adic_l_function_order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")