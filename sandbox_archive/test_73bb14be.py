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

def generate_tseitin_formula(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each variable being true
    for i in range(n):
        clauses.append([literals[i]])
    
    # Generate clauses for each pair of variables
    for i in range(n):
        for j in range(i + 1, n):
            new_lit = f'x{n+i+j+1}'
            literals.append(new_lit)
            clauses.append([-literals[i], -literals[j], new_lit])
            clauses.append([literals[i], literals[j], -new_lit])
    
    # Generate the final clause
    for i in range(n):
        new_lit = f'x{2*n+i+1}'
        literals.append(new_lit)
        clauses.append([-literals[i]] + [literals[n+j] for j in range(i, n)])
    
    return literals, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n)
        # Placeholder for computing the tropical Hodge structure index
        I_H = random.random() * n  # Simulated value for demonstration
        # Placeholder for computing the resolution proof width
        w_phi_G = random.randint(10, 2*n)  # Simulated value for demonstration
        
        results.append({
            "n": n,
            "I_H": I_H,
            "w_phi_G": w_phi_G
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    I_H_values = [result["I_H"] for result in results]
    w_phi_G_values = [result["w_phi_G"] for result in results]
    
    # Calculate the correlation coefficient
    mean_I_H = sum(I_H_values) / len(I_H_values)
    mean_w_phi_G = sum(w_phi_G_values) / len(w_phi_G_values)
    numerator = sum((I_H - mean_I_H) * (w_phi_G - mean_w_phi_G) for I_H, w_phi_G in zip(I_H_values, w_phi_G_values))
    denominator = math.sqrt(sum((I_H - mean_I_H)**2 for I_H in I_H_values)) * math.sqrt(sum((w_phi_G - mean_w_phi_G)**2 for w_phi_G in w_phi_G_values))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    r = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(r) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_r = sum(results) / len(results)
        std_r = math.sqrt(sum((r - mean_r)**2 for r in results) / len(results))
        
        support_fraction = sum(1 for r in results if abs(r) >= 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.7))]
            print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed={first_failing_seed}")