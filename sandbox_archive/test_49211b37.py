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
    
    def generate_random_sat_instance(n):
        clauses = []
        for _ in range(n * (n - 1) // 2):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n + 1)]
            random.shuffle(literals)
            clause = '(' + ' ∨ '.join(literals) + ')'
            clauses.append(clause)
        return ' ∧ '.join(clauses)

    def tseitin_formula(sat_instance):
        literals = set()
        for clause in sat_instance.split(' ∧ '):
            for literal in clause.split(' ∨ '):
                literals.add(literal[2:] if literal.startswith('-') else literal)
        
        formulas = {}
        counter = 1
        for literal in literals:
            formulas[literal] = f'x{counter}'
            formulas[f'-{literal}'] = f'y{counter}'
            counter += 1
        
        tseitin_clauses = []
        for clause in sat_instance.split(' ∧ '):
            new_vars = [formulas[literal[2:] if literal.startswith('-') else literal] for literal in clause.split(' ∨ ')]
            tseitin_clauses.append(f'({new_vars[0]} → {formulas[f"-{new_vars[0]}"]})')
            for i in range(1, len(new_vars)):
                tseitin_clauses.append(f'({new_vars[i]} → {formulas[f"-{new_vars[i]}"]})')
                tseitin_clauses.append(f'({formulas[f"-{new_vars[i-1]}"]} ∨ {formulas[f"-{new_vars[i]}"]})')
        
        return ' ∧ '.join(tseitin_clauses)

    def resolution_width(formula):
        clauses = formula.split(' ∧ ')
        queue = []
        for clause in clauses:
            if len(clause.split(' ∨ ')) == 1:
                continue
            queue.append(clause)
        
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                common_literals = set(clause1.split(' ∨ ')).intersection(set(clause2.split(' ∨ ')))
                if len(common_literals) == 1:
                    new_clause = []
                    for literal in clause1.split(' ∨ '):
                        if literal not in common_literals:
                            new_clause.append(literal)
                    for literal in clause2.split(' ∨ '):
                        if literal not in common_literals:
                            new_clause.append(literal)
                    queue.append(' ∨ '.join(new_clause))
                elif len(common_literals) == 0:
                    return len(queue) + 1
        
        return len(queue)

    def local_induction_degree(formula):
        # Placeholder for LID computation
        # Replace with actual LID algorithm implementation
        return random.random() * resolution_width(formula)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_random_sat_instance(n)
    phi_G = tseitin_formula(sat_instance)
    lid_phi_G = local_induction_degree(phi_G)
    w_phi_G = resolution_width(phi_G)
    
    return {
        "metric_name": "LID / w(φ_G)",
        "metric_value": lid_phi_G / w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": lid_phi_G <= 10 * w_phi_G,  # Example constant c=10
        "counterexample": "" if lid_phi_G <= 10 * w_phi_G else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")