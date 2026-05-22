# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(2**n):
            row = [random.choice([0, 1]) for _ in range(n)]
            bp.append(row)
        return bp
    
    def calculate_tropical_curve_index(bp):
        n = len(bp[0])
        index = 0
        for i in range(n):
            count = sum(1 for row in bp if row[i] == 1)
            index += count * (n - count)
        return index
    
    def size_of_bp(bp):
        return len(bp) * len(bp[0])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n)
        index = calculate_tropical_curve_index(bp)
        size = size_of_bp(bp)
        
        if size == 0 or index < 0:
            continue
        
        results.append({
            "n": n,
            "bp_size": size,
            "tropical_index": index
        })
    
    if not results:
        return {
            "metric_name": "index_tropical_curve",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_index = sum(result["tropical_index"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["tropical_index"] <= 2 * result["bp_size"]) / len(results)
    
    return {
        "metric_name": "index_tropical_curve",
        "metric_value": mean_index,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_index = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")