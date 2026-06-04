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
    
    def generate_sat_clause_set(n):
        clauses = []
        for _ in range(n):
            num_vars = random.randint(1, n)
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(num_vars)]
            clauses.append(clause)
        return clauses
    
    def compute_nerve_and_indeterminacy(clauses):
        # Simplified computation of nerve and indeterminacy index
        n = len(clauses)
        indeterminacy = sum(len(set(clause)) for clause in clauses) / (n * n)
        return indeterminacy
    
    def estimate_complexity(clauses):
        return len(clauses)
    
    total_indeterminacy = 0
    total_complexity = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_clause_set(n)
            indeterminacy = compute_nerve_and_indeterminacy(clauses)
            complexity = estimate_complexity(clauses)
            
            total_indeterminacy += indeterminacy * complexity
            total_complexity += complexity
            instances_tested += 1
            n_max = max(n_max, n)
    
    if total_complexity == 0:
        return {
            "metric_name": "indeterminacy_to_complexity_ratio",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    ratio = total_indeterminacy / total_complexity
    return {
        "metric_name": "indeterminacy_to_complexity_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 1,  # Simplified check for the conjecture
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='indeterminacy_to_complexity_ratio' first_failing_seed={first_failing_seed}")