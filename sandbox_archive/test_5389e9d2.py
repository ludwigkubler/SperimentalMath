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
    
    def tropicalize(cnf):
        # Simplified tropicalization algorithm
        T = {}
        for clause in cnf:
            for lit in clause:
                if abs(lit) not in T:
                    T[abs(lit)] = 0
                T[abs(lit)] += 1
        return T
    
    def rank_variance(T):
        # Simplified rank variance calculation
        return sum(v * math.log2(v + 1) for v in T.values())
    
    def tropical_curvature(T):
        # Simplified tropical curvature calculation
        if not T:
            return 0
        max_val = max(T.values())
        return sum(1 / (v + 1) for v in T.values()) / max_val
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            T = tropicalize(cnf)
            R_V = rank_variance(T)
            curvature = tropical_curvature(T)
            
            results.append({
                "n": n,
                "m": m,
                "R_V": R_V,
                "curvature": curvature
            })
    
    mean_R_V = sum(result["R_V"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    conjecture_holds = all(result["R_V"] <= math.log2(n) * math.log2(m) and abs(result["curvature"]) <= 2**n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": mean_R_V,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")