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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clause = [var]
            for other_var in variables:
                if other_var != var:
                    clause.append(f'-{other_var}')
            clauses.append(clause)
        
        # Generate clauses for the negation of each variable
        for var in variables:
            clause = [f'-{var}']
            for other_var in variables:
                if other_var != var:
                    clause.append(other_var)
            clauses.append(clause)
        
        # Generate a final clause that is the conjunction of all variables
        final_clause = []
        for var in variables:
            final_clause.append(var)
        clauses.append(final_clause)
        
        return clauses
    
    def diophantine_set(clauses):
        n = len(clauses[0])
        equations = [0] * (n + 1)
        
        for clause in clauses:
            coefficient = random.choice([-1, 1])
            mod = 2**random.randint(3, 8)  # Random modulus between 8 and 512
            equation = 0
            
            for var in clause:
                if var.startswith('x'):
                    index = int(var[1:]) - 1
                    equation += coefficient * mod_inverse(index + 1, mod)
                elif var.startswith('-x'):
                    index = int(var[2:]) - 1
                    equation -= coefficient * mod_inverse(index + 1, mod)
            
            equations.append(equation % mod)
        
        return equations
    
    def mod_inverse(a, m):
        if a == 0:
            raise ValueError("Inverse doesn't exist")
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            # q is quotient
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        # Make x1 positive
        if x1 < 0:
            x1 += m0
        return x1
    
    def resolution_proof_depth(clauses):
        n = len(clauses)
        stack = []
        
        for clause in clauses:
            stack.append(clause)
        
        while stack:
            clause1 = stack.pop()
            clause2 = next((c for c in stack if any(var.startswith(f'-{v}') for v in clause1)), None)
            if not clause2:
                return 0
            
            new_clause = []
            for var in clause1:
                if not any(var.startswith(f'-{v}') for v in clause2):
                    new_clause.append(var)
            for var in clause2:
                if not any(var.startswith(f'-{v}') for v in clause1):
                    new_clause.append(f'-{var}')
            
            stack.append(new_clause)
        
        return len(stack)

    n = random.randint(5, 40)
    clauses = generate_tseitin_formula(n)
    equations = diophantine_set(clauses)
    depth = resolution_proof_depth(clauses)
    
    if depth == 0:
        return {
            "metric_name": "ID(φ)/d(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_depth_zero"
        }
    
    ratio = Fraction(equations[-1], depth)
    return {
        "metric_name": "ID(φ)/d(φ)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if 0.5 <= ratio <= 1.5 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "ID(φ)/d(φ) ratio outside [0.5, 1.5]"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")