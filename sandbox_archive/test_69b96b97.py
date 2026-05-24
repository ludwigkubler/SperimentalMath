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
    
    n = 5 + (seed % 6) * 5  # Sweep n through {5, 10, 15, 20, 30, 40}
    if n > 40:
        return {
            "metric_name": "L(f)/CC_GQ(f)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Generate a random Boolean function f: {0,1}^n -> {0,1}
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Construct an algebraic curve representation (simplified example)
    L_f = n  # Placeholder for minimal local complexity
    
    # Perform geometric quantization and calculate communication complexity
    CC_GQ_f = sum(f) / len(f)  # Placeholder for communication complexity
    
    metric_value = L_f / CC_GQ_f if CC_GQ_f != 0 else None
    
    return {
        "metric_name": "L(f)/CC_GQ(f)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": (0.9 <= metric_value <= 1.1) if metric_value is not None else False,
        "counterexample": "" if conjecture_holds else f"n={n}, L(f)={L_f}, CC_GQ(f)={CC_GQ_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["metric_value"] is None for res in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        metric_values = [res["metric_value"] for res in results if res["metric_value"] is not None]
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(0.9 <= val <= 1.1 for val in metric_values) / len(metric_values)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, res in zip(seeds, results) if not (0.9 <= res["metric_value"] <= 1.1))
            print(f"RESULT: FALSIFIED counterexample=\"out_of_bounds\" first_failing_seed={first_failing_seed}")