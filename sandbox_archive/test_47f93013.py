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

def tseitin_formula(n):
    if n <= 1:
        return []
    
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Base case: x1 ∨ ¬x2
    clauses.append([variables[0], -variables[1]])
    
    for i in range(2, n):
        new_var = f'x{i+1}'
        clauses.append([-variables[i-1], variables[i], -new_var])
        clauses.append([variables[i-1], -variables[i], new_var])
        clauses.append([-variables[i], -new_var])
        clauses.append([new_var])
    
    return clauses

def minimal_representation_rank(n):
    if n <= 1:
        return 0
    
    # Simplified rank calculation for demonstration
    return n - 1

def circuit_monotone_width(clauses):
    # Placeholder function to simulate monotone width calculation
    # In practice, this would involve a DPLL solver or other method
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Pearson correlation coefficient"
    instances_tested = 0
    n_max = 0
    r_values = []
    w_m_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        clauses = tseitin_formula(n)
        
        if not clauses:
            continue
        
        rank = minimal_representation_rank(n)
        w_m = circuit_monotone_width(clauses)
        
        r_values.append(rank)
        w_m_values.append(w_m)
    
    if len(r_values) < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_r = sum(r_values) / len(r_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    correlation_coefficient = (sum((r - mean_r) * (w_m - mean_w_m) for r, w_m in zip(r_values, w_m_values)) /
                               math.sqrt(sum((r - mean_r)**2 for r in r_values) *
                                         sum((w_m - mean_w_m)**2 for w_m in w_m_values)))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
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
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_threshold\" first_failing_seed={first_failing_seed}")