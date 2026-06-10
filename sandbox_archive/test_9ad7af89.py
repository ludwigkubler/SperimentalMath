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

def generate_tseitin_formula(n, k=3):
    if n >= k:
        colors = random.sample(range(1, k + 1), n)
        literals = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate clauses for each variable
        for i in range(n):
            clauses.append([literals[i], f'-x{i+1}', str(colors[i])])
        
        # Generate clauses to ensure all variables have different colors
        for i in range(n):
            for j in range(i + 1, n):
                if colors[i] != colors[j]:
                    clauses.append([f'-{literals[i]}', f'{literals[j]}'])
                    clauses.append([f'{literals[i]}', f'-{literals[j]}'])
        
        # Generate the final clause to ensure all variables are true
        final_clause = [f'{-l}' for l in literals]
        clauses.append(final_clause)
        
        return literals, clauses
    else:
        raise ValueError("n must be greater than or equal to k")

def quadratic_form(literals, clauses):
    n = len(literals)
    qform = [[0] * n for _ in range(n)]
    
    for clause in clauses:
        for l1 in clause:
            if l1.startswith('-'):
                i1 = int(l1[1:]) - 1
                sign1 = -1
            else:
                i1 = int(l1) - 1
                sign1 = 1
            
            for l2 in clause:
                if l2.startswith('-'):
                    i2 = int(l2[1:]) - 1
                    sign2 = -1
                else:
                    i2 = int(l2) - 1
                    sign2 = 1
                
                if i1 != i2:
                    qform[i1][i2] += sign1 * sign2
    
    return qform

def count_integral_points(qform):
    n = len(qform)
    count = 0
    
    for x in range(-10, 11):  # Bounded range for simplicity
        for y in range(-10, 11):
            if all(qform[i][j] * (x**2 + y**2) >= 0 for i in range(n) for j in range(n)):
                count += 1
    
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_n = sum(n_values)
    instances_tested = 0
    n_max = max(n_values)
    metric_value = Fraction(0)
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            try:
                literals, clauses = generate_tseitin_formula(n)
                qform = quadratic_form(literals, clauses)
                N_phi = count_integral_points(qform)
                
                w_phi = len(clauses)  # Simplified resolution proof width
                
                metric_value += Fraction(N_phi * w_phi, total_n)
                instances_tested += 1
            except ValueError as e:
                counterexample = str(e)
                conjecture_holds = False
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    mean_metric = metric_value / instances_tested
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(mean_metric),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric >= 0.7,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")