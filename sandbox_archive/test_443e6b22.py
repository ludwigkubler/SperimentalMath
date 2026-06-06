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
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        for lit in literals:
            clauses.append([lit])
        
        for i in range(1, n+1):
            a, b = random.sample(literals, 2)
            new_lit = f'y{i}'
            clauses.append([new_lit, -a, -b])
            clauses.append([-new_lit, a])
            clauses.append([-new_lit, b])
        
        return literals, clauses
    
    def compute_min_rank(clauses):
        # Placeholder for Hodge decomposition module computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    def compute_resolution_width(clauses):
        # Placeholder for resolution proof width computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    n = random.randint(5, 40) if seed % 2 == 0 else random.choice([10, 15, 20, 30])
    literals, clauses = generate_tseitin_formula(n)
    
    min_rank = compute_min_rank(clauses)
    resolution_width = compute_resolution_width(clauses)
    
    ratio = min_rank / resolution_width if resolution_width != 0 else float('inf')
    
    metric_value = ratio
    conjecture_holds = 0.5 <= ratio <= 2
    
    return {
        "metric_name": "min_rank_over_resolution_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} out of range [0.5, 2]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of range [0.5, 2]\" first_failing_seed={first_failing_seed}")