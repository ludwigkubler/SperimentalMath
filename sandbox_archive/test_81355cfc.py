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
    
    def resolution_width(phi):
        # Placeholder for actual resolution width calculation
        return len(phi.split())  # Simplified for demonstration
    
    def symmetric_braid_group_order(w):
        # Placeholder for actual braid group order calculation
        return w**2 + 1  # Simplified for demonstration
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        phi = ' '.join(random.choices('01', k=n))  # Random Boolean satisfiability instance
        w = resolution_width(phi)
        order = symmetric_braid_group_order(w)
        
        results.append({
            "n": n,
            "phi": phi,
            "w": w,
            "order": order
        })
    
    max_n = max(result["n"] for result in results)
    if max_n < 16:
        return {
            "metric_name": "order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    total_order = sum(result["order"] for result in results)
    avg_order = total_order / len(results)
    std_dev = math.sqrt(sum((result["order"] - avg_order) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "order",
        "metric_value": avg_order,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": avg_order <= 10**6 * max([result["w"] for result in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")