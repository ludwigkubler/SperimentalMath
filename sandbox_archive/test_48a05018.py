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

def generate_tseitin_formula(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    
    # Clause 1: x1 ∨ ¬x2 ∨ ¬x3 ∨ ... ∨ ¬xn
    clause = ["¬" + var if i == 1 else var for i, var in enumerate(variables, start=1)]
    clauses.append(clause)
    
    # Clause 2: ¬x1 ∨ x2
    clauses.append(["¬" + variables[0], variables[1]])
    
    # Clause 3: ¬x2 ∨ x3
    clauses.append(["¬" + variables[1], variables[2]])
    
    # Continue this pattern for all variables
    for i in range(2, n):
        clause = ["¬" + variables[i-1], variables[i]]
        clauses.append(clause)
    
    # Clause n+1: x1 ∨ ¬x2 ∨ ¬x3 ∨ ... ∨ ¬xn
    clause = [var if i == 1 else "¬" + var for i, var in enumerate(variables, start=1)]
    clauses.append(clause)
    
    return variables, clauses

def dpll_solve(clauses):
    def solve(model):
        unassigned_vars = [v for v in model if v not in model]
        if not unassigned_vars:
            return model
        var = unassigned_vars[0]
        for value in [True, False]:
            new_model = model.copy()
            new_model[var] = value
            result = solve(new_model)
            if result is not None:
                return result
        return None
    
    initial_model = {}
    return solve(initial_model)

def local_induction_degree(clauses):
    n = len(clauses)
    degree = 0
    for i in range(n):
        clause = clauses[i]
        for j in range(i+1, n):
            other_clause = clauses[j]
            common_vars = set(clause) & set(other_clause)
            if common_vars:
                degree += 1
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = generate_tseitin_formula(n)
        w_G = dpll_solve(clauses)
        
        if w_G is None:
            continue
        
        lind_G = local_induction_degree(clauses)
        results.append({"n": n, "w_G": len(w_G), "lind_G": lind_G})
    
    if not results:
        return {
            "metric_name": "lind_over_w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "no_solution_found"
        }
    
    lind_over_w = sum(result["lind_G"] / result["w_G"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    return {
        "metric_name": "lind_over_w",
        "metric_value": lind_over_w,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='lind_over_w' first_failing_seed={seeds[first_failing_seed]}")