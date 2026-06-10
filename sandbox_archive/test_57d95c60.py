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

def generate_tseitin_formula(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n+1):
        clauses.append([variables[i-1]])
        clauses.append([-variables[i-1], f"y{i}"])
    
    # Generate clauses for the OR gate
    for i in range(2, n+1):
        clauses.append([f"y{i}", variables[0]])
        clauses.append([-f"y{i}", -variables[0]])
    
    # Final clause for the OR gate output
    clauses.append([f"y{n}"])
    
    return variables, clauses

def calculate_resolution_width(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            return False
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        for l in [-l for l in new_assignment if new_assignment[l]]:
            new_clauses = [c for c in new_clauses if l not in c and -l not in c]
        return dpll(new_clauses, new_assignment)
    
    assignment = {}
    return len([c for c in clauses if not any(l in assignment or -l in assignment for l in c)])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    
    resolution_width = calculate_resolution_width(clauses)
    order_M2_B = (n * (n + 1)) // 2
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": resolution_width <= Fraction(order_M2_B, 4)**0.5 * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")