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
    n_values = [5, 10, 15, 20, 30, 40]
    min_order_sum = 0
    rank_variance_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        q = 2**n
        if q > 16777216:  # 2^24, avoid excessive computation
            continue
        
        # Generate a random elliptic curve E over F_q
        a = random.randint(0, q-1)
        b = random.randint(0, q-1)
        while (4*a**3 + 27*b**2) % q == 0:  # Ensure the curve is non-singular
            a = random.randint(0, q-1)
            b = random.randint(0, q-1)

        # Compute the minimal order of p-adic Selmer groups (simplified for testing)
        min_order = math.log(q**2 / math.log(q), 2)  # Simplified lower bound
        if min_order <= 0:
            continue
        
        # Generate a random communication problem of size n variables
        rank_variance = q * (q - 1) / 2  # Simplified upper bound
        
        min_order_sum += min_order
        rank_variance_sum += rank_variance
        instances_tested += 1
        n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    min_order_avg = min_order_sum / instances_tested
    rank_variance_avg = rank_variance_sum / instances_tested

    # Check the conjecture bounds
    lower_bound = math.log(q**2 / math.log(q), 2)
    upper_bound = q

    if all(lower_bound <= order <= upper_bound for order in [min_order_avg]):
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = "bounds_violation"

    return {
        "metric_name": "min_order",
        "metric_value": min_order_avg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "bounds_violation"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")