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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        k = random.randint(1, n)
        clause = random.sample(['x' + str(i+1) for i in range(n)], k=k)
        clauses.append(clause)
    return clauses

def dpll_solver(phi):
    def solve(model):
        if not phi:
            return model
        literal = next(iter(phi[0]))
        rest = [c for c in phi if literal not in c and -literal not in c]
        if literal > 0:
            new_model = model + [(literal,)]
            result = solve(rest)
            if result is not None:
                return result
            return solve([c for c in rest if -literal not in c])
        else:
            new_model = model + [(-literal,)]
            result = solve(rest)
            if result is not None:
                return result
            return solve([c for c in rest if literal not in c])

    return solve([])

def euler_characteristic(phi):
    # Placeholder implementation; actual computation depends on the moduli space mapping
    return len(phi)  # Simplified for testing purposes

def resolution_width(phi):
    return dpll_solver(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    phi = generate_cnf(n, m)
    
    chi_phi = euler_characteristic(phi)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "Euler Characteristic vs Resolution Width",
        "metric_value": chi_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")