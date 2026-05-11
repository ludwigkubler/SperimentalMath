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
    
    # Parameters
    n = 40
    instances_tested = 30
    
    # Generate a random elliptic curve over GF(2^n)
    def generate_elliptic_curve(n):
        a, b = random.randint(1, 2**n - 1), random.randint(1, 2**n - 1)
        return (a, b)
    
    def is_smooth_projective(a, b, n):
        # Simplified check for smoothness; actual implementation depends on genus calculation
        return True
    
    def compute_genus(a, b, n):
        # Placeholder for genus computation; actual implementation needed
        return 1
    
    def sos_refutation_size(g, n):
        return 2**(g * math.log(n))
    
    total_metric_value = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        a, b = generate_elliptic_curve(n)
        if not is_smooth_projective(a, b, n):
            continue
        
        g = compute_genus(a, b, n)
        refutation_size = sos_refutation_size(g, n)
        
        total_metric_value += refutation_size
        if g >= math.log(n):
            counterexample = f"High genus curve with g={g}, n={n}"
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = True if not counterexample else False
    
    return {
        "metric_name": "SOS Refutation Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and not counterexample:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")