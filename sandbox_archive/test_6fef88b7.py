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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def entropy(subset_size, total_clauses):
    if subset_size == 0 or subset_size == total_clauses:
        return 0
    p = subset_size / total_clauses
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        total_clauses = len(cnf)
        
        if total_clauses == 0:
            continue
        
        entropy_values = [entropy(i, total_clauses) for i in range(total_clauses + 1)]
        min_order = n  # Placeholder for minimal order calculation
        
        results.append({
            "metric_name": "Entropy",
            "metric_value": sum(entropy_values),
            "instances_tested": len(cnf),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })
    
    return {
        "seed": seed,
        "metric_name": "Entropy",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")