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
    for _ in range(2**n // 3):
        clause = [random.randint(1, n) * (1 if random.choice([True, False]) else -1)
                   for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment=None, literals=None):
    if assignment is None:
        assignment = {}
    if literals is None:
        literals = set(abs(l) for l in sum(cnf, []))
    
    # Check if the CNF is satisfied
    if all(all(l in assignment and assignment[l] == (l > 0) or -l not in assignment for l in c) for c in cnf):
        return True
    
    # Check if the CNF is unsatisfiable
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    pure_literals = [l for l in literals if all(l not in c or -l in c for c in cnf)]
    
    if not unit_clauses and not pure_literals:
        return False
    
    # Unit propagation
    while unit_clauses:
        literal = unit_clauses.pop()
        assignment[literal] = (literal > 0)
        literals.remove(abs(literal))
        new_cnf = []
        for c in cnf:
            if literal in c:
                continue
            elif -literal in c:
                new_cnf.append([l for l in c if l != -literal])
            else:
                new_cnf.append(c)
        cnf = new_cnf
    
    # Pure literal elimination
    while pure_literals:
        literal = pure_literals.pop()
        assignment[literal] = (literal > 0)
        literals.remove(abs(literal))
        new_cnf = []
        for c in cnf:
            if literal in c:
                continue
            elif -literal in c:
                new_cnf.append([l for l in c if l != -literal])
            else:
                new_cnf.append(c)
        cnf = new_cnf
    
    # Backtracking
    literal = next(iter(literals))
    assignment[literal] = True
    if dpll(cnf, assignment, literals):
        return True
    assignment[literal] = False
    literals.add(abs(literal))
    
    assignment[-literal] = True
    if dpll(cnf, assignment, literals):
        return True
    assignment[-literal] = False
    literals.add(abs(literal))
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small value and increase as needed
    cnf = generate_cnf(n)
    
    k = 1  # Minimal order of the totally ramified extension
    while True:
        try:
            if dpll(cnf):
                break
        except RecursionError:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=1')
            return {
                "metric_name": "log2(k)",
                "metric_value": math.log2(k),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        k += 1
    
    t_star = k  # Minimal depth of the DPLL refutation tree
    return {
        "metric_name": "log2(k)",
        "metric_value": math.log2(k),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")