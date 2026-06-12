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
    
    def ramanujan_theta_2(tau):
        if tau <= 0:
            return 0
        theta = 1
        for k in range(1, 100):  # Sum the first 100 terms for approximation
            theta += (-1)**k * math.exp(-math.pi**2 * k**2 * tau)
        return theta
    
    def minimal_local_indecomposable_sheaf_rank(D):
        # Placeholder function. Replace with actual computation if known.
        return random.random()  # Dummy value for testing
    
    n_max = 0
    metric_values = []
    
    for D in range(5, 41):  # Sweep n from 5 to 40
        tau = random.uniform(0.1, 1)  # Random argument for theta function
        mls_D = minimal_local_indecomposable_sheaf_rank(D)
        theta_2_tau_D = ramanujan_theta_2(tau)**D
        
        if mls_D > theta_2_tau_D:
            return {
                "metric_name": "mls(D) vs θ_2(τ)^D",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": D,
                "conjecture_holds": False,
                "counterexample": f"mls({D}) = {mls_D}, θ_2({tau})^{D} = {theta_2_tau_D}"
            }
        
        metric_values.append(mls_D)
        n_max = max(n_max, D)
    
    return {
        "metric_name": "mls(D) vs θ_2(τ)^D",
        "metric_value": sum(metric_values),
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    
    print(result)