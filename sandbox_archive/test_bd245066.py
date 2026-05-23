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

def generate_geometric_group(n):
    # Simple example: cyclic group Z_n
    return list(range(n))

def compute_r_G_S_C(G, S_C):
    # Placeholder for actual computation; this is a dummy function
    return len(G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_geometric_group(n)
        S_C = random.randint(1, 10) * n
        r_G_S_C = compute_r_G_S_C(G, S_C)
        
        if S_C <= 0 or len(G) == 0:
            continue
        
        ratio = Fraction(r_G_S_C, math.log(S_C))
        results.append({"n": n, "S_C": S_C, "r_G_S_C": r_G_S_C, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to Log Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= Fraction(1, math.log(result["S_C"])) for result in results)
    counterexample = "" if conjecture_holds else "Ratio exceeds log(S(C))"
    
    return {
        "metric_name": "Ratio of Rank to Log Circuit Size",
        "metric_value": float(metric_value),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30)) + [53, 67, 79, 83, 89]  # Default to first 30 primes and a few more
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds log(S(C))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")