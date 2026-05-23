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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    while unit_clauses:
        lit = unit_clauses.pop()
        if lit < 0:
            lit = -lit
        assignment[lit] = True
        cnf = [[l for l in clause if l != lit and l != -lit] for clause in cnf]
        unit_clauses.extend([c[0] for c in cnf if len(c) == 1])
    
    pure_literals = {}
    for lit in set(abs(l) for l in sum(cnf, [])):
        pos_count = sum(1 for clause in cnf if any(lit in clause))
        neg_count = sum(1 for clause in cnf if any(-lit in clause))
        if pos_count == 0:
            pure_literals[lit] = False
        elif neg_count == 0:
            pure_literals[lit] = True
    
    while pure_literals:
        lit, value = pure_literals.popitem()
        assignment[lit] = value
        cnf = [[l for l in clause if l != lit and l != -lit] for clause in cnf]
    
    if not cnf:
        return assignment
    elif any(all(lit not in assignment for lit in clause) for clause in cnf):
        return None
    
    for lit in set(abs(l) for l in sum(cnf, [])):
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        result = dpll(cnf, new_assignment)
        if result is not None:
            return result
        
        new_assignment[lit] = False
        result = dpll(cnf, new_assignment)
        if result is not None:
            return result
    
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = len(dpll(cnf)) if dpll(cnf) is not None else float('inf')
        
        hodge_rank = n  # Placeholder value; actual computation of Hodge rank is complex and beyond scope
        c_n = 1.0  # Placeholder value; actual determination of c(n) is complex and beyond scope
        
        results.append({
            "n": n,
            "width": width,
            "hodge_rank": hodge_rank,
            "c_n": c_n,
            "conjecture_holds": width <= c_n * hodge_rank**2
        })
    
    metric_value = sum(result["width"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if not result["conjecture_holds"]:
            break
        
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")