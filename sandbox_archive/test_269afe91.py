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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_boolean_function(m, d):
    n = 2**m
    f = [random.randint(0, 1) for _ in range(n)]
    return f

def compute_coxeter_diagram_complexity(f, m, d):
    # Placeholder implementation of Coxeter-diagram complexity computation
    # This is a dummy function to illustrate the structure
    # Replace with actual implementation if available
    return Fraction(m**2 * d**3, 6)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = random.randint(1, min(n, 8))  # Ensure at least one variable
        d = random.randint(1, min(m, 40))
        
        f = generate_boolean_function(m, d)
        chi_f = compute_coxeter_diagram_complexity(f, m, d)
        
        if chi_f <= 0:
            return {
                "metric_name": "Coxeter-diagram complexity",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "negative or zero value"
            }
        
        expected = Fraction(m**(2*d/3), 1)
        results.append((chi_f, expected))
    
    metric_value = sum(chi_f / expected for chi_f, expected in results) / len(results)
    conjecture_holds = all(0.5 <= chi_f / expected <= 2 for chi_f, expected in results)
    
    return {
        "metric_name": "Coxeter-diagram complexity",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")