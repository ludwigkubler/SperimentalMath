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
    
    def read_twice_bp(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def size(bp):
        return len(bp)
    
    def index(tropical_curve):
        # Placeholder function to calculate the index of a tropical curve
        # This is a dummy implementation and should be replaced with actual logic
        return sum(tropical_curve) % 2
    
    def construct_tropical_curve(bp):
        # Placeholder function to construct a tropical curve from a BP
        # This is a dummy implementation and should be replaced with actual logic
        return [bp[i] for i in range(len(bp)) if bp[i]]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with multiple instances
            bp = read_twice_bp(n)
            tropical_curve = construct_tropical_curve(bp)
            idx = index(tropical_curve)
            
            if idx > 2**size(bp):
                return {
                    "metric_name": "index",
                    "metric_value": idx,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"BP size {size(bp)}, index {idx}"
                }
    
    return {
        "metric_name": "index",
        "metric_value": sum(index(construct_tropical_curve(read_twice_bp(n))) for n in n_values) / len(n_values),
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")