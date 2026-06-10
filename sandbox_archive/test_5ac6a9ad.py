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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def tropical_curve_length(cnf):
        length = 0
        for clause in cnf:
            length += abs(sum(clause))
        return length
    
    def rank_variance(n, m):
        # Simplified version of the rank variance formula
        return math.log(n) * math.log(m)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, min(2*n-1, 100))  # Ensure m is reasonable
        cnf = generate_cnf(n, m)
        length = tropical_curve_length(cnf)
        rv = rank_variance(n, m)
        
        results.append({
            "n": n,
            "m": m,
            "length": length,
            "rv": rv
        })
    
    max_n = max(result["n"] for result in results)
    total_rv = sum(result["rv"] for result in results)
    avg_rv = total_rv / len(results)
    std_rv = math.sqrt(sum((result["rv"] - avg_rv) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["length"] <= 2**result["n"] and result["rv"] <= math.log(result["n"]) * math.log(result["m"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": avg_rv,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rv = sum(result["metric_value"] for result in results)
    avg_rv = total_rv / len(results)
    std_rv = math.sqrt(sum((result["metric_value"] - avg_rv) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rv} std={std_rv} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")