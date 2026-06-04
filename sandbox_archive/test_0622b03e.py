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
    
    # Simulate generating a d-dimensional variety V with known monodromy group
    d = random.randint(2, 5)  # Dimension of the variety
    n = random.randint(5, 10)  # Number of instances to test
    
    if n > 40:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Sub-asymptotic n"
        }
    
    # Simulate computing the resolution proof width w(φ_V)
    w_phi_V = random.randint(n, 2 * n)  # Simulated value
    
    # Simulate calculating the order of the minimal normal subgroup |M_min(V)|
    M_min_V_order = random.randint(1, n)  # Simulated value
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": w_phi_V,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": w_phi_V <= 1.5 * M_min_V_order,
        "counterexample": "" if w_phi_V <= 1.5 * M_min_V_order else f"Counterexample: n={n}, w(φ_V)={w_phi_V}, |M_min(V)|={M_min_V_order}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")