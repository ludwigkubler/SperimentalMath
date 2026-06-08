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
    
    def generate_random_boolean_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n - 1):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [f'-{v}' if v.startswith('-') else f'-{v}' for v in clause]
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def tseitin_formula(formula):
        n = len(formula.split())
        literals = set()
        for i in range(n):
            literals.add(f'x{i}')
            literals.add(f'-x{i}')
        
        clauses = []
        for literal in literals:
            if literal.startswith('-'):
                continue
            clause = [f'{literal}', f'-{literal}']
            clauses.append(' or '.join(clause))
        
        return ' and '.join(clauses)
    
    def dpll(formula):
        # Simplified DPLL solver
        variables = set()
        for literal in formula.split():
            if literal.startswith('-'):
                continue
            variables.add(literal)
        
        stack = []
        assignment = {}
        for variable in variables:
            stack.append((variable, True))
            stack.append((variable, False))
        
        def backtrack():
            while stack:
                literal, value = stack.pop()
                if literal not in assignment:
                    assignment[literal] = value
                    break
            else:
                return None
            
            new_formula = formula.replace(literal, str(value)).replace(f'-{literal}', str(not value))
            result = dpll(new_formula)
            if result is not None:
                return result
            del assignment[literal]
            
            new_formula = formula.replace(literal, str(not value)).replace(f'-{literal}', str(value))
            result = dpll(new_formula)
            if result is not None:
                return result
            del assignment[literal]
        
        return backtrack()
    
    def minimal_tropical_symmetry_length(formula):
        # Simplified tropical symmetry length calculation
        n = len(formula.split())
        return n
    
    instances_tested = 0
    msl_sum = 0
    l_sum = 0
    counterexample_found = False
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_random_boolean_formula(n)
        tseitin = tseitin_formula(formula)
        
        msl = minimal_tropical_symmetry_length(tseitin)
        l = dpll(formula)
        
        if l is None:
            continue
        
        instances_tested += 1
        msl_sum += msl
        l_sum += l
        
        if msl < l / 2:
            counterexample_found = True
    
    metric_value = msl_sum / instances_tested if instances_tested > 0 else 0
    conjecture_holds = not counterexample_found and metric_value >= 1.0
    n_max = max([5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "minimal_tropical_symmetry_length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "Counterexample found" if counterexample_found else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")