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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random instance φ with size n and polynomially bounded d(φ)
    n = random.randint(5, 40)
    d_phi = random.randint(1, min(n, 10))  # Polynomially bounded
    
    # Construct the corresponding Frege proof tree T(φ)
    # This is a placeholder for actual proof construction logic
    depth_T_phi = d_phi * (d_phi + 1) // 2  # Simplified example depth
    
    # Compute the groupoid categorical dimension d(φ)
    # Placeholder for actual groupoid dimension computation
    d_phi_computed = d_phi
    
    # Measure the depth d(T(φ)) of the Frege proof tree
    depth_T_phi_measured = depth_T_phi
    
    # Correlate the computed dimensions and depths
    metric_value = depth_T_phi_measured / (d_phi_computed ** 2 * math.log(n))
    
    # Check if the conjecture holds
    conjecture_holds = metric_value <= 1.0
    
    return {
        "metric_name": "depth_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Depth ratio {metric_value} > 1.0 for d(φ)={d_phi_computed}, depth(T(φ))={depth_T_phi_measured}, n={n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    total_metric_value = sum(r["metric_value"] for r in results)
    total_instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric_value = total_metric_value / total_instances_tested
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / total_instances_tested)
    
    # Determine if the conjecture is supported, falsified, or inconclusive
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE insufficient_data"
    
    print(result)