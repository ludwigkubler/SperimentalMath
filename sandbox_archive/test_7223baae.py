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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(phi):
        # Placeholder function to simulate resolution width calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    def minimal_tropical_index():
        # Placeholder function to simulate minimal tropical index calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_boolean_instance(n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            width = resolution_width(phi)
            index = minimal_tropical_index()
            
            if abs(index - width) > 0.5 * width:
                counterexample = f"n={n}, phi={phi}, width={width}, index={index}"
                break
        
        if counterexample:
            break
    
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    conjecture_holds = abs(metric_value - (1.5 * n_max)) <= 0.5 * (1.5 * n_max)
    
    return {
        "metric_name": "minimal_tropical_index",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")