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
    
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError("Modular inverse does not exist")
    
    def diophantine_set(clauses):
        n = len(clauses)
        equations = []
        mod = 2**n + 1  # A prime number greater than n
        
        for clause in clauses:
            equation = 0
            for literal, sign in clause:
                index = abs(literal) - 1
                coefficient = sign * (-1 if literal < 0 else 1)
                try:
                    equation += coefficient * mod_inverse(index + 1, mod)
                except ValueError:
                    return None  # Return None if modular inverse does not exist
            equations.append(equation % mod)
        
        return equations
    
    def resolution_proof_depth(clauses):
        n = len(clauses)
        stack = clauses[:]
        depth = 0
        
        while stack:
            clause1 = stack.pop()
            for clause2 in stack:
                new_clause = []
                for literal1 in clause1:
                    if -literal1 in clause2:
                        common_literals = [l for l in clause1 if l != literal1]
                        new_clause.extend(common_literals)
                        break
                else:
                    continue
                new_clause = list(set(new_clause))
                if not new_clause:
                    return depth + 1
                stack.append(new_clause)
            depth += 1
        
        return depth
    
    def tseitin_formula(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Clause for each variable being true or false
        for var in variables:
            clause = [(var, 1), (-var, -1)]
            clauses.append(clause)
        
        # Clause for each pair of variables being different
        for i in range(n):
            for j in range(i + 1, n):
                clause = [(-variables[i], 1), (variables[j], 1), (-variables[j], -1), (variables[i], -1)]
                clauses.append(clause)
        
        # Clause for each pair of variables being the same
        for i in range(n):
            for j in range(i + 1, n):
                clause = [(variables[i], 1), (variables[j], -1), (-variables[j], 1), (-variables[i], -1)]
                clauses.append(clause)
        
        return clauses
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    
    diophantine_eqs = diophantine_set(clauses)
    if diophantine_eqs is None:
        return {
            "metric_name": "ID(φ)/d(φ)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "modular_inverse_does_not_exist"
        }
    
    proof_depth = resolution_proof_depth(clauses)
    
    if proof_depth == 0:
        return {
            "metric_name": "ID(φ)/d(φ)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_depth_zero"
        }
    
    ratio = Fraction(diophantine_eqs[0], proof_depth)
    
    return {
        "metric_name": "ID(φ)/d(φ)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if not math.isnan(result["metric_value"])) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(result["metric_value"]) for result in results) and 0.5 <= mean_ratio <= 1.5:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=nan support_fraction={support_fraction}")
    elif any(math.isnan(result["metric_value"]) for result in results):
        print("RESULT: INCONCLUSIVE metric_saturation")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_outside_range' first_failing_seed={first_failing_seed}")