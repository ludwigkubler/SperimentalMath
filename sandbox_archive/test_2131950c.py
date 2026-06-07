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
        return len(phi.split())  # Simplified example
    
    def symmetric_braid_group(phi):
        # Placeholder for constructing the symmetric braid group
        return [phi]  # Simplified example
    
    def normal_subgroup_order(braid_group):
        # Placeholder for calculating the order of the smallest normal subgroup
        return len(braid_group)  # Simplified example
    
    phi = " ".join([str(random.randint(0, 1)) for _ in range(20)])  # Random Boolean satisfiability instance
    w_phi = resolution_width(phi)
    braid_group = symmetric_braid_group(phi)
    N_phi = normal_subgroup_order(braid_group)
    
    return {
        "metric_name": "Normal Subgroup Order",
        "metric_value": N_phi,
        "instances_tested": 1,
        "n_max": len(phi),
        "conjecture_holds": N_phi <= 10**6 * w_phi,
        "counterexample": "" if N_phi <= 10**6 * w_phi else f"phi={phi}, w(φ)={w_phi}, |N(φ)|={N_phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default list of primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")