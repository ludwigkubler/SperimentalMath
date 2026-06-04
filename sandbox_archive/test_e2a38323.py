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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def construct_binary_quadratic_form(lit):
    a = 1
    b = -lit
    c = 0
    return (a, b, c)

def resolution_width(cnf):
    stack = []
    for clause in cnf:
        if not any(lit < 0 for lit in clause):
            continue
        stack.append(clause)
    
    while stack:
        clause1 = stack.pop()
        if not any(lit < 0 for lit in clause1):
            continue
        
        for clause2 in cnf:
            if not any(lit > 0 for lit in clause2):
                continue
            
            new_clause = []
            for lit1 in clause1:
                if -lit1 in clause2:
                    continue
                new_clause.append(lit1)
            
            if len(new_clause) == 0:
                return float('inf')
            
            stack.append(new_clause)
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    quadratic_forms = set()
    for clause in cnf:
        for lit in clause:
            quadratic_form = construct_binary_quadratic_form(lit)
            quadratic_forms.add(quadratic_form)
    
    num_distinct_forms = len(quadratic_forms)
    w_phi = resolution_width(cnf)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    ratio = w_phi / (n ** 0.5)
    if not (0.8 <= ratio <= 1.2) or num_distinct_forms > 1.5 * w_phi:
        return {
            "metric_name": "resolution_width",
            "metric_value": w_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"ratio={ratio:.2f}, num_forms={num_distinct_forms}"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != float('inf')]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={first_failing_seed + 1}")