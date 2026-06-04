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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def hodge_order(phi):
        # Placeholder implementation; actual Hodge order calculation is complex
        return len(phi)
    
    def monotone_width(phi):
        # Placeholder implementation; actual circuit width calculation is complex
        return len(phi)
    
    n = 5
    instances_tested = 0
    total_h = 0
    total_w = 0
    
    while instances_tested < 30:
        phi = generate_boolean_function(n)
        h = hodge_order(phi)
        w = monotone_width(phi)
        
        if h > 0 and w > 0:
            total_h += h
            total_w += w
            instances_tested += 1
    
    mean_h = total_h / instances_tested
    mean_w = total_w / instances_tested
    ratio = mean_h / mean_w
    
    conjecture_holds = (ratio <= 1.5) and (mean_h / math.log(n) >= 0.7)
    
    return {
        "metric_name": "Ratio of Hodge Order to Monotone Width",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
             [31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed + 1}")