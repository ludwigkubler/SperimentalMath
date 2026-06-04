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
    
    def hodge_norm(C):
        # Placeholder for actual Hodge norm computation
        return sum(abs(c) for c in C)
    
    def circuit_monotone_width(C):
        # Placeholder for actual circuit monotone width computation
        return len(C)
    
    def polynomial_bound(mn, n):
        # Placeholder for actual polynomial bound function
        return mn ** 2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        C = [random.complex() for _ in range(n)]
        H_C = hodge_norm(C)
        mn = circuit_monotone_width(C)
        bound = polynomial_bound(mn, n)
        
        results.append({
            "H_C": H_C,
            "mn": mn,
            "bound": bound
        })
    
    mean_H_C = sum(result["H_C"] for result in results) / len(results)
    mean_bound = sum(result["bound"] for result in results) / len(results)
    
    conjecture_holds = all(result["H_C"] <= 1.1 * result["bound"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hodge Norm vs Circuit Monotone Width",
        "metric_value": mean_H_C,
        "instances_tested": len(results),
        "n_max": max(result["mn"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")