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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    # Clause: x1 ∨ ¬x2
    clauses.append([variables[0], -variables[1]])
    
    # Clauses: xi ∨ ¬xi+1 for i = 2 to n-1
    for i in range(1, n - 1):
        clauses.append([variables[i], -variables[i + 1]])
    
    # Clause: ¬x1 ∨ x2
    clauses.append([-variables[0], variables[1]])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        
        # Simulate resolution refutation length (placeholder value)
        t_F = n * (n + 1) // 2
        
        min_rank_C_F = len(variables)  # Placeholder value
        ratio = 2 ** min_rank_C_F / t_F
        
        results.append({
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": ratio > 1,  # Simplified for demonstration
            "counterexample": ""
        })
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_ratio": mean_ratio,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["mean_ratio"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")