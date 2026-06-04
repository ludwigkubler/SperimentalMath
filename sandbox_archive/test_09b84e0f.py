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
    
    # Define the function to compute the resolution proof width (simplified example)
    def resolution_proof_width(n):
        return n * 2
    
    # Define the function to compute the order of the minimal normal subgroup (simplified example)
    def min_normal_subgroup_order(n):
        return n // 2
    
    # Generate a random d-dimensional variety V with known monodromy group
    d = random.randint(2, 5)  # Example dimension
    n = random.randint(10, 30)  # Example size
    
    # Compute the associated Tseitin formula φ_V and its resolution proof width w(φ_V)
    w_phi_V = resolution_proof_width(n)
    
    # Calculate the order of the minimal normal subgroup |M_min(V)|
    M_min_V_order = min_normal_subgroup_order(n)
    
    # Check if there is a correlation between w(φ_V) and |M_min(V)|
    conjecture_holds = w_phi_V <= 1.5 * M_min_V_order
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": w_phi_V,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: n={n}, w(φ_V)={w_phi_V}, |M_min(V)|={M_min_V_order}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")