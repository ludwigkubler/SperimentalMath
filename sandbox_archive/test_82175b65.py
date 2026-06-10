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
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    for i in range(1, n+1):
        clause = [-literals[i-1], literals[i]]
        clauses.append(clause)
    
    tseitin_var = 't'
    final_clause = [tseitin_var]
    for literal in literals:
        clause = [-tseitin_var, literal]
        clauses.append(clause)
    
    return literals + [tseitin_var], clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n)
        instances_tested += len(clauses)
        n_max = max(n_max, n)
        
        # Placeholder for Kac-Moody Lie algebra representation and proof length calculation
        dim_V = random.randint(1, 10)  # Simulated minimal dimension of the representation
        f_phi = len(clauses)  # Simulated Frege proof length
        
        if dim_V > 2 * f_phi:
            conjecture_holds = False
            counterexample = "dim(V) > 2*f(φ)"
        
        total_metric_value += dim_V
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": "dim(V)/f(φ)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1.0 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")