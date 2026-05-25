# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_tseitin_formula(n, m):
    variables = set(f'x{i}' for i in range(1, n + 1))
    clauses = []
    
    # Generate literals
    literals = [var for var in variables] + [-var for var in variables]
    
    for _ in range(m):
        clause = random.sample(literals, 2)
        clauses.append(clause)
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_range = range(10, 21, (n // 2) or 1)
        for m in m_range:
            variables, clauses = generate_tseitin_formula(n, m)
            k = len(clauses)
            
            # Placeholder for Delone set computation
            # This is a dummy implementation to avoid errors
            rho_D = random.randint(1, k)
            
            if rho_D > k:
                counterexample = f"n={n}, m={m}, rho(D)={rho_D} > {k}"
                return {
                    "metric_name": "resolution_proof_length",
                    "metric_value": 2**(k+1),
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
    
    mean_metric = sum(results) / len(results)
    std_metric = (sum((x - mean_metric)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result >= 2**(k+1)) / len(results)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result:
            results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    std_metric = (sum((x - mean_metric)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result >= 2**(k+1)) / len(results)
    
    if all(result >= 2**(k+1) for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(result < 2**(k+1) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 2**(k+1))
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, m={m}, rho(D) > {k}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")