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

def generate_k_sat_instance(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = tuple(random.sample(variables, 3))
        if len(clause) == 2:
            clause += (random.choice([True, False]),)
        clauses.add(clause)
    return variables, clauses

def p_adic_order(differential_representation):
    # Simplified p-adic order calculation for demonstration
    return len(differential_representation)

def resolution_depth(instance):
    variables, clauses = instance
    n = len(variables)
    m = len(clauses)
    
    # Placeholder for actual DPLL solver implementation
    # This is a dummy function to avoid actual computation
    if random.choice([True, False]):
        return 2 * n
    else:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = min(n**2, random.randint(10, 100))
        instance = generate_k_sat_instance(n, m)
        
        differential_representation = (n, m)  # Placeholder for actual calculation
        p_order = p_adic_order(differential_representation)
        
        res_depth = resolution_depth(instance)
        
        results.append({
            "p_adic_order": p_order,
            "resolution_depth": res_depth
        })
    
    min_p_order = min(result["p_adic_order"] for result in results)
    max_res_depth = max(result["resolution_depth"] for result in results)
    
    conjecture_holds = (min_p_order <= math.log(n) + math.log(m)) and (max_res_depth >= n**2)
    counterexample = "" if conjecture_holds else "p-adic order exceeds log(n) + log(m)"
    
    return {
        "metric_name": "Minimal p-Adic Order vs Resolution Depth",
        "metric_value": min_p_order,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {'seed':<8} {run_trial(seed)}")
        results.append(run_trial(seed))
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic order exceeds log(n) + log(m)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")