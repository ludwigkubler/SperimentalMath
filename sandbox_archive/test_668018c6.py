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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([variables[i], f'~{variables[i-1]}'])
        return clauses
    
    def resolution_width(clauses):
        # Simplified resolution width calculation
        return len(clauses)
    
    def coxeter_group_reflections(n):
        # Simplified reflection count for a Tseitin formula
        return n * (n - 1) // 2
    
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        n = random.randint(5, 40)
        clauses = tseitin_formula(n)
        w = resolution_width(clauses)
        r = coxeter_group_reflections(n)
        results.append((n, r, w))
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n for _, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    ratios = [w / (r ** 2) for _, r, w in results]
    avg_ratio = sum(ratios) / len(ratios)
    std_dev = math.sqrt(sum((x - avg_ratio) ** 2 for x in ratios) / len(ratios))
    
    conjecture_holds = all(0.9 <= x / (r ** 2) <= 1.1 for _, r, w in results)
    counterexample = "" if conjecture_holds else "out_of_bounds"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not results:
            results.append(trial_result)
        else:
            results.append({
                "metric_name": "resolution_proof_width",
                "metric_value": (results[-1]["metric_value"] * results[-1]["instances_tested"] + trial_result["metric_value"] * trial_result["instances_tested"]) / (results[-1]["instances_tested"] + trial_result["instances_tested"]),
                "instances_tested": results[-1]["instances_tested"] + trial_result["instances_tested"],
                "n_max": max(results[-1]["n_max"], trial_result["n_max"]),
                "conjecture_holds": results[-1]["conjecture_holds"] and trial_result["conjecture_holds"],
                "counterexample": "" if results[-1]["conjecture_holds"] and trial_result["conjecture_holds"] else "out_of_bounds"
            })
    
    mean_value = results[-1]["metric_value"]
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for _, x, _ in results) / len(results))
    support_fraction = sum(1 for _, _, conjecture_holds in results if conjecture_holds) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not conjecture_holds for _, _, conjecture_holds in results):
        first_failing_seed = next(seed for seed, _, conjecture_holds in results if not conjecture_holds)
        print(f"RESULT: FALSIFIED counterexample=\"out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")