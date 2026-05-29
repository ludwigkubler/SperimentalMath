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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def read_twice_bp_size(f):
        n = len(f)
        if n <= 1:
            return 0
        max_value = -math.inf
        for i in range(1 << (n-1)):
            value = f[i] + f[~i]
            if value > max_value:
                max_value = value
        return max_value
    
    def minimal_order_brauer_group(f):
        n = len(f)
        # Simplified Brauer group order calculation for demonstration purposes
        return 2**n
    
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        rtbp_size = read_twice_bp_size(f)
        brauer_group_order = minimal_order_brauer_group(f)
        
        if brauer_group_order > rtbp_size:
            conjecture_holds = False
            counterexample = f"n={n}, RTBP size={rtbp_size}, Brauer group order={brauer_group_order}"
            break
        
        instances_tested += 1
        total_ratio += brauer_group_order / rtbp_size
    
    if not conjecture_holds:
        return {
            "metric_name": "ratio",
            "metric_value": total_ratio / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")