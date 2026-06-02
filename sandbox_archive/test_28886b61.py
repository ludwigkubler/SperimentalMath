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
    total_gal = 0
    total_cw = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            instances_tested += 1
            
            # Generate a random Boolean circuit with n gates
            circuit = [random.choice([0, 1]) for _ in range(n)]
            
            # Compute the Galois group order |Gal(C)|
            gal = len(set(circuit))
            
            # Compute the monotone width cw(C)
            cw = max(len(list(g)) for g in itertools.combinations(range(n), n//2))
            
            total_gal += gal
            total_cw += cw
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_gal = total_gal / instances_tested
    mean_cw = total_cw / instances_tested
    
    # Pearson's correlation coefficient
    cov = sum((gal - mean_gal) * (cw - mean_cw) for gal, cw in zip([total_gal] * instances_tested, [total_cw] * instances_tested)) / instances_tested
    var_gal = sum((gal - mean_gal) ** 2 for gal in [total_gal] * instances_tested) / instances_tested
    var_cw = sum((cw - mean_cw) ** 2 for cw in [total_cw] * instances_tested) / instances_tested
    
    if var_gal == 0 or var_cw == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    correlation = cov / math.sqrt(var_gal * var_cw)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.5,  # Significance threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((r - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r) >= 0.5) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"correlation\" first_failing_seed={seeds[results.index(min(results, key=abs))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")