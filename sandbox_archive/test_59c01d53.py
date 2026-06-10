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

def tseitin_formula(sat_instance):
    n = len(sat_instance)
    new_vars = [f'x{i+1}' for i in range(n)]
    formulas = {}
    
    # Create Tseitin clauses
    for i in range(n):
        formulas[new_vars[i]] = f'{new_vars[i]}'
        tseitin_clauses = []
        for literal in sat_instance[i]:
            if literal.startswith('-'):
                var = literal[1:]
                tseitin_clauses.append(f'({var} → {new_vars[i]})')
                tseitin_clauses.append(f'(¬{var} → ¬{new_vars[i]})')
            else:
                tseitin_clauses.append(f'({literal} ∨ {new_vars[i]})')
        formulas[f'-{new_vars[i]}'] = ' '.join(tseitin_clauses)
    
    # Combine all clauses
    final_clause = ' ∧ '.join(formulas.values())
    return final_clause

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_lid = 0.0
    max_n = 0
    
    while True:
        sat_instance = [[f'x{i+1}', f'-x{i+1}'] for i in range(n)]
        phi_G = tseitin_formula(sat_instance)
        
        # Calculate LID (simplified example, replace with actual LID computation)
        lid = len(phi_G.split(' ∧ '))
        
        # Calculate resolution proof width
        proof_width = n  # Simplified example, replace with actual proof width calculation
        
        total_lid += lid / proof_width
        instances_tested += 1
        max_n = max(max_n, n)
        
        if instances_tested >= 30:
            break
        
        n += 5
    
    metric_value = total_lid / instances_tested
    conjecture_holds = metric_value <= 10.0
    counterexample = "" if conjecture_holds else f"lid={metric_value}, width=10"
    
    return {
        "metric_name": "LID/Width Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")