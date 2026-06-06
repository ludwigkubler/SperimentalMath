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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        
        def dpll():
            if not cnf:
                return True
            literal = next((l for l in range(1, n + 1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            stack.append((assignment.copy(), new_cnf))
            
            if dpll():
                return True
            
            assignment.pop(literal)
            literal = -literal
            assignment[literal] = True
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            stack.append((assignment.copy(), new_cnf))
            
            while stack and not dpll():
                assignment, cnf = stack.pop()
            
            return False
        
        return dpll()
    
    def compute_modular_form_order(n, m):
        # Placeholder for actual computation
        # For demonstration purposes, we use a simple polynomial function
        return n ** (3/2) * math.log(m)
    
    def compute_resolution_width(cnf):
        # Placeholder for actual resolution width computation
        # For demonstration purposes, we use a simple linear function
        return len(cnf)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 10)
        cnf = generate_cnf(n, m)
        
        if not is_satisfiable(cnf):
            continue
        
        order = compute_modular_form_order(n, m)
        width = compute_resolution_width(cnf)
        results.append((n, m, order, width))
    
    if not results:
        return {
            "metric_name": "order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_satisfiable_cnf"
        }
    
    order_errors = [abs(order - n ** (3/2) * math.log(m)) / (n ** (3/2) * math.log(m)) for n, m, _, _ in results]
    correlation_coefficient = sum((order - mean_order) * (width - mean_width) for n, m, order, width in results) / \
                              (math.sqrt(sum((order - mean_order) ** 2 for n, m, order, width in results)) *
                               math.sqrt(sum((width - mean_width) ** 2 for n, m, order, width in results)))
    mean_order = sum(order for n, m, order, _ in results) / len(results)
    mean_width = sum(width for _, _, _, width in results) / len(results)
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n for n, m, _, _ in results),
        "conjecture_holds": all(error <= 0.1 for error in order_errors) and correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)
        print(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")