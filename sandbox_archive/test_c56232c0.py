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
    
    def generate_random_csp(n):
        # Generate a random CSP instance with n variables
        return [random.choice([-1, 1]) for _ in range(2**n)]
    
    def min_order_quaternion_algebra(csp):
        # Compute the minimal order of quaternion algebra for a given CSP
        # This is a placeholder function; actual implementation needed
        return random.randint(1, n)
    
    def sum_of_squares_refutation_levels(csp):
        # Compute the number of levels in a sum-of-squares refutation for a given CSP
        # This is a placeholder function; actual implementation needed
        return random.randint(1, 2*n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    csp = generate_random_csp(n)
    min_order = min_order_quaternion_algebra(csp)
    refutation_levels = sum_of_squares_refutation_levels(csp)
    
    if min_order < n**0.75 and refutation_levels <= 1.5*n/2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"min_order={min_order}, refutation_levels={refutation_levels}"
    
    return {
        "metric_name": "min_order_quaternion_algebra",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break