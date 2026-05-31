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
    
    def generate_formula(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def galois_group_size(clauses):
        # Simplified version of computing the Galois group size
        n = len(clauses[0])
        return 2 ** (n - len(set(len(c) for c in clauses)))
    
    def distinct_clauses(clauses):
        return len(set(tuple(sorted(c)) for c in clauses))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times
            formula = generate_formula(n)
            deg_G = galois_group_size(formula)
            num_clauses = distinct_clauses(formula)
            results.append({"n": n, "deg_G": deg_G, "num_clauses": num_clauses})
    
    if not results:
        return {
            "metric_name": "Galois Group Degree",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    total_deg_G = sum(result["deg_G"] for result in results)
    total_num_clauses = sum(result["num_clauses"] for result in results)
    mean_deg_G = total_deg_G / len(results)
    n_max = max(result["n"] for result in results)
    
    conjecture_holds = all(result["deg_G"] <= result["num_clauses"] ** 2 for result in results)
    counterexample = "" if conjecture_holds else "Counterexample found"
    
    return {
        "metric_name": "Galois Group Degree",
        "metric_value": mean_deg_G,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
    
    # Compute mean and std of metric_value
    metrics = [result["metric_value"] for result in seeds]
    mean_metric = sum(metrics) / len(metrics)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metrics) / len(metrics))
    
    support_fraction = sum(result["conjecture_holds"] for result in seeds) / len(seeds)
    
    if all(result["conjecture_holds"] for result in seeds):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in seeds):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")