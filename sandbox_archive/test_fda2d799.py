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

def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(2 * n)]
    clauses = []
    
    # Clause 1: x0 ∨ ¬x1
    clauses.append([variables[0], -variables[1]])
    
    # Clause 2: ¬x0 ∨ x2
    clauses.append([-variables[0], variables[2]])
    
    # Clause 3: x1 ∨ x3
    clauses.append([variables[1], variables[3]])
    
    # Clause 4: ¬x2 ∨ ¬x3
    clauses.append([-variables[2], -variables[3]])
    
    return clauses

def dpll_solver(clauses):
    assignment = {}
    
    def solve():
        if not clauses:
            return True
        
        literal = find_pure_literal(clauses)
        if literal is not None:
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if solve():
                return True
            del assignment[literal]
        
        literal = find_unit_clause(clauses)
        if literal is not None:
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if solve():
                return True
            del assignment[literal]
        
        literal = random.choice([l for l in range(-2 * n + 1, 2 * n) if l not in assignment])
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if solve():
            return True
        
        del assignment[literal]
        assignment[-literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if solve():
            return True
        
        del assignment[-literal]
        return False
    
    def find_pure_literal(clauses):
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal in pure_literals:
                    pure_literals[literal] = None
                elif -literal not in pure_literals:
                    pure_literals[literal] = True
        
        for literal, _ in pure_literals.items():
            return literal
        
        return None
    
    def find_unit_clause(clauses):
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        
        for literal in unit_clauses:
            return literal
        
        return None
    
    return solve()

def minimal_representation_rank(n):
    clauses = tseitin_formula(n)
    rank = dpll_solver(clauses)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        rank = minimal_representation_rank(n)
        width = dpll_solver(clauses)  # This is a placeholder; actual width calculation needed
        
        if rank is None or width is None:
            continue
        
        total_rank += rank
        total_width += width
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_rank * mean_width,  # Placeholder; actual correlation calculation needed
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")