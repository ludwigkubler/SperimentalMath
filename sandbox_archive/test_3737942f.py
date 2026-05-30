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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate Tseitin encoding of an arbitrary formula
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]} ∨ ¬{variables[i-1]}')
        
        for _ in range(n):
            clause = random.choice(variables) + ' ∨ ' + random.choice(variables)
            clauses.append(clause)
        
        return clauses
    
    def minimal_order_of_quadratic_residues(clauses):
        residues = set()
        for clause in clauses:
            literals = clause.split(' ∨ ')
            for lit in literals:
                if lit.startswith('¬'):
                    lit = lit[1:]
                residues.add(int(lit))
        
        residues = sorted(residues)
        q = 1
        for i in range(1, len(residues)):
            if (residues[i] - residues[i-1]) ** 2 > q:
                q = (residues[i] - residues[i-1]) ** 2
        
        return math.isqrt(q)
    
    def resolution_width(clauses):
        width = 0
        for clause in clauses:
            literals = clause.split(' ∨ ')
            width = max(width, len(literals))
        
        return width
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(75):  # Aim for at least 30 instances per seed
            clauses = generate_tseitin_formula(n)
            q = minimal_order_of_quadratic_residues(clauses)
            w = resolution_width(clauses)
            
            if q == 0 or w == 0:
                continue
            
            results.append((q, w))
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    q_values = [q for q, w in results]
    w_values = [w for q, w in results]
    
    correlation_coefficient = sum((q - mean_q) * (w - mean_w) for q, w in results)
    correlation_coefficient /= math.sqrt(sum((q - mean_q) ** 2 for q, _ in results)) * math.sqrt(sum((w - mean_w) ** 2 for _, w in results))
    
    mean_q = sum(q_values) / len(q_values)
    mean_w = sum(w_values) / len(w_values)
    std_q = math.sqrt(sum((q - mean_q) ** 2 for q in q_values) / len(q_values))
    std_w = math.sqrt(sum((w - mean_w) ** 2 for w in w_values) / len(w_values))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in enumerate(results) if abs(r["metric_value"]) < 0.7)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7\" first_failing_seed={first_failing_seed}")