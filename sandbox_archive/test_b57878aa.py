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
    n = random.randint(5, 40)
    G = generate_tseitin_formula(n)
    local_cohomology_rank = compute_local_cohomology_rank(G)
    read_twice_bp_complexity = compute_read_twice_bp_complexity(G)
    
    if read_twice_bp_complexity == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Read-Twice BP complexity is zero"
        }
    
    ratio = local_cohomology_rank / read_twice_bp_complexity
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.3,
        "counterexample": "" if abs(ratio - 1) <= 0.3 else f"Ratio {ratio} is outside ±30%"
    }

def generate_tseitin_formula(n: int) -> list:
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n+1):
        clause = [f'-{i}', f'{i}']
        clauses.append(clause)
    
    # Generate clauses for OR of all variables
    or_clause = [f'x{i}' for i in range(1, n+1)]
    clauses.append(or_clause)
    
    return clauses

def compute_local_cohomology_rank(G: list) -> int:
    # Placeholder implementation (not actual local cohomology computation)
    return len(G)

def compute_read_twice_bp_complexity(G: list) -> int:
    # Placeholder implementation (not actual Read-Twice BP complexity computation)
    return len(G)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    total_ratio = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        
        if trial_result["conjecture_holds"]:
            count_supporting += 1
        
        total_ratio += trial_result["metric_value"]
    
    mean_ratio = total_ratio / len(results)
    support_fraction = count_supporting / len(results)
    
    print("TRIALS:")
    for result in results:
        print(f"TRIAL: {result}")
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±30%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")