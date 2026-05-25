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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        clauses.append([var])
        clauses.append([-var])
    
    # Generate clauses for implications
    for i in range(n):
        for j in range(i+1, n):
            clauses.append([f'x{i}', -f'x{j}'])
            clauses.append([-f'x{i}', f'x{j}'])
            clauses.append([f'x{j}', -f'x{i}'])
            clauses.append([-f'x{j}', f'x{i}'])
    
    # Generate clauses for the final implication
    for i in range(n):
        clauses.append([f'x{i}', 'F'])
        clauses.append([-f'x{i}', -'F'])
    
    return clauses

def dpll(clauses, model={}):
    unit_clauses = [l for l in range(1, len(clauses) + 1) if any(l in c for c in clauses)]
    pure_symbols = {}
    
    while True:
        # Unit propagation
        while unit_clauses:
            lit = unit_clauses.pop()
            if lit > 0:
                model[lit] = True
            else:
                model[-lit] = False
            
            new_clauses = []
            for c in clauses:
                if lit in c:
                    continue
                elif -lit in c:
                    new_clauses.append([l for l in c if l != -lit])
                else:
                    new_clauses.append(c)
            
            unit_clauses.extend([l for l in range(1, len(new_clauses) + 1) if any(l in c for c in new_clauses)])
            clauses = new_clauses
        
        # Pure literal elimination
        for lit in set(model):
            if -lit not in model:
                pure_symbols[lit] = True
                new_clauses = []
                for c in clauses:
                    if lit in c:
                        continue
                    elif -lit in c:
                        new_clauses.append([l for l in c if l != -lit])
                    else:
                        new_clauses.append(c)
                
                unit_clauses.extend([l for l in range(1, len(new_clauses) + 1) if any(l in c for c in new_clauses)])
                clauses = new_clauses
        
        # Backtracking
        if not clauses:
            return True
        if not model:
            return False
        
        var = next(k for k in range(1, len(clauses) + 1) if k not in model and -k not in model)
        if any(var in c for c in clauses):
            result = dpll(clauses, {**model, var: True})
            if result:
                return True
        if any(-var in c for c in clauses):
            result = dpll(clauses, {**model, -var: False})
            if result:
                return True
        
        return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    clauses = generate_tseitin_formula(n)
    resolution_length = dpll(clauses)
    
    h_n_g = sum(1 for c in clauses if len(c) == 2)  # Simplified H_n(G) for Tseitin formulas
    
    if h_n_g <= math.log(n, 2) * math.log(n, 2) * math.log(n, 2):
        counterexample = f"H_n(G) ≤ {h_n_g} log^3({n})"
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")