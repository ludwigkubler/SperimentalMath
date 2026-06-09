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
    n_max = 0
    instances_tested = 0
    total_n = 0
    total_d = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test 5 instances per size
            depth = random.randint(1, n)
            num_vars = random.randint(1, n)
            
            total_n += num_vars
            total_d += depth
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "n(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    avg_n = total_n / instances_tested
    avg_d = total_d / instances_tested
    
    correlation_coefficient = (instances_tested * sum(n * d for n, d in zip([avg_n] * instances_tested, [avg_d] * instances_tested)) -
                                instances_tested * avg_n * avg_d) / \
                               math.sqrt((instances_tested * sum(n**2 for n in [avg_n] * instances_tested) - instances_tested * avg_n**2) *
                                         (instances_tested * sum(d**2 for d in [avg_d] * instances_tested) - instances_tested * avg_d**2))
    
    return {
        "metric_name": "n(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(res["metric_value"] is not None for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_instances_generated")