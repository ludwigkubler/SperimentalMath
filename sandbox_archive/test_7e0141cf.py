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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(phi):
        n = len(phi)
        max_width = 0
        for i in range(1 << n):
            width = 0
            for j in range(n):
                if (i >> j) & 1:
                    width += 1
                    if not all(phi[i ^ (1 << k)] <= phi[i] for k in range(j)):
                        break
            max_width = max(max_width, width)
        return max_width
    
    def local_induction_dimension(n):
        # Placeholder implementation. This is a dummy function.
        # Replace with actual computation of lnd if available.
        return n  # Example: lnd is linearly correlated with n for simplicity
    
    metric_name = "correlation_coefficient"
    instances_tested = 0
    total_lnd = 0
    total_width = 0
    n_max = 1
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        phi = generate_random_boolean_function(n)
        lnd_phi = local_induction_dimension(n)
        width_phi = monotone_width(phi)
        
        total_lnd += lnd_phi
        total_width += width_phi
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    avg_lnd = total_lnd / instances_tested
    avg_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * avg_lnd * avg_width - 
                               sum(lnd_phi * width_phi for lnd_phi, width_phi in zip(phi, phi))) / \
                              math.sqrt((instances_tested * sum(lnd_phi**2 for lnd_phi in phi) - 
                                          sum(lnd_phi**2 for lnd_phi in phi)) *
                                        (instances_tested * sum(width_phi**2 for width_phi in phi) - 
                                         sum(width_phi**2 for width_phi in phi)))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")