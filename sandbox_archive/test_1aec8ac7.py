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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        max_consecutive_ones = 0
        current_count = 0
        for bit in f:
            if bit == 1:
                current_count += 1
                max_consecutive_ones = max(max_consecutive_ones, current_count)
            else:
                current_count = 0
        return max_consecutive_ones
    
    def minimal_local_ring_norm(f):
        n = len(f)
        # Simplified approximation for demonstration purposes
        return Fraction(n**2, 4)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    max_n = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        norm = minimal_local_ring_norm(f)
        
        if norm <= 0 or r_f <= 0:
            continue
        
        ratio = norm / (n**Fraction(1, 2))
        total_metric_value += ratio
        instances_tested += 1
        max_n = max(max_n, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Ratio of Norm to sqrt(n)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Ratio of Norm to sqrt(n)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)