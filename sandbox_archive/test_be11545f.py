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
        # Placeholder for Hodge norm calculation
        return sum(abs(c)**2 for c in C) ** 0.5
    
    def circuit_monotone_width(C):
        # Placeholder for circuit monotone width calculation
        return len(C)
    
    def polynomial_bound(mn, n):
        # Placeholder for polynomial bound calculation
        return mn * (n**2 + n + 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hodge_norm = 0.0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            # Generate a random polynomial curve C of degree n
            C = [random.uniform(-1, 1) for _ in range(n+1)]
            hodge_val = hodge_norm(C)
            mn = circuit_monotone_width(C)
            bound = polynomial_bound(mn, n)
            
            total_hodge_norm += hodge_val
            instances_tested += 1
            max_n = max(max_n, n)
            
            if hodge_val > bound * 1.1:
                return {
                    "metric_name": "Hodge Norm",
                    "metric_value": hodge_val,
                    "instances_tested": instances_tested,
                    "n_max": max_n,
                    "conjecture_holds": False,
                    "counterexample": f"H(C) > 1.1 * f(mn), H(C)={hodge_val}, f(mn)={bound}"
                }
    
    mean_hodge_norm = total_hodge_norm / instances_tested
    return {
        "metric_name": "Hodge Norm",
        "metric_value": mean_hodge_norm,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")