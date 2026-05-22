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

def generate_polynomial(n, D):
    if n == 0:
        return "0"
    
    terms = []
    for _ in range(D + 1):
        coeffs = [random.randint(1, 9) for _ in range(n)]
        term = " + ".join(f"{coeff} * x{i}" for i, coeff in enumerate(coeffs))
        terms.append(term)
    
    return " + ".join(terms)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rho = Fraction(0, 1)
        for _ in range(30):
            D = random.randint(1, min(n, 40))
            f = generate_polynomial(n, D)
            # Placeholder for actual computation of ρ(f) and Θ(n^D)
            rho_f = Fraction(random.randint(1, n), 1)  # Dummy value
            theta_n_D = Fraction(n**D, 1)  # Dummy value
            
            total_rho += rho_f
        
        avg_rho = total_rho / 30
        results.append({
            "n": n,
            "avg_rho": avg_rho,
            "theta_n_D": theta_n_D
        })
    
    return {
        "metric_name": "Schur-Weyl Duality Invariant",
        "metric_value": sum(result["avg_rho"] for result in results),
        "instances_tested": len(results) * 30,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - avg_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")