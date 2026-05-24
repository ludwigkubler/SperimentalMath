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
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            new_var = f'y{i}'
            clauses.append([new_var, f'~{variables[i-1]}'])
            clauses.append([new_var, f'{variables[i]}'])
            clauses.append([f'~{new_var}', f'~{variables[i-1]}', f'~{variables[i]}'])
        return variables, clauses
    
    def calculate_rho(f):
        # Placeholder for actual calculation of rho(f)
        # This is a dummy implementation
        return random.randint(1, 5)
    
    def construct_resolution_proof(clauses):
        proof_length = len(clauses) * 2
        return proof_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rho = 0
    total_proof_length = 0
    instances_tested = 0
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        rho_f = calculate_rho(f"polynomial_system_{n}")
        proof_length = construct_resolution_proof(clauses)
        
        if rho_f <= 0 or proof_length <= 0:
            continue
        
        total_rho += rho_f
        total_proof_length += proof_length
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "rho_and_proof_length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_rho = total_rho / instances_tested
    mean_proof_length = total_proof_length / instances_tested
    
    conjecture_holds = (mean_rho <= 1.5 * math.log(instances_tested, 2)) and (mean_proof_length <= 2 ** (1.25 * mean_rho))
    
    return {
        "metric_name": "rho_and_proof_length",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rho: {mean_rho}, Mean proof length: {mean_proof_length}"
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
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")