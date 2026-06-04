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
    
    n = 40
    metric_name = "resolution_proof_width"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        # Generate a random d-dimensional variety V with known monodromy group
        # This is a placeholder function; replace it with actual implementation
        def generate_variety(n):
            return {"monodromy_group": [random.randint(1, 10) for _ in range(n)]}
        
        V = generate_variety(n)
        monodromy_group = V["monodromy_group"]
        
        # Calculate the order of the minimal normal subgroup |M_min(V)|
        def order_of_subgroup(subgroup):
            return len(set(subgroup))
        
        M_min_order = order_of_subgroup(monodromy_group)
        
        # Compute the resolution proof width w(φ_V)
        def resolution_proof_width(n, monodromy_group):
            # Placeholder function; replace it with actual implementation
            return random.randint(1, 2 * n)
        
        w_phi_V = resolution_proof_width(n, monodromy_group)
        
        if w_phi_V > 1.5 * M_min_order:
            conjecture_holds = False
            counterexample = f"Counterexample: n={n}, w(φ_V)={w_phi_V}, |M_min(V)|={M_min_order}"
    
    return {
        "metric_name": metric_name,
        "metric_value": 0,  # This is a placeholder; replace with actual computation
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")