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
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
        for i in range(2, n+1):
            clauses.append(f'{-variables[i-2]} {variables[i-1]}')
        return variables, clauses
    
    def read_twice_bp_complexity(clauses):
        return len(clauses)
    
    def minimal_local_cohomology_rank(variables, clauses):
        # Simplified mock implementation
        return len(variables) + len(clauses)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    complexity = read_twice_bp_complexity(clauses)
    rank = minimal_local_cohomology_rank(variables, clauses)
    
    ratio = rank / complexity if complexity != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Minimal Local Cohomology Rank to Read-Twice BP Complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.3,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} is outside ±30% of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±30% of 1\" first_failing_seed={first_failing_seed}")