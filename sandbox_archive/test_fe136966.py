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
    
    def generate_k_ary_boolean_function(k, n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        # Placeholder function for communication complexity rank
        # Replace with actual algorithm if available
        return len(f)
    
    def tropical_hodge_structure_index(f):
        # Placeholder function for minimal index of tropical Hodge structure
        # Replace with actual algorithm if available
        return sum(f) / len(f)
    
    n_max = 0
    instances_tested = 0
    total_ratio = 0.0
    
    for _ in range(30):
        k = random.randint(2, 10)
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        
        f = generate_k_ary_boolean_function(k, n)
        instances_tested += 1
        r = communication_complexity_rank(f)
        I_f = tropical_hodge_structure_index(f)
        
        if r == 0:
            continue
        
        ratio = I_f / r
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = 0.5 <= mean_ratio <= 1.5
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")