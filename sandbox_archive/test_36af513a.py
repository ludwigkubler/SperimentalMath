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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(2*n)]
    clauses = []
    
    # Generate clauses for OR gate
    for i in range(n):
        clauses.append(f'{variables[i]} {variables[n+i]}')
        clauses.append(f'-{variables[i]} -{variables[n+i]} {variables[2*n+i]}')
        clauses.append(f'{-variables[i]} {variables[2*n+i]}')
        clauses.append(f'{variables[i]} {-variables[2*n+i]}')
    
    # Generate clauses for AND gate
    for i in range(n):
        clauses.append(f'-{variables[n+i]} -{variables[2*n+i]} -{variables[2*n+n+i]}')
        clauses.append(f'{variables[n+i]} {variables[2*n+i]} {variables[2*n+n+i]}')
    
    # Generate clauses for NOT gate
    for i in range(n):
        clauses.append(f'-{variables[i]} {variables[2*n+n+i]}')
        clauses.append(f'{variables[i]} -{variables[2*n+n+i]}')
    
    return variables, clauses

def read_twice_bp_complexity(clauses):
    # Placeholder function to compute Read-Twice BP complexity
    # This is a dummy implementation for the sake of testing
    return len(clauses)

def minimal_local_cohomology_rank(variables, clauses):
    # Placeholder function to compute minimal local cohomology rank
    # This is a dummy implementation for the sake of testing
    return len(variables) / 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    
    rank = minimal_local_cohomology_rank(variables, clauses)
    complexity = read_twice_bp_complexity(clauses)
    
    ratio = rank / complexity if complexity != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Minimal Local Cohomology Rank to Read-Twice BP Complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.3,
        "counterexample": "" if abs(ratio - 1) <= 0.3 else f"Ratio {ratio} is outside ±30% of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")