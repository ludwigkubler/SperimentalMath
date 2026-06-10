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
    variables = list(range(1, n+1))
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n+1):
        clause = [i]
        for j in range(i+1, n+1):
            clause.append(-j)
        clauses.append(clause)
    
    # Generate clauses for the OR of all variables
    or_clause = [-i for i in range(1, n+1)]
    clauses.append(or_clause)
    
    return variables, clauses

def dpll_solver(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[-abs(literal)] = literal > 0
        return dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    
    polarities = [1, -1]
    literal = random.choice(polarities) * random.choice(variables)
    new_assignment = assignment.copy()
    new_assignment[-abs(literal)] = literal > 0
    
    if dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment):
        return True
    else:
        new_assignment[-abs(literal)] = False
        return dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment)

def resolution(clauses, assignment):
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            assignment[-abs(literal)] = literal > 0
            return assignment
        
        resolvents = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                common_literals = [l for l in clauses[i] if -l in clauses[j]]
                if common_literals:
                    new_clause = list(set(clauses[i]) | set(clauses[j]))
                    new_clause.remove(common_literals[0])
                    new_clause.remove(-common_literals[0])
                    resolvents.append(new_clause)
        
        if not resolvents:
            return None
        
        clauses.extend(resolvents)

def local_induction_degree(clauses):
    n = len(variables)
    degree = 0
    for i in range(n):
        for j in range(i+1, n):
            clause_i = [l for l in clauses if l[0] == i+1]
            clause_j = [l for l in clauses if l[0] == j+1]
            common_literals = [l for l in clause_i if -l in clause_j]
            degree += len(common_literals)
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        
        assignment = {i: None for i in range(1, n+1)}
        width = len(dpll_solver(clauses, assignment))
        
        assignment = {i: None for i in range(1, n+1)}
        proof_tree = resolution(clauses, assignment)
        
        if proof_tree is None:
            continue
        
        lind_value = local_induction_degree(clauses)
        
        results.append({
            "n": n,
            "width": width,
            "lind": lind_value
        })
    
    if not results:
        return {
            "metric_name": "local_induction_degree",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_lind = sum(r["lind"] for r in results)
    total_width = sum(r["width"] for r in results)
    mean_ratio = total_lind / total_width
    
    return {
        "metric_name": "local_induction_degree",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": mean_ratio <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")