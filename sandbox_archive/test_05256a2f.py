# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_function_field(g):
        # Simplified generation for demonstration purposes
        return [random.randint(0, 1) for _ in range(2 * g)]
    
    def compute_minimal_rank(field):
        # Placeholder implementation
        return len(set(field))
    
    def generate_tseitin_formula(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def compute_resolution_depth(formula):
        # Placeholder implementation
        return len(formula)
    
    g_values = [0, 1, 2, 3]
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for g in g_values:
        field = generate_function_field(g)
        rank = compute_minimal_rank(field)
        if rank < 2**(g+1):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": len(g_values),
                "conjecture_holds": False,
                "counterexample": f"Function field with genus {g} has minimal rank {rank}, expected at least {2**(g+1)}"
            }
        
        for n in n_values:
            m = random.randint(1, 2*n)
            formula = generate_tseitin_formula(n, m)
            depth = compute_resolution_depth(formula)
            if depth > 2**n / 2**(g+1):
                return {
                    "metric_name": "resolution_depth",
                    "metric_value": depth,
                    "instances_tested": len(g_values) * len(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"Tseitin formula on {n} variables and {m} clauses has depth {depth}, expected at most {2**n / 2**(g+1)}"
                }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(g_values) * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r >= 2**(g+1) for g in [0, 1, 2, 3]) / len(results)
    
    if all(r >= 2**(g+1) for r, g in zip(results, [0, 1, 2, 3])):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 2**(g+1) for r, g in zip(results, [0, 1, 2, 3])):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 2**(g+1) for g in [0, 1, 2, 3])]
        print(f"RESULT: FALSIFIED counterexample='Function field with genus g has minimal rank less than 2^(g+1)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")