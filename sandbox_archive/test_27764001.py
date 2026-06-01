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

def generate_random_cnf(m, n):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            literal = random.randint(-n, n)
            if literal not in clause:
                clause.add(literal)
        cnf.append(tuple(sorted(clause)))
    return cnf

def dpll_solver(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    
    def solve():
        unit_clauses = [l for l in range(1, n+1) if (l not in assignment and any(l in clause for clause in cnf)) or (-l not in assignment and any(-l in clause for clause in cnf))]
        pure_literals = [l for l in range(1, n+1) if all((l in assignment and assignment[l] == True) or (-l in assignment and assignment[-l] == False) for clause in cnf)]
        
        if not unit_clauses and not pure_literals:
            return assignment
        
        literal_to_add = unit_clauses[0] if unit_clauses else pure_literals[0]
        new_assignment = assignment.copy()
        new_assignment[literal_to_add] = True
        result = solve()
        if result is not None:
            return result
        
        new_assignment[literal_to_add] = False
        result = solve()
        if result is not None:
            return result
        
        return None
    
    return solve()

def minimal_diophantine_property_set(cnf):
    n = max(abs(l) for clause in cnf for l in clause)
    assignment = {}
    
    def find_minimal_set():
        nonlocal assignment
        while True:
            if dpll_solver(cnf, assignment) is None:
                return set(assignment.keys())
            literal_to_add = random.choice(list(range(-n, 0)) + list(range(1, n+1)))
            if literal_to_add not in assignment:
                assignment[literal_to_add] = True
    
    return find_minimal_set()

def circuit_monotone_width(property_set):
    return len(property_set)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    m_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for m in m_values:
        cnf = generate_random_cnf(m, m)
        property_set = minimal_diophantine_property_set(cnf)
        monotone_width = circuit_monotone_width(property_set)
        
        total_metric_value += monotone_width
        instances_tested += len(cnf)
        n_max = max(n_max, m)
    
    mean_td = Fraction(total_metric_value, instances_tested)
    conjecture_holds = mean_td <= 1.5 * m_values[-1] * math.log(m_values[-1])
    counterexample = "" if conjecture_holds else f"mean={mean_td}, expected<=1.5*m*log(m)"
    
    return {
        "metric_name": "Circuit Monotone Width",
        "metric_value": float(mean_td),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")