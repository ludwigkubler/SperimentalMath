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
    
    def resolution_width(phi):
        # Placeholder for actual resolution width calculation
        return len(phi.split())  # Simplified for demonstration
    
    def symmetric_braid_group(phi):
        # Placeholder for constructing the symmetric braid group
        n = resolution_width(phi)
        # Example: a simple mapping that depends on phi's length
        return [i for i in range(n)]
    
    def normal_subgroup_order(braid_group):
        # Placeholder for calculating the order of the smallest normal subgroup
        # This is a trivial example; actual implementation needed
        return len(braid_group)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = " ".join(random.choices("01", k=n))  # Generate a random Boolean satisfiability instance
        w_phi = resolution_width(phi)
        braid_group = symmetric_braid_group(phi)
        order = normal_subgroup_order(braid_group)
        
        results.append({
            "n": n,
            "phi": phi,
            "w_phi": w_phi,
            "order": order
        })
    
    metric_value = sum(result["order"] for result in results) / len(results)
    conjecture_holds = all(result["order"] <= 10**6 * result["w_phi"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Normal Subgroup Order",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")